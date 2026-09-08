from flask import Flask
from threading import Thread
import os
app = Flask('')
@app.route('/')
def home(): return "KETO FAMILY BOT TA ON!"
def run_flask():
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
def keep_alive():
    t = Thread(target=run_flask)
    t.daemon = True
    t.start()
