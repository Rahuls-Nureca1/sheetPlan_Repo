
from models.plan_schedule_model import Planned_Meal


def process_planned_meal_recipe(recipe, planned_meal):
    """
    This function is used to process the planned_meal recipe
    - Calculates the nutrition info as per quantity in meal plan
    - Update serving info

    Params
    - `recipe` - Recipe object
    - `planned_meal` - Planned_Meal object

    Returns
    - `recipe` - Updated Recipe object
    """
    # Calculate nutrition as per quantity in planned meal
    meal_servings_ratio = planned_meal['quantity'] / recipe['serving']
    for type in ['macros', 'micros']:
        for nutrient in recipe[type]:
            nutrient['value'] = round(
                nutrient['value'] * meal_servings_ratio, 2)

    # Update serving info
    recipe['serving'] = planned_meal['serving']
    recipe['serving']['quantity'] = planned_meal['quantity']
    return recipe
