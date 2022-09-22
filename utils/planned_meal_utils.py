
from models.plan_schedule_model import Planned_Meal
from schemas.plan_schedule_schema import PlannedMealSchema


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


def get_planned_meal_serving_details(recipe_id, schedule_id):
    """
    This function is used to get the planned meal quantity

    Params
    - `recipe_id` - Recipe ID
    - `schedule_id` - Schedule ID

    Returns
    - `servings` - Planned meal quantity
    """
    planned_meal_data = Planned_Meal.query.filter_by(recipe_id=recipe_id, schedule_id=schedule_id).first()
    meal_data = PlannedMealSchema().dump(planned_meal_data)

    response = {
        **meal_data['serving'],
        'quantity': meal_data['quantity']
    }

    return response