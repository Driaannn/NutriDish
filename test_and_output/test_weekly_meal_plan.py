import pandas as pd
from scripts.data_storage import load_from_sql, save_to_json
from scripts.recipe_search import search_recipes
from scripts.weekly_meal_plan import generate_weekly_menu
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
# Load dataset from SQLite
data = load_from_sql(db_path=PROJECT_ROOT / "data" / "recipes.db", table_name="recipes")

# User input simulation
user_input = {
    "keywords": "",
    "ingredients": [],
    "nutritional_constraints": {
        "calories": {"min": 0, "max": 9999},
        "protein": {"min": 0, "max": 9999},
        "fat": {"min": 0, "max": 9999},
        "sodium": {"min": 0, "max": 9999},
    },
    "tags": {"breakfast": True, "lunch": True, "dinner": True, "snack": True, "dessert": True},
}

# Generate weekly menu
weekly_menu, cooldown_tracker = generate_weekly_menu(data, user_input)
save_to_json(weekly_menu, json_path=PROJECT_ROOT / "data" / "weekly_menu.json")

# Output the result
print("Weekly menu generated and saved to JSON.")
