"""
Camada de dados do bot — pontos, streak e referral.

Guarda tudo num arquivo JSON simples (keto_data.json). É de propósito bem
isolado: se no futuro a gente trocar pra SQLite/Postgres, só mexe aqui,
o resto do bot (main.py) não precisa saber como os dados são guardados.

ATENÇÃO: no plano Free do Render o disco é temporário — os dados se
perdem a cada novo deploy ou quando o serviço reinicia sozinho por
inatividade. Serve pra testar a lógica agora; antes de ir pra produção
de verdade, migrar pra um banco persistente (SQLite com Render Disk,
ou um banco externo tipo Postgres/Supabase gratuito).
"""

import json
import logging
import os
import threading
from datetime import date, datetime, timedelta

log = logging.getLogger("keto_family_bot.store")

DATA_FILE = os.environ.get("DATA_FILE", "keto_data.json")

_lock = threading.Lock()

# ---------- Pontuação (ajuste os valores aqui, sem mexer na lógica) ----------

WELCOME_BONUS = 100
CHECKIN_POINTS = 10
STREAK_BONUSES = {7: 50, 14: 100, 21: 200}  # dias de streak -> pontos extra
REFERRAL_PERCENT = 0.20  # indicador ganha 20% de todo ponto do indicado, pra sempre


def _default_data():
    return {"next_member_number": 1, "users": {}}


def _load():
    if not os.path.exists(DATA_FILE):
        return _default_data()
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        log.error(f"Erro lendo {DATA_FILE}, começando do zero: {e}")
        return _default_data()


def _save(data):
    tmp_file = DATA_FILE + ".tmp"
    with open(tmp_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    os.replace(tmp_file, DATA_FILE)


def _new_user(member_number, username, referred_by=None):
    return {
        "username": username,
        "member_number": member_number,
        "points": 0,
        "streak": 0,
        "last_checkin": None,
        "referred_by": referred_by,
        "referral_count": 0,
        "joined_at": datetime.utcnow().isoformat(),
    }


def get_or_create_user(user_id, username=None, referred_by=None):
    """Retorna (user_dict, created_bool). Se já existir, ignora referred_by."""
    user_id = str(user_id)
    with _lock:
        data = _load()
        created = False
        if user_id not in data["users"]:
            member_number = data["next_member_number"]
            data["next_member_number"] = member_number + 1

            valid_referrer = None
            if referred_by is not None:
                referred_by = str(referred_by)
                if referred_by != user_id and referred_by in data["users"]:
                    valid_referrer = referred_by

            data["users"][user_id] = _new_user(member_number, username, valid_referrer)
            if valid_referrer:
                data["users"][valid_referrer]["referral_count"] += 1
            created = True
        else:
            # atualiza username se mudou
            if username:
                data["users"][user_id]["username"] = username
        _save(data)
        return data["users"][user_id], created


def add_points(user_id, amount, apply_referral=True):
    """Soma pontos ao usuário. Se ele tiver indicador, o indicador ganha
    20% desses mesmos pontos também (sem afetar o streak dele)."""
    user_id = str(user_id)
    with _lock:
        data = _load()
        user = data["users"].get(user_id)
        if not user:
            return None
        user["points"] += amount

        if apply_referral and user.get("referred_by"):
            referrer_id = user["referred_by"]
            referrer = data["users"].get(referrer_id)
            if referrer:
                bonus = int(amount * REFERRAL_PERCENT)
                if bonus > 0:
                    referrer["points"] += bonus

        _save(data)
        return user["points"]


def do_checkin(user_id):
    """
    Processa o /checkin de hoje.
    Retorna um dict com: ok, already_done, streak, points_earned, bonus, total_points
    """
    user_id = str(user_id)
    today = date.today()

    with _lock:
        data = _load()
        user = data["users"].get(user_id)
        if not user:
            return {"ok": False, "reason": "no_user"}

        last_str = user.get("last_checkin")
        last = date.fromisoformat(last_str) if last_str else None

        if last == today:
            return {
                "ok": True,
                "already_done": True,
                "streak": user["streak"],
                "total_points": user["points"],
            }

        if last == today - timedelta(days=1):
            user["streak"] += 1
        else:
            user["streak"] = 1  # perdeu um dia (ou é o primeiro checkin) -> reseta

        user["last_checkin"] = today.isoformat()

        earned = CHECKIN_POINTS
        bonus = STREAK_BONUSES.get(user["streak"], 0)
        total_earned = earned + bonus

        user["points"] += total_earned

        # referral: indicador ganha 20% do que foi ganho hoje
        referrer_id = user.get("referred_by")
        if referrer_id:
            referrer = data["users"].get(referrer_id)
            if referrer:
                kickback = int(total_earned * REFERRAL_PERCENT)
                if kickback > 0:
                    referrer["points"] += kickback

        _save(data)

        return {
            "ok": True,
            "already_done": False,
            "streak": user["streak"],
            "points_earned": earned,
            "bonus": bonus,
            "total_points": user["points"],
        }


def get_top(n=10):
    with _lock:
        data = _load()
        users = [
            {"user_id": uid, **u} for uid, u in data["users"].items()
        ]
        users.sort(key=lambda u: u["points"], reverse=True)
        return users[:n]


def get_rank(user_id):
    """Retorna (posicao, total_de_usuarios, pontos) - posicao é 1-based."""
    user_id = str(user_id)
    with _lock:
        data = _load()
        users = [
            {"user_id": uid, **u} for uid, u in data["users"].items()
        ]
        users.sort(key=lambda u: u["points"], reverse=True)
        for i, u in enumerate(users, start=1):
            if u["user_id"] == user_id:
                return i, len(users), u["points"]
        return None, len(users), 0


def get_user(user_id):
    user_id = str(user_id)
    with _lock:
        data = _load()
        return data["users"].get(user_id)
