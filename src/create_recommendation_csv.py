import pandas as pd
import os

print("Creating SmartNutri recommendation CSV...")

# Disease food rules file
rules_file = "data/disease_food_rules.csv"

# Output folder
output_folder = "output"
os.makedirs(output_folder, exist_ok=True)

# Read disease food rules
rules = pd.read_csv(rules_file)

# Keep only required recommendation columns
required_columns = [
    "disease",
    "age_group",
    "food_category",
    "food_name",
    "recommendation",
    "priority",
    "reason"
]

rules = rules[required_columns]

# Remove duplicate recommendation rules
rules = rules.drop_duplicates()

# Save clean recommendation CSV
output_file = "output/smartnutri_recommendations.csv"

rules.to_csv(
    output_file,
    index=False
)

print("Recommendation CSV created successfully!")
print("Total recommendation rows:", len(rules))
print("File:", output_file)

print("\nAge groups:")
print(rules["age_group"].unique())

print("\nRecommendation types:")
print(rules["recommendation"].unique())