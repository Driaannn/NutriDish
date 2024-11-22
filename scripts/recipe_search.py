# Step 2: Define the recipe searching script

# recipe_search.py
def search_recipes(data, user_input):
    """
    Search and filter recipes based on user inputs.

    Parameters:
    - data (DataFrame): Recipe dataset.
    - user_input (dict): Processed user input from `handle_user_input`.

    Returns:
    - DataFrame: Filtered recipes matching the user's criteria.
    """
    # Extract inputs with default values
    keywords = user_input.get("keywords", "")  # Default to an empty string
    ingredients = user_input.get("ingredients", [])  # Default to an empty list
    constraints = user_input.get("nutritional_constraints", {})
    tags = user_input.get("tags", {})

    # Apply filters
    filtered_data = data.copy()

    # Filter by keywords in title
    if keywords:
        filtered_data = filtered_data[filtered_data["title"].str.contains(keywords, case=False, na=False)]

    # Filter by ingredients
    if ingredients:
        ingredient_columns = [col for col in data.columns if col in ingredients]
        if ingredient_columns:
            filtered_data = filtered_data[(filtered_data[ingredient_columns].sum(axis=1) > 0)]

    # Filter by nutritional constraints
    for nutrient, values in constraints.items():
        if nutrient in filtered_data.columns:
            filtered_data = filtered_data[
                (filtered_data[nutrient] >= values.get("min", 0)) & (filtered_data[nutrient] <= values.get("max", 9999))
            ]

    # Filter by boolean tags
    for tag, value in tags.items():
        if value and tag in filtered_data.columns:
            filtered_data = filtered_data[filtered_data[tag] == 1]

    return filtered_data


# Save this script to the file system for modularization
"""
with open("WeeklyRec/recipe_search.py", "w") as f:
    f.write(search_recipes.__code__.co_consts[0])
"""