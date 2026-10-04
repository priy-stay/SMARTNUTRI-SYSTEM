import pandas as pd
from database import get_database_connection


print("Connecting to MySQL...")

engine = get_database_connection()

print("MySQL connection successful!")


# ==============================
# 1. LOAD CSV FILES
# ==============================

print("\nLoading CSV files...")

food = pd.read_csv(
    "data/food.csv",
    low_memory=False
)

# Convert publication_date into MySQL DATE format
food["publication_date"] = pd.to_datetime(
    food["publication_date"],
    errors="coerce"
).dt.strftime("%Y-%m-%d")


food_nutrient = pd.read_csv(
    "data/food_nutrient.csv",
    low_memory=False
)

nutrient = pd.read_csv(
    "data/nutrient.csv",
    low_memory=False
)

rules = pd.read_csv(
    "data/disease_food_rules.csv",
    low_memory=False
)


print("\nCSV files loaded successfully.")

print("Food rows:", len(food))
print("Food nutrient rows:", len(food_nutrient))
print("Nutrient rows:", len(nutrient))
print("Disease rules:", len(rules))


# ==============================
# 2. SHOW COLUMN NAMES
# ==============================

print("\nFood columns:")
print(food.columns.tolist())

print("\nFood nutrient columns:")
print(food_nutrient.columns.tolist())

print("\nNutrient columns:")
print(nutrient.columns.tolist())

print("\nDisease rules columns:")
print(rules.columns.tolist())


# ==============================
# 3. UPLOAD FOOD
# ==============================

print("\nUploading Food data...")

food.to_sql(
    "food",
    engine,
    if_exists="append",
    index=False,
    chunksize=1000
)

print("Food data uploaded successfully.")


# ==============================
# 4. UPLOAD NUTRIENT
# ==============================

print("\nUploading Nutrient data...")

nutrient.to_sql(
    "nutrient",
    engine,
    if_exists="append",
    index=False,
    chunksize=100
)

print("Nutrient data uploaded successfully.")


# ==============================
# 5. UPLOAD FOOD NUTRIENT
# ==============================

print("\nUploading Food Nutrient data...")

food_nutrient.to_sql(
    "food_nutrient",
    engine,
    if_exists="append",
    index=False,
    chunksize=1000
)

print("Food nutrient data uploaded successfully.")


# ==============================
# 6. UPLOAD DISEASE RULES
# ==============================

print("\nUploading Disease Rules...")

rules.to_sql(
    "disease_food_rules",
    engine,
    if_exists="append",
    index=False,
    chunksize=100
)

print("Disease rules uploaded successfully.")


print("\n")
print("======================================")
print("   ALL DATA UPLOADED SUCCESSFULLY")
print("======================================")