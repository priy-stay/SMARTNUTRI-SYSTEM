import os
import pandas as pd

from data_loader import (
    load_food_data,
    load_food_nutrient_data,
    load_nutrient_data,
    load_disease_rules
)

from recommendation_engine import (
    create_recommendations,
    get_age_group,
    calculate_bmi,
    get_bmi_category,
    get_avoid_foods
)


print("==========================================")
print("          SMARTNUTRI AI SYSTEM")
print("==========================================")

# -------------------------------------------------
# LOAD REAL DATA
# -------------------------------------------------

print("\nLoading real USDA data...")

food = load_food_data()
food_nutrient = load_food_nutrient_data()
nutrient = load_nutrient_data()
rules = load_disease_rules()

print("Food rows:", len(food))
print("Food nutrient rows:", len(food_nutrient))
print("Nutrient rows:", len(nutrient))
print("Disease rules:", len(rules))


# -------------------------------------------------
# USER DETAILS
# -------------------------------------------------

print("\n========== USER DETAILS ==========")

age = int(input("Enter age: "))
gender = input("Enter gender (Optional): ").strip()
disease = input("Enter disease / health condition: ").strip()
weight = float(input("Enter weight in kg: "))
height = float(input("Enter height in cm: "))

food_preference = input(
    "Enter food preference "
    "(Vegetarian/Non-Vegetarian/Vegan/Any): "
).strip()


# -------------------------------------------------
# AGE GROUP
# -------------------------------------------------

age_group = get_age_group(age)

print("\n==========================================")
print("Age Group:", age_group)


# -------------------------------------------------
# BMI
# -------------------------------------------------

bmi = calculate_bmi(weight, height)
bmi_category = get_bmi_category(bmi)


# -------------------------------------------------
# AI RECOMMENDATIONS
# -------------------------------------------------

recommendations = create_recommendations(
    age=age,
    disease=disease,
    food_preference=food_preference,
    food=food,
    food_nutrient=food_nutrient,
    nutrient=nutrient,
    rules=rules
)

print("\nMatched food records:", len(recommendations))


# -------------------------------------------------
# USER PROFILE
# -------------------------------------------------

print("\n========== USER PROFILE ==========")

print("Age:", age)
print("Age Group:", age_group)
print("Gender:", gender)
print("Disease:", disease)
print("Weight:", weight, "kg")
print("Height:", height, "cm")
print("BMI:", round(bmi, 2))
print("BMI Category:", bmi_category)
print("Food Preference:", food_preference)


# -------------------------------------------------
# RECOMMENDED / MODERATE FOODS
# -------------------------------------------------

final_rows = []

if not recommendations.empty:

    recommendations["amount"] = pd.to_numeric(
        recommendations["amount"],
        errors="coerce"
    ).fillna(0)

    # Priority score
    priority_map = {
        "high": 3,
        "medium": 2,
        "low": 1
    }

    recommendations["priority_score"] = (
        recommendations["priority"]
        .astype(str)
        .str.lower()
        .map(priority_map)
        .fillna(1)
    )

    # Recommendation score
    recommendation_map = {
        "recommended": 3,
        "moderate": 2
    }

    recommendations["recommendation_score"] = (
        recommendations["recommendation"]
        .astype(str)
        .str.lower()
        .map(recommendation_map)
        .fillna(1)
    )

    # AI score
    recommendations["AI_score"] = (
        recommendations["priority_score"] * 50
        +
        recommendations["recommendation_score"] * 30
        +
        recommendations["amount"].clip(upper=100)
    )

    # Remove duplicate food records
    recommendations = recommendations.drop_duplicates(
        subset=[
            "disease",
            "age_group",
            "description",
            "recommendation"
        ]
    )

    recommendations = recommendations.sort_values(
        by="AI_score",
        ascending=False
    )

    recommendations = recommendations.head(10)

    print("\n========== RECOMMENDED / MODERATE FOODS ==========")

    display_columns = [
        "description",
        "food_category",
        "recommendation",
        "priority",
        "reason",
        "AI_score"
    ]

    print(
        recommendations[display_columns].to_string(
            index=False
        )
    )

    # Add user information
    recommendations["user_age"] = age
    recommendations["gender"] = gender
    recommendations["weight_kg"] = weight
    recommendations["height_cm"] = height
    recommendations["food_preference"] = food_preference
    recommendations["BMI"] = round(bmi, 2)
    recommendations["BMI_category"] = bmi_category

    # Rename description for final structure
    recommendations["food_name"] = recommendations["description"]

    final_rows.append(recommendations)


# -------------------------------------------------
# AVOID FOODS
# -------------------------------------------------

avoid_foods = get_avoid_foods(
    age=age,
    disease=disease,
    rules=rules
)

print("\n========== AVOID FOODS ==========")

if avoid_foods.empty:

    print("No avoid-food rules found.")

else:

    for _, row in avoid_foods.iterrows():

        print("\nFood     :", row["food_name"])
        print("Category :", row["food_category"])
        print("Priority :", row["priority"])
        print("Reason   :", row["reason"])

    # Convert avoid rules into final CSV rows
    avoid_rows = avoid_foods.copy()

    avoid_rows["disease"] = disease
    avoid_rows["age_group"] = age_group

    avoid_rows["user_age"] = age
    avoid_rows["gender"] = gender
    avoid_rows["weight_kg"] = weight
    avoid_rows["height_cm"] = height
    avoid_rows["food_preference"] = food_preference
    avoid_rows["BMI"] = round(bmi, 2)
    avoid_rows["BMI_category"] = bmi_category

    avoid_rows["food_name"] = avoid_rows["food_name"]

    avoid_rows["fdc_id"] = None
    avoid_rows["description"] = avoid_rows["food_name"]
    avoid_rows["amount"] = None

    avoid_rows["priority_score"] = (
        avoid_rows["priority"]
        .astype(str)
        .str.lower()
        .map({
            "high": 3,
            "medium": 2,
            "low": 1 
        })
        .fillna(1)
    )
    avoid_rows["AI_score"] = (
        avoid_rows["priority_score"] * 50
    )
    final_rows.append(avoid_rows)

    if final_rows:
        final_result = pd.concat(final_rows, ignore_index=True)
    else:
        final_result = pd.DataFrame()


    os.makedirs("output", exist_ok=True)
    output_file = "output/smartnutri_ai_results.csv"
    final_result.to_csv(output_file, index=False)
    print("\nFinal recommendation file created:",output_file)
    print("\nTotal final records:", len(final_result))
    print("\n===========================================")
    print("     SMARTNUTRI PROCESS COMPLETED")
    print("===========================================")        