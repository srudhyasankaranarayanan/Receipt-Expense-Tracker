# ---------------------------------------------
# RECIPE DATABASE
# ---------------------------------------------

recipes = {

    "Tomato Rice": [
        "rice",
        "tomato",
        "onion"
    ],

    "Potato Curry": [
        "potato",
        "onion",
        "tomato"
    ],

    "Vegetable Rice": [
        "rice",
        "carrot",
        "beans",
        "onion"
    ],

    "Fried Rice": [
        "rice",
        "carrot",
        "beans",
        "onion"
    ],

    "Vegetable Curry": [
        "potato",
        "carrot",
        "beans",
        "onion",
        "tomato"
    ],

    "Dal Rice": [
        "rice",
        "dal",
        "onion",
        "tomato"
    ],

    "Curd Rice": [
        "rice",
        "milk",
        "curd"
    ],

    "Potato Rice": [
        "rice",
        "potato",
        "onion"
    ]
}


# ---------------------------------------------
# INGREDIENT ALIASES
# ---------------------------------------------

ingredient_aliases = {

    "tomatoes": "tomato",
    "onions": "onion",
    "potatoes": "potato",
    "carrots": "carrot",
    "beans": "beans",

    "basmati rice": "rice",
    "raw rice": "rice",
    "rice": "rice",

    "toor dal": "dal",
    "tuvar dal": "dal",
    "tur dal": "dal",
    "moong dal": "dal",

    "curd": "curd",
    "yogurt": "curd",

    "milk": "milk"
}


# ---------------------------------------------
# NORMALIZE INGREDIENT
# ---------------------------------------------

def normalize_ingredient(item):

    item = item.lower().strip()

    for key, value in ingredient_aliases.items():

        if key in item:
            return value

    return item


# ---------------------------------------------
# FIND RECIPES
# ---------------------------------------------

def find_recipes(available_items):

    normalized_items = []

    for item in available_items:

        normalized = normalize_ingredient(item)

        normalized_items.append(normalized)

    suggestions = []

    for recipe_name, ingredients in recipes.items():

        matched = []

        for ingredient in ingredients:

            for item in normalized_items:

                if ingredient in item:

                    matched.append(ingredient)

                    break

        match_percentage = (
            len(set(matched))
            / len(ingredients)
        ) * 100

        if match_percentage >= 50:

            suggestions.append({
                "Recipe": recipe_name,
                "Match": match_percentage,
                "Available": matched
            })

    suggestions.sort(
        key=lambda x: x["Match"],
        reverse=True
    )

    return suggestions