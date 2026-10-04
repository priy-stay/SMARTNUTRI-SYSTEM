import pandas as pd


def clean_food_data(food, food_nutrient, nutrient):

    food = food.drop_duplicates()

    food_nutrient = food_nutrient.drop_duplicates()

    nutrient = nutrient.drop_duplicates()

    food = food.dropna(subset=["fdc_id"])

    food_nutrient = food_nutrient.dropna(
        subset=["fdc_id", "nutrient_id"]
    )

    nutrient = nutrient.dropna(
        subset=["id", "name"]
    )

    return food, food_nutrient, nutrient