# diet-planner-notebooks readme

## Notebooks

### add_meal_mapping_api.ipynb
- Updates meal mappings
- Requires :
    - [Meal plan mapping csv](https://docs.google.com/spreadsheets/d/1jjKx8er0NxZSRgBoLJX-KoZ6JIbn6njcIpGJB6QNVaw/) (from human supervision) which contains the mapping of recipes to a recipe id.
    - Recipe list csv (dump from DB).
    - Serving unit list csv (dump from DB).


### delete_wrong_meal_mapping_api.ipynb
- Deletes wrong meal mapping.
- Requires:
    - [Meal plan mapping csv](https://docs.google.com/spreadsheets/d/1jjKx8er0NxZSRgBoLJX-KoZ6JIbn6njcIpGJB6QNVaw/) (from human supervision) which contains the mapping of recipes to a recipe id.


### update_ingredient_and_nutrition_api.ipynb
- Use this notebook to update the ***ingredient*** table. Calories are recalculated in based on the changes in other columns like serving_unit_id, nin_id etc.
- Requires: 
    - A json containing nin ingredients data, which is exported from the *nin_ingredient* table.
    - A csv, from this [spreadsheet](https://docs.google.com/spreadsheets/d/1s7CxqU2bonZnuMCVIMIEnVOlVNmcWTe8fRRoPovpN5U), containing updated data(under human supervision).
- It also generates a csv file of the updated table.


### add_recipe_api.ipynb
- Adds new recipes to the ***recipe*** table.
- Requires:
    - A json file, from this [spreadsheet](https://docs.google.com/spreadsheets/d/1gZdstqUvPTFUCKWORt7iJIDki1G63LAn/), containing recipe data.
    - Use **recipes_csv_to_json.ipynb** notebook to obtain this json from the csv file.


### recipes_csv_to_json.ipynb
- Converts data the scraped recipe data in csv form to a json file.
- The generated json file is an input in **add_recipe_api.ipynb** notebook.


### recipe_calories_qc.ipynb
- Generates a csv for performing a QC.
- Import this csv file in this [spreadsheet](https://docs.google.com/spreadsheets/d/1mn97aEVQ1qfRD3s-2mLHAVC2CR3IzNOafy6ANU2_qS0) for human supervision.


### meal_plan_with_calories_qc.ipynb
- Generates a csv containing meals as per the diet plan along with it's serving quantity and calories.
- Import this csv file in this [spreadsheet](https://docs.google.com/spreadsheets/d/1mn97aEVQ1qfRD3s-2mLHAVC2CR3IzNOafy6ANU2_qS0) for human supervision.


###  new_nin_ingredient_json.ipynb
- Generates a json out of a csv file containing the macros of new ingredients.
- Adding new ingredients to the DB requires the usage of API's, using Postman, which requires a json text. This notebook makes it easier to fill up this json text.
- If you want to add new ingrediets to the ***nin_ingredient*** table you must first find the macros of the new ingredients and add these new entries at the bottom of this [spreadsheet](https://docs.google.com/spreadsheets/d/1s7CxqU2bonZnuMCVIMIEnVOlVNmcWTe8fRRoPovpN5U/edit#gid=1238110143).
- Copy the contents of the new ingredients onto a new spreadsheetalong with the column headers.
- Save this new spreadsheet as a csv file.
- Use this notebook to covert the csv to a json file.
- **Note**: The genereated json requires manual updates:
    - Verify the *ingredient_name*.
    - Update the *ingredient_description* with the inredient's alternate names.
    - Fill the *nin_code* with the following rules:
        - **CN$$$001**
        - **CN** - Custom NIN
        - **$$$** - 3 letters of the ingredient, whatever is indicative of the ingredient
        - 001 - First ingredient of type


###  fooddb_experiment.ipynb
- This notebook contains experiments with potential features that could be implemented for the food db.
