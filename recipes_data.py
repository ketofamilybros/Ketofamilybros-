"""
Receitas keto próprias do bot — sem link externo, sem propaganda.

Estrutura: RECIPES é um dict de categoria -> {"label": str, "items": [(title, text), ...]}
"items" é uma lista (não dict) pra manter a ordem e permitir referenciar por índice
no callback_data (recipe:<categoria>:<índice>), que precisa ser curto.
"""

RECIPES = {
    "breakfast": {
        "label": "🌅 Breakfast",
        "items": [
            (
                "Scrambled Eggs with Bacon & Avocado",
                "🍳 *Scrambled Eggs with Bacon & Avocado*\n\n"
                "*Ingredients:*\n"
                "• 3 eggs\n• 2 strips of bacon\n• 1/2 avocado\n• 1 tbsp butter\n• Salt & pepper\n\n"
                "*Steps:*\n"
                "1. Fry the bacon until crispy, set aside.\n"
                "2. Melt butter in the same pan, add whisked eggs on low heat, stirring gently.\n"
                "3. Season with salt & pepper, plate with bacon and sliced avocado on the side.",
            ),
            (
                "Keto Pancakes",
                "🥞 *Keto Pancakes*\n\n"
                "*Ingredients:*\n"
                "• 2 eggs\n• 1 cup almond flour\n• 1/4 cup cream cheese\n• 1 tsp baking powder\n• 1 tsp cinnamon (optional)\n• Butter for the pan\n\n"
                "*Steps:*\n"
                "1. Blend all ingredients until smooth.\n"
                "2. Heat butter in a non-stick pan over medium-low heat.\n"
                "3. Pour small circles of batter, cook 2 min per side until golden.\n"
                "4. Serve with sugar-free syrup or berries.",
            ),
            (
                "Cheese & Spinach Stuffed Omelet",
                "🧀 *Cheese & Spinach Stuffed Omelet*\n\n"
                "*Ingredients:*\n"
                "• 3 eggs\n• 1 handful fresh spinach\n• 1/4 cup shredded cheese\n• 1 tbsp butter\n• Salt & pepper\n\n"
                "*Steps:*\n"
                "1. Sauté spinach in butter until wilted, remove from pan.\n"
                "2. Pour whisked eggs into the pan, cook on low heat until mostly set.\n"
                "3. Add spinach and cheese on one half, fold the omelet over.\n"
                "4. Cook 1 more minute until cheese melts.",
            ),
            (
                "Coconut Flour Pancakes",
                "🥥 *Coconut Flour Pancakes*\n\n"
                "*Ingredients:*\n"
                "• 3 eggs\n• 3 tbsp coconut flour\n• 2 tbsp melted butter\n• 2 tbsp cream or coconut milk\n• 1/2 tsp baking powder\n• Pinch of salt\n\n"
                "*Steps:*\n"
                "1. Whisk eggs, butter and cream together.\n"
                "2. Mix in coconut flour, baking powder and salt until smooth (batter will be thick).\n"
                "3. Cook small spoonfuls in a greased pan, 2 min per side.",
            ),
            (
                "Chaffle (Cheese & Egg Waffle)",
                "🧇 *Chaffle (Cheese & Egg Waffle)*\n\n"
                "*Ingredients:*\n"
                "• 1 egg\n• 1/2 cup shredded mozzarella\n• Pinch of garlic powder (optional)\n\n"
                "*Steps:*\n"
                "1. Whisk egg and cheese together.\n"
                "2. Pour into a hot mini waffle iron.\n"
                "3. Cook 3-4 min until golden and crispy.\n"
                "4. Great plain, or as a base for a sandwich.",
            ),
            (
                "Green Keto Smoothie",
                "🥑 *Green Keto Smoothie*\n\n"
                "*Ingredients:*\n"
                "• 1/2 avocado\n• 1 handful spinach\n• 1 cup unsweetened almond or coconut milk\n• 1 tbsp MCT oil or coconut oil\n• Ice cubes\n\n"
                "*Steps:*\n"
                "1. Add everything to a blender.\n"
                "2. Blend until smooth and creamy.\n"
                "3. Drink immediately for a quick energizing breakfast.",
            ),
            (
                "Greek Yogurt with Keto Granola",
                "🥣 *Greek Yogurt with Keto Granola*\n\n"
                "*Ingredients:*\n"
                "• 1 cup full-fat Greek yogurt\n• 1/4 cup chopped nuts (almonds, pecans, walnuts)\n• 1 tbsp shredded unsweetened coconut\n• A few berries\n• Cinnamon to taste\n\n"
                "*Steps:*\n"
                "1. Toast the nuts and coconut in a dry pan for 2-3 min until fragrant.\n"
                "2. Layer yogurt in a bowl, top with the toasted mix and berries.\n"
                "3. Sprinkle cinnamon on top.",
            ),
        ],
    },
    "lunch": {
        "label": "☀️ Lunch",
        "items": [
            (
                "Keto Picanha (Brazilian Steak)",
                "🥩 *Keto Picanha*\n\n"
                "*Ingredients:*\n"
                "• 1 picanha steak (or top sirloin cap)\n• Coarse salt\n• 1 tbsp butter\n\n"
                "*Steps:*\n"
                "1. Score the fat cap in a criss-cross pattern, season generously with coarse salt.\n"
                "2. Sear fat-side down in a hot pan until golden and rendered, about 5 min.\n"
                "3. Flip and sear the other side to your preferred doneness, basting with butter.\n"
                "4. Rest 5 min before slicing against the grain.",
            ),
            (
                "Grilled Chicken with Herb Butter",
                "🍗 *Grilled Chicken with Herb Butter*\n\n"
                "*Ingredients:*\n"
                "• 2 chicken breasts\n• 2 tbsp butter, softened\n• 1 tsp chopped parsley\n• 1 clove garlic, minced\n• Salt & pepper\n\n"
                "*Steps:*\n"
                "1. Mix butter, parsley and garlic together.\n"
                "2. Season chicken with salt & pepper, grill or pan-sear until cooked through (~6 min per side).\n"
                "3. Top with a spoonful of herb butter while hot.",
            ),
            (
                "Keto Caesar Salad (No Croutons)",
                "🥗 *Keto Caesar Salad*\n\n"
                "*Ingredients:*\n"
                "• Romaine lettuce, chopped\n• Grilled chicken strips (optional)\n• 1/4 cup parmesan, shaved\n• 2 tbsp Caesar dressing (check label for sugar)\n• Crispy bacon bits instead of croutons\n\n"
                "*Steps:*\n"
                "1. Toss lettuce with dressing.\n"
                "2. Top with parmesan, bacon bits and chicken.\n"
                "3. Serve immediately.",
            ),
            (
                "Lettuce Wrap Burger",
                "🍔 *Lettuce Wrap Burger*\n\n"
                "*Ingredients:*\n"
                "• 1 beef patty\n• 2 large lettuce leaves (for the \"bun\")\n• 1 slice cheese\n• Tomato, onion, pickles to taste\n• Mustard or sugar-free ketchup\n\n"
                "*Steps:*\n"
                "1. Season and grill the patty to your liking, melt cheese on top.\n"
                "2. Layer the patty and toppings between the lettuce leaves.\n"
                "3. Wrap like a burrito and enjoy.",
            ),
            (
                "Cheese & Bacon Stuffed Chicken",
                "🧀 *Cheese & Bacon Stuffed Chicken*\n\n"
                "*Ingredients:*\n"
                "• 2 chicken breasts\n• 2 slices cheese\n• 2 strips cooked bacon\n• Toothpicks\n• Salt & pepper\n\n"
                "*Steps:*\n"
                "1. Cut a pocket into each chicken breast, season inside and out.\n"
                "2. Stuff with cheese and bacon, secure with toothpicks.\n"
                "3. Sear in a pan 4 min per side, then finish in the oven at 190°C for 15 min.",
            ),
            (
                "Tuna & Avocado Salad",
                "🐟 *Tuna & Avocado Salad*\n\n"
                "*Ingredients:*\n"
                "• 1 can tuna, drained\n• 1/2 avocado, diced\n• 2 tbsp mayo\n• 1 tbsp lemon juice\n• Salt & pepper\n\n"
                "*Steps:*\n"
                "1. Mix all ingredients gently in a bowl (keep avocado chunky).\n"
                "2. Serve over lettuce leaves or straight from the bowl.",
            ),
            (
                "Baked Pork Ribs with Cauliflower",
                "🍖 *Baked Pork Ribs with Cauliflower*\n\n"
                "*Ingredients:*\n"
                "• 500g pork ribs\n• 1 tbsp sugar-free BBQ seasoning or paprika/garlic powder\n• 1/2 head cauliflower, florets\n• Olive oil, salt\n\n"
                "*Steps:*\n"
                "1. Season ribs, bake at 180°C covered for 45 min.\n"
                "2. Uncover, raise heat to 220°C, roast 15 more min until browned.\n"
                "3. Toss cauliflower in olive oil and salt, roast alongside for the last 20 min.",
            ),
        ],
    },
    "dinner": {
        "label": "🌙 Dinner",
        "items": [
            (
                "Baked Salmon with Asparagus",
                "🐟 *Baked Salmon with Asparagus*\n\n"
                "*Ingredients:*\n"
                "• 1 salmon fillet\n• 1 bunch asparagus\n• 1 tbsp olive oil\n• 1 lemon\n• Salt & pepper\n\n"
                "*Steps:*\n"
                "1. Place salmon and asparagus on a baking tray, drizzle with olive oil.\n"
                "2. Season with salt, pepper and lemon slices.\n"
                "3. Bake at 200°C for 12-15 min until salmon flakes easily.",
            ),
            (
                "Creamy Broccoli & Cheese Soup",
                "🥦 *Creamy Broccoli & Cheese Soup*\n\n"
                "*Ingredients:*\n"
                "• 2 cups broccoli florets\n• 1 cup chicken broth\n• 1/2 cup heavy cream\n• 1/2 cup shredded cheddar\n• Salt & pepper\n\n"
                "*Steps:*\n"
                "1. Simmer broccoli in broth until tender, about 10 min.\n"
                "2. Blend until smooth (or leave chunky, your call).\n"
                "3. Stir in cream and cheese over low heat until melted. Season to taste.",
            ),
            (
                "Keto Skillet Pizza",
                "🍕 *Keto Skillet Pizza*\n\n"
                "*Ingredients:*\n"
                "• 1 cup shredded mozzarella (for the crust)\n• 2 tbsp almond flour\n• 1 egg\n• Sugar-free tomato sauce, extra cheese and toppings\n\n"
                "*Steps:*\n"
                "1. Mix mozzarella, almond flour and egg into a dough, press into a hot skillet.\n"
                "2. Cook 3-4 min until the base sets and browns underneath.\n"
                "3. Flip, add sauce, cheese and toppings, cover and cook until cheese melts.",
            ),
            (
                "Filet Mignon with Garlic Butter",
                "🥩 *Filet Mignon with Garlic Butter*\n\n"
                "*Ingredients:*\n"
                "• 1 filet mignon steak\n• 2 tbsp butter\n• 2 cloves garlic, smashed\n• 1 sprig rosemary or thyme\n• Salt & pepper\n\n"
                "*Steps:*\n"
                "1. Season steak generously, sear in a hot pan 3-4 min per side.\n"
                "2. Add butter, garlic and herbs to the pan, baste the steak for 1 min.\n"
                "3. Rest 5 min before serving.",
            ),
            (
                "Garlic Butter Shrimp",
                "🍤 *Garlic Butter Shrimp*\n\n"
                "*Ingredients:*\n"
                "• 300g shrimp, peeled\n• 3 tbsp butter\n• 3 cloves garlic, minced\n• Juice of 1/2 lemon\n• Parsley, salt & pepper\n\n"
                "*Steps:*\n"
                "1. Melt butter in a pan, sauté garlic for 30 sec until fragrant.\n"
                "2. Add shrimp, cook 2 min per side until pink.\n"
                "3. Finish with lemon juice and parsley.",
            ),
            (
                "Keto Eggplant Parmesan",
                "🍆 *Keto Eggplant Parmesan*\n\n"
                "*Ingredients:*\n"
                "• 1 eggplant, sliced\n• 1 cup sugar-free marinara sauce\n• 1 cup shredded mozzarella\n• 1/4 cup grated parmesan\n• Olive oil, salt\n\n"
                "*Steps:*\n"
                "1. Salt eggplant slices, let sit 10 min, pat dry, then pan-fry in olive oil until soft.\n"
                "2. Layer eggplant, sauce and cheeses in a baking dish, repeat layers.\n"
                "3. Bake at 190°C for 20 min until bubbly and golden.",
            ),
            (
                "Keto Chicken Parmesan",
                "🍗 *Keto Chicken Parmesan*\n\n"
                "*Ingredients:*\n"
                "• 2 chicken breasts, pounded thin\n• 1/2 cup almond flour + parmesan (for the crust)\n• 1 egg, beaten\n• 1 cup sugar-free marinara\n• 1 cup shredded mozzarella\n\n"
                "*Steps:*\n"
                "1. Dip chicken in egg, then coat with almond flour/parmesan mix.\n"
                "2. Pan-fry until golden on both sides.\n"
                "3. Top with marinara and mozzarella, bake at 190°C for 10 min until cheese melts.",
            ),
        ],
    },
    "snacks": {
        "label": "🥪 Snacks",
        "items": [
            (
                "Mom's Keto Bread",
                "🍞 *Mom's Keto Bread*\n\n"
                "*Ingredients:*\n"
                "• 6 eggs\n• 1/2 cup melted butter\n• 2 cups almond flour\n• 1 tbsp baking powder\n• Pinch of salt\n\n"
                "*Steps:*\n"
                "1. Blend eggs and butter until frothy.\n"
                "2. Mix in almond flour, baking powder and salt.\n"
                "3. Pour into a greased loaf pan, bake at 180°C for 35-40 min until golden and firm.\n"
                "4. Cool before slicing.",
            ),
            (
                "Keto Sandwich",
                "🥪 *Keto Sandwich*\n\n"
                "*Ingredients:*\n"
                "• 2 slices Mom's Keto Bread (see recipe above)\n• Deli meat or grilled chicken\n• Cheese, lettuce, tomato, mayo\n\n"
                "*Steps:*\n"
                "1. Toast the keto bread slices lightly if you like.\n"
                "2. Layer with your favorite fillings.\n"
                "3. Slice and serve — a proper keto lunchbox classic.",
            ),
            (
                "Crispy Cheese Crisps",
                "🧀 *Crispy Cheese Crisps*\n\n"
                "*Ingredients:*\n"
                "• 1 cup shredded cheddar or parmesan\n\n"
                "*Steps:*\n"
                "1. Drop small mounds of cheese onto a parchment-lined tray, spaced apart.\n"
                "2. Bake at 200°C for 5-7 min until golden and bubbly.\n"
                "3. Cool 2 min before peeling off — they crisp up as they cool.",
            ),
            (
                "60-Second Keto English Muffin",
                "🍞 *60-Second Keto English Muffin*\n\n"
                "*Ingredients:*\n"
                "• 1 egg\n• 3 tbsp almond flour\n• 1/4 tsp baking powder\n• 1 tbsp melted butter\n• Pinch of salt\n\n"
                "*Steps:*\n"
                "1. Mix everything in a microwave-safe mug.\n"
                "2. Microwave for 60-90 seconds until set.\n"
                "3. Slice in half and toast if you like it crispy.",
            ),
            (
                "Breaded Eggplant Fries",
                "🍆 *Breaded Eggplant Fries*\n\n"
                "*Ingredients:*\n"
                "• 1 eggplant, cut into sticks\n• 1 egg, beaten\n• 1/2 cup almond flour + parmesan\n• Salt, garlic powder, paprika\n\n"
                "*Steps:*\n"
                "1. Dip eggplant sticks in egg, then coat in the almond flour/parmesan mix.\n"
                "2. Bake at 200°C for 20 min, flipping halfway, until crispy.\n"
                "3. Serve with sugar-free marinara for dipping.",
            ),
            (
                "Deviled Eggs",
                "🥚 *Deviled Eggs*\n\n"
                "*Ingredients:*\n"
                "• 6 hard-boiled eggs\n• 3 tbsp mayo\n• 1 tsp mustard\n• Paprika, salt & pepper\n\n"
                "*Steps:*\n"
                "1. Halve the eggs, scoop out yolks into a bowl.\n"
                "2. Mash yolks with mayo, mustard, salt and pepper.\n"
                "3. Pipe or spoon the filling back into the whites, dust with paprika.",
            ),
            (
                "Seasoned Nut Mix",
                "🥜 *Seasoned Nut Mix*\n\n"
                "*Ingredients:*\n"
                "• 1 cup mixed nuts (almonds, walnuts, pecans)\n• 1 tbsp melted butter or olive oil\n• Salt, paprika, garlic powder to taste\n\n"
                "*Steps:*\n"
                "1. Toss nuts with butter and seasonings.\n"
                "2. Roast at 160°C for 10 min, stirring halfway, until fragrant.\n"
                "3. Cool completely before storing — great grab-and-go snack.",
            ),
        ],
    },
    "dessert": {
        "label": "🍫 Dessert",
        "items": [
            (
                "Coconut Butter Fat Bombs",
                "🥥 *Coconut Butter Fat Bombs*\n\n"
                "*Ingredients:*\n"
                "• 1/2 cup coconut oil, melted\n• 1/2 cup shredded unsweetened coconut\n• 2 tbsp butter, softened\n• 1 tbsp sugar-free sweetener (optional)\n\n"
                "*Steps:*\n"
                "1. Mix all ingredients until combined.\n"
                "2. Spoon into a silicone mold or mini muffin liners.\n"
                "3. Freeze for 30 min until solid. Store in the fridge.",
            ),
            (
                "Keto Mini Cheesecakes",
                "🍰 *Keto Mini Cheesecakes*\n\n"
                "*Ingredients:*\n"
                "• 250g cream cheese, softened\n• 2 eggs\n• 1/2 cup sugar-free sweetener\n• 1 tsp vanilla extract\n\n"
                "*Steps:*\n"
                "1. Beat cream cheese until smooth, add eggs one at a time.\n"
                "2. Mix in sweetener and vanilla.\n"
                "3. Pour into muffin liners, bake at 160°C for 18-20 min.\n"
                "4. Cool completely, then chill in the fridge for at least 2 hours.",
            ),
            (
                "Keto Chocolate Brownies",
                "🍫 *Keto Chocolate Brownies*\n\n"
                "*Ingredients:*\n"
                "• 1/2 cup butter, melted\n• 1 cup almond flour\n• 1/3 cup cocoa powder\n• 1/2 cup sugar-free sweetener\n• 2 eggs\n• 1/2 tsp baking powder\n\n"
                "*Steps:*\n"
                "1. Mix melted butter with sweetener, then whisk in eggs.\n"
                "2. Fold in almond flour, cocoa and baking powder.\n"
                "3. Pour into a greased pan, bake at 175°C for 18-20 min.\n"
                "4. Cool before cutting into squares.",
            ),
            (
                "2-Ingredient Keto Vanilla Ice Cream",
                "🍦 *2-Ingredient Keto Vanilla Ice Cream*\n\n"
                "*Ingredients:*\n"
                "• 2 cups heavy cream, well chilled\n• 1/2 cup sugar-free sweetener + 1 tsp vanilla extract\n\n"
                "*Steps:*\n"
                "1. Whip the cream with sweetener and vanilla until stiff peaks form.\n"
                "2. Transfer to a container, freeze for at least 4 hours.\n"
                "3. Let sit 5 min at room temp before scooping.",
            ),
            (
                "Chocolate Avocado Mousse",
                "🥑 *Chocolate Avocado Mousse*\n\n"
                "*Ingredients:*\n"
                "• 2 ripe avocados\n• 1/4 cup cocoa powder\n• 1/4 cup sugar-free sweetener\n• 1/4 cup almond milk\n• 1 tsp vanilla extract\n\n"
                "*Steps:*\n"
                "1. Blend all ingredients until completely smooth and creamy.\n"
                "2. Taste and adjust sweetness if needed.\n"
                "3. Chill for at least 30 min before serving.",
            ),
            (
                "Coconut Chia Pudding",
                "🥄 *Coconut Chia Pudding*\n\n"
                "*Ingredients:*\n"
                "• 1 cup coconut milk\n• 3 tbsp chia seeds\n• 1 tbsp sugar-free sweetener\n• 1/2 tsp vanilla extract\n\n"
                "*Steps:*\n"
                "1. Whisk everything together in a jar.\n"
                "2. Refrigerate at least 4 hours (or overnight), stirring once after 30 min to prevent clumping.\n"
                "3. Top with berries or shredded coconut before serving.",
            ),
            (
                "Keto Chocolate Mug Cake",
                "☕ *Keto Chocolate Mug Cake*\n\n"
                "*Ingredients:*\n"
                "• 3 tbsp almond flour\n• 1 tbsp cocoa powder\n• 1 tbsp sugar-free sweetener\n• 1/4 tsp baking powder\n• 1 egg\n• 1 tbsp melted butter\n\n"
                "*Steps:*\n"
                "1. Mix dry ingredients in a mug.\n"
                "2. Add egg and melted butter, stir until smooth.\n"
                "3. Microwave for 60-90 seconds. Let cool slightly before eating (it's hot!).",
            ),
        ],
    },
}
