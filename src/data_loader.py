import pandas as pd

from database import get_database_connection


# ==========================================
# LOAD FOOD DATA
# ==========================================

def load_food_data():

    food = pd.read_csv(
        "data/food.csv",
        low_memory=False
    )

    return food


# ==========================================
# LOAD FOOD NUTRIENT DATA
# ==========================================

def load_food_nutrient_data():

    food_nutrient = pd.read_csv(
        "data/food_nutrient.csv",
        low_memory=False
    )

    return food_nutrient


# ==========================================
# LOAD NUTRIENT DATA
# ==========================================

def load_nutrient_data():

    nutrient = pd.read_csv(
        "data/nutrient.csv",
        low_memory=False
    )

    return nutrient


# ==========================================
# LOAD DISEASE FOOD RULES FROM MYSQL
# ==========================================

def load_disease_rules():

    engine = get_database_connection()

    query = """
        SELECT
            rule_id,
            disease,
            age_group,
            food_category,
            food_name,
            recommendation,
            priority,
            reason
        FROM disease_food_rules
    """

    rules = pd.read_sql(
        query,
        engine
    )

    return rules


# ==========================================
# TEST DATA LOADING
# ==========================================

if __name__ == "__main__":

    print("Loading SmartNutri data...")

    food = load_food_data()

    food_nutrient = load_food_nutrient_data()

    nutrient = load_nutrient_data()

    rules = load_disease_rules()

    print("\n===================================")
    print("SMARTNUTRI DATA LOADING SUCCESS")
    print("===================================")

    print("Food rows:", len(food))

    print(
        "Food nutrient rows:",
        len(food_nutrient)
    )

    print(
        "Nutrient rows:",
        len(nutrient)
    )

    print(
        "Disease rules from MySQL:",
        len(rules)
    )

    print("\nAvailable diseases:")

    print(
        rules["disease"]
        .dropna()
        .drop_duplicates()
        .tolist()
    )

    print("\nDisease rule counts:")

    print(
        rules["disease"]
        .value_counts()
    )