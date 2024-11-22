# Step 3: Define the weekly meal plan generation script

# weekly_meal_plan.py
def generate_weekly_menu(data, user_input, cooldown_tracker=None, cooldown_weeks=4):
    """
    Generate a weekly meal plan with cooldown and fallback handling.

    Parameters:
    - data (DataFrame): Filtered recipe dataset.
    - user_input (dict): User preferences and tags.
    - cooldown_tracker (dict, optional): Tracks recipes on cooldown. Defaults to None.
    - cooldown_weeks (int): Number of weeks a recipe remains on cooldown.

    Returns:
    - dict: Weekly meal plan with recipes per day and meal type.
    - dict: Updated cooldown tracker.
    """
    if cooldown_tracker is None:
        cooldown_tracker = {}

    # Meal types (absolute tags)
    meal_types = ["breakfast", "lunch", "snack", "dinner", "dessert"]
    weekly_menu = []

    # Update cooldown tracker
    cooldown_tracker = {recipe: weeks - 1 for recipe, weeks in cooldown_tracker.items() if weeks > 1}

    # Filter out recipes on cooldown
    available_recipes = data[~data["title"].isin(cooldown_tracker.keys())].copy()

    for day in range(7):  # Generate menu for 7 days
        daily_menu = {}

        for meal_type in meal_types:
            meal_options = available_recipes[available_recipes[meal_type] == 1]

            if not meal_options.empty:
                # Select a random recipe
                selected_recipe = meal_options.sample(1)
                recipe_title = selected_recipe["title"].values[0]

                # Add to daily menu
                daily_menu[meal_type] = recipe_title

                # Add recipe to cooldown
                cooldown_tracker[recipe_title] = cooldown_weeks

                # Remove from available recipes
                available_recipes = available_recipes[available_recipes["title"] != recipe_title]
            else:
                # Fallback: Recommend a recipe from cooldown
                fallback_recipes = data[data[meal_type] == 1]
                if not fallback_recipes.empty:
                    selected_recipe = fallback_recipes.sample(1)
                    recipe_title = selected_recipe["title"].values[0]
                    daily_menu[meal_type] = recipe_title
                else:
                    daily_menu[meal_type] = f"No {meal_type} recipe available."

        weekly_menu.append(daily_menu)

    return weekly_menu, cooldown_tracker


# Save this script to the file system for modularization
with open("WeeklyRec/weekly_meal_plan.py", "w") as f:
    f.write(generate_weekly_menu.__code__.co_consts[0])
