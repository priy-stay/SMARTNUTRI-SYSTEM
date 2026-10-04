import pandas as pd


# ==========================================
# CREATE FOOD + NUTRIENT DATASET
# ==========================================

def create_food_nutrient_dataset(
    food,
    food_nutrient,
    nutrient
):

    # --------------------------------------
    # COPY DATA
    # --------------------------------------

    food_data = food.copy()
    food_nutrient_data = food_nutrient.copy()
    nutrient_data = nutrient.copy()

    # --------------------------------------
    # CLEAN COLUMN NAMES
    # --------------------------------------

    food_data.columns = (
        food_data.columns
        .astype(str)
        .str.strip()
    )

    food_nutrient_data.columns = (
        food_nutrient_data.columns
        .astype(str)
        .str.strip()
    )

    nutrient_data.columns = (
        nutrient_data.columns
        .astype(str)
        .str.strip()
    )

    # --------------------------------------
    # NUTRIENT ID
    # --------------------------------------

    if "id" in nutrient_data.columns:

        nutrient_data = nutrient_data.rename(
            columns={
                "id": "nutrient_id"
            }
        )

    # --------------------------------------
    # CHECK REQUIRED COLUMNS
    # --------------------------------------

    required_food = [
        "fdc_id",
        "description"
    ]

    required_food_nutrient = [
        "fdc_id",
        "nutrient_id"
    ]

    for column in required_food:

        if column not in food_data.columns:

            raise ValueError(
                f"Missing column in food data: {column}"
            )

    for column in required_food_nutrient:

        if column not in food_nutrient_data.columns:

            raise ValueError(
                f"Missing column in food nutrient data: {column}"
            )

    # --------------------------------------
    # MERGE FOOD NUTRIENT + NUTRIENT
    # --------------------------------------

    merged = food_nutrient_data.merge(
        nutrient_data,
        on="nutrient_id",
        how="left"
    )

    # --------------------------------------
    # MERGE WITH FOOD
    # --------------------------------------

    merged = merged.merge(
        food_data[
            [
                "fdc_id",
                "description"
            ]
        ],
        on="fdc_id",
        how="left"
    )

    # --------------------------------------
    # REMOVE INVALID FOOD NAMES
    # --------------------------------------

    merged["description"] = (
        merged["description"]
        .astype(str)
        .str.strip()
    )

    merged = merged[
        merged["description"]
        .notna()
    ].copy()

    # --------------------------------------
    # REMOVE DUPLICATE FOOD/NUTRIENT ROWS
    # --------------------------------------

    merged = merged.drop_duplicates(
        subset=[
            "fdc_id",
            "nutrient_id"
        ]
    )

    return merged