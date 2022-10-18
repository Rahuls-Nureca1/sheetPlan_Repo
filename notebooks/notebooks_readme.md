# diet-planner-notebooks readme

### Notebooks

**add_meal_mapping_api.ipynb**

- Takes :
    - [Meal plan mapping csv](https://docs.google.com/spreadsheets/d/1jjKx8er0NxZSRgBoLJX-KoZ6JIbn6njcIpGJB6QNVaw/) (from human supervision) which contains the mapping of recipes to a recipe id
    - recipe list csv (dump from DB)
    - serving unit list csv (dump from DB)
    

**add_recipe_api.ipynb**

- adds new recipes to the *recipe* table
- requires a json, from this [spreadsheet](https://docs.google.com/spreadsheets/d/1gZdstqUvPTFUCKWORt7iJIDki1G63LAn/), containing recipe data

**delete_wrong_meal_mapping_api.ipynb**

**generate_calories_qc_csv.ipynb**

- generates a csv for performing a QC
- copy the content of this csv file to this [spreadsheet](https://docs.google.com/spreadsheets/d/1mn97aEVQ1qfRD3s-2mLHAVC2CR3IzNOafy6ANU2_qS0) for human supervision

**update_ingredient_and_nutrition_api.ipynb**

- Use this notebook to update the ***ingredient*** table. Calories are recalculated in based on the changes in other columns like serving_unit_id, nin_id etc
- Requires a json containing nin ingredients data, which is exported from the *nin_ingredient* table
- requires a csv, from this [spreadsheet](https://docs.google.com/spreadsheets/d/1s7CxqU2bonZnuMCVIMIEnVOlVNmcWTe8fRRoPovpN5U), containing updated data(under human supervision)
- generates a csv file of the updated table