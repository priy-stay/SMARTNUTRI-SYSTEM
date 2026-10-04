import re
import pandas as pd

from feature_engineering import create_food_nutrient_dataset


# ==========================================
# AGE GROUP
# ==========================================

def get_age_group(age):

    if age < 16:
        return "Below 16"

    elif age <= 25:
        return "16-25"

    elif age <= 40:
        return "26-40"

    elif age <= 50:
        return "41-50"

    else:
        return "51+"


# ==========================================
# BMI
# ==========================================

def calculate_bmi(weight, height):

    if height is None or height <= 0:
        return 0

    height_m = height / 100

    return round(
        weight / (height_m ** 2),
        2
    )


def get_bmi_category(bmi):

    if bmi < 18.5:
        return "Underweight"

    elif bmi < 25:
        return "Normal"

    elif bmi < 30:
        return "Overweight"

    else:
        return "Obesity"


# ==========================================
# CLEAN TEXT
# ==========================================

def clean_text(value):

    if value is None:
        return ""

    return (
        str(value)
        .strip()
        .lower()
    )


# ==========================================
# FOOD PREFERENCE
# ==========================================

def apply_food_preference(
    food_data,
    food_preference
):

    if food_data.empty:
        return food_data

    preference = clean_text(
        food_preference
    )

    if preference in ["", "any"]:
        return food_data

    result = food_data.copy()

    if "description" not in result.columns:
        return result

    description = (
        result["description"]
        .astype(str)
        .str.lower()
    )

    # ======================================
    # VEGAN
    # ======================================

    if preference == "vegan":

        result = result[
            ~description.str.contains(
                r"\bmeat\b|fish|chicken|beef|pork|seafood|egg|milk|dairy|cheese|yogurt",
                case=False,
                na=False,
                regex=True
            )
        ].copy()

    # ======================================
    # VEGETARIAN
    # ======================================

    elif preference == "vegetarian":

        result = result[
            ~description.str.contains(
                r"\bmeat\b|fish|chicken|beef|pork|seafood",
                case=False,
                na=False,
                regex=True
            )
        ].copy()

    # ======================================
    # NON-VEGETARIAN
    # ======================================

    elif preference == "non-vegetarian":

        result = result.copy()

    return result


# ==========================================
# REMOVE USDA ANALYTICAL RECORDS
# ==========================================

def remove_invalid_usda_records(food_data):

    if food_data.empty:
        return food_data

    if "description" not in food_data.columns:
        return food_data

    result = food_data.copy()

    descriptions_lower = (
        result["description"]
        .astype(str)
        .str.strip()
        .str.lower()
    )

    invalid_prefixes = (
        "moisture",
        "vitamin ",
        "minerals",
        "mineral ",
        "proximates",
        "carotenoids",
        "fiber",
        "sugar",
        "fatty acids",
        "amino acids",
        "protein",
        "energy",
        "cholesterol",
        "thiamin",
        "riboflavin",
        "niacin",
        "folate",
        "calcium",
        "iron",
        "sodium",
        "potassium",
        "magnesium",
        "zinc"
    )

    result = result[
        ~descriptions_lower.str.startswith(
            invalid_prefixes
        )
    ].copy()

    return result


# ==========================================
# NORMALIZE FOOD NAME
# ==========================================

def normalize_food_name(value):

    value = clean_text(value)

    value = re.sub(
        r"[^a-z0-9\s]",
        " ",
        value
    )

    value = re.sub(
        r"\s+",
        " ",
        value
    )

    return value.strip()


# ==========================================
# BUILD FOOD SEARCH TERMS
# ==========================================

def get_food_search_terms(rule_food):

    rule_food_clean = normalize_food_name(
        rule_food
    )

    if not rule_food_clean:
        return []

    aliases = {

        "green gram": [
            "green gram",
            "mung bean",
            "mung beans",
            "moong bean",
            "moong beans"
        ],

        "mung beans": [
            "mung bean",
            "mung beans",
            "green gram",
            "moong bean",
            "moong beans"
        ],

        "spinach": [
            "spinach"
        ],

        "lentils": [
            "lentil",
            "lentils"
        ],

        "chickpeas": [
            "chickpea",
            "chickpeas",
            "garbanzo bean",
            "garbanzo beans"
        ],

        "broccoli": [
            "broccoli"
        ],

        "barley": [
            "barley"
        ],

        "oats": [
            "oat",
            "oats"
        ],

        "bitter gourd": [
            "bitter gourd",
            "bitter melon"
        ],

        "pumpkin seeds": [
            "pumpkin seed",
            "pumpkin seeds"
        ],

        "almonds": [
            "almond",
            "almonds"
        ],

        "walnuts": [
            "walnut",
            "walnuts"
        ],

        "banana": [
            "banana",
            "bananas"
        ],

        "guava": [
            "guava",
            "guavas"
        ],

        "orange": [
            "orange",
            "oranges"
        ],

        "cucumber": [
            "cucumber",
            "cucumbers"
        ],

        "cabbage": [
            "cabbage",
            "cabbages"
        ],

        "amaranth leaves": [
            "amaranth leaves",
            "amaranth"
        ],

        "sesame seeds": [
            "sesame seed",
            "sesame seeds",
            "sesame"
        ],

        "eggs": [
            "egg",
            "eggs"
        ]
    }

    return aliases.get(
        rule_food_clean,
        [rule_food_clean]
    )


# ==========================================
# USDA FOOD MATCHING
# ==========================================

def find_usda_foods(
    food_data,
    rule_food
):

    if food_data.empty:
        return pd.DataFrame()

    if "description" not in food_data.columns:
        return pd.DataFrame()

    valid_food = remove_invalid_usda_records(
        food_data
    )

    if valid_food.empty:
        return pd.DataFrame()

    search_terms = get_food_search_terms(
        rule_food
    )

    if not search_terms:
        return pd.DataFrame()

    descriptions = (
        valid_food["description"]
        .astype(str)
        .str.strip()
    )

    descriptions_lower = (
        descriptions
        .str.lower()
    )

    matched_parts = []

    # ======================================
    # PREFIX SEARCH
    # ======================================

    for term in search_terms:

        term = normalize_food_name(term)

        if not term:
            continue

        escaped_term = re.escape(term)

        temp = valid_food[
            descriptions_lower.str.startswith(
                escaped_term,
                na=False
            )
        ].copy()

        if not temp.empty:
            matched_parts.append(temp)

    # ======================================
    # COMBINE PREFIX RESULTS
    # ======================================

    if matched_parts:

        matched = pd.concat(
            matched_parts,
            ignore_index=True
        )

    else:

        matched = pd.DataFrame()

    # ======================================
    # FALLBACK CONTAINS SEARCH
    # ======================================

    if matched.empty:

        for term in search_terms:

            term = normalize_food_name(term)

            if not term:
                continue

            escaped_term = re.escape(term)

            temp = valid_food[
                descriptions_lower.str.contains(
                    escaped_term,
                    case=False,
                    na=False,
                    regex=True
                )
            ].copy()

            if not temp.empty:
                matched_parts.append(temp)

        if matched_parts:

            matched = pd.concat(
                matched_parts,
                ignore_index=True
            )

    # ======================================
    # NO REAL USDA MATCH
    # ======================================

    if matched.empty:

        print(
            f"USDA match not found: {rule_food}"
        )

        return pd.DataFrame()

    # ======================================
    # OATS CLEANING
    # ======================================

    rule_food_clean = normalize_food_name(
        rule_food
    )

    if (
        rule_food_clean == "oats"
        and not matched.empty
    ):

        oats_description = (
            matched["description"]
            .astype(str)
            .str.lower()
        )

        matched = matched[
            ~oats_description.str.contains(
                "cookie|cookies|biscuit|cake|muffin|bar",
                case=False,
                na=False,
                regex=True
            )
        ].copy()

    # ======================================
    # BROCCOLI CLEANING
    # ======================================

    if (
        rule_food_clean == "broccoli"
        and not matched.empty
    ):

        broccoli_description = (
            matched["description"]
            .astype(str)
            .str.strip()
        )

        strict_match = broccoli_description.str.startswith(
            (
                "Broccoli, raw",
                "Broccoli, cooked"
            ),
            na=False
        )

        if strict_match.any():

            matched = matched[
                strict_match
            ].copy()

    # ======================================
    # REMOVE DUPLICATES
    # ======================================

    if not matched.empty:

        if "fdc_id" in matched.columns:

            matched = (
                matched
                .drop_duplicates(
                    subset=["fdc_id"]
                )
                .copy()
            )

        else:

            matched = (
                matched
                .drop_duplicates()
                .copy()
            )

    # ======================================
    # LIMIT RECORDS
    # ======================================

    if rule_food_clean == "broccoli":

        matched = matched.head(3)

    else:

        matched = matched.head(5)

    return matched


# ==========================================
# CREATE RECOMMENDATIONS
# ==========================================

def create_recommendations(
    age,
    disease,
    food,
    food_nutrient,
    nutrient,
    rules,
    weight=None,
    height=None,
    gender=None,
    food_preference=None
):

    age_group = get_age_group(age)

    if age_group == "Below 16":
        return pd.DataFrame()

    required_columns = [
        "disease",
        "age_group",
        "food_name",
        "recommendation",
        "food_category",
        "priority",
        "reason"
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in rules.columns
    ]

    if missing_columns:

        print(
            "\nMissing rule columns:",
            missing_columns
        )

        return pd.DataFrame()

    disease_clean = clean_text(disease)

    disease_rules = rules[
        (
            rules["disease"]
            .astype(str)
            .str.lower()
            .str.strip()
            == disease_clean
        )
        &
        (
            rules["age_group"]
            .astype(str)
            .str.strip()
            == age_group
        )
    ].copy()

    if disease_rules.empty:

        print(
            "\nNo rules available for:",
            disease,
            age_group
        )

        return pd.DataFrame()

    # ======================================
    # RECOMMENDED + MODERATE
    # ======================================

    positive_rules = disease_rules[
        disease_rules["recommendation"]
        .astype(str)
        .str.lower()
        .str.strip()
        .isin([
            "recommended",
            "moderate"
        ])
    ].copy()

    if positive_rules.empty:
        return pd.DataFrame()

    # ======================================
    # FOOD PREFERENCE
    # ======================================

    filtered_food = apply_food_preference(
        food,
        food_preference
    )

    if filtered_food.empty:

        print(
            "\nNo foods remain after food preference filter."
        )

        return pd.DataFrame()

    # ======================================
    # NUTRIENT DATASET
    # ======================================

    food_nutrient_data = (
        create_food_nutrient_dataset(
            food,
            food_nutrient,
            nutrient
        )
    )

    if food_nutrient_data.empty:
        return pd.DataFrame()

    results = []

    # ======================================
    # PROCESS RULES
    # ======================================

    for _, rule in positive_rules.iterrows():

        rule_food = rule["food_name"]

        matched_foods = find_usda_foods(
            filtered_food,
            rule_food
        )

        if matched_foods.empty:
            continue

        nutrition_rows = (
            food_nutrient_data[
                food_nutrient_data["fdc_id"].isin(
                    matched_foods["fdc_id"]
                )
            ].copy()
        )

        if nutrition_rows.empty:
            continue

        # ==================================
        # NUMERIC AMOUNT
        # ==================================

        if "amount" in nutrition_rows.columns:

            nutrition_rows["amount"] = pd.to_numeric(
                nutrition_rows["amount"],
                errors="coerce"
            )

            nutrition_rows = (
                nutrition_rows
                .groupby(
                    [
                        "fdc_id",
                        "description"
                    ],
                    as_index=False
                )
                .agg(
                    amount=("amount", "mean")
                )
            )

        else:

            nutrition_rows = (
                nutrition_rows
                .drop_duplicates(
                    subset=[
                        "fdc_id",
                        "description"
                    ]
                )
            )

        # ==================================
        # ONE RECORD PER FOOD
        # ==================================

        nutrition_rows["food_base_name"] = (
            nutrition_rows["description"]
            .astype(str)
            .str.lower()
            .str.strip()
        )

        nutrition_rows = (
            nutrition_rows
            .drop_duplicates(
                subset=["food_base_name"]
            )
            .copy()
        )

        nutrition_rows.drop(
            columns=["food_base_name"],
            inplace=True,
            errors="ignore"
        )

        # ==================================
        # RULE INFORMATION
        # ==================================

        nutrition_rows["disease"] = (
            rule["disease"]
        )

        nutrition_rows["age_group"] = (
            age_group
        )

        nutrition_rows["rule_food"] = (
            rule["food_name"]
        )

        nutrition_rows["food_category"] = (
            rule["food_category"]
        )

        nutrition_rows["recommendation"] = (
            rule["recommendation"]
        )

        nutrition_rows["priority"] = (
            rule["priority"]
        )

        nutrition_rows["reason"] = (
            rule["reason"]
        )

        # ==================================
        # USER INFORMATION
        # ==================================

        nutrition_rows["user_age"] = age
        nutrition_rows["gender"] = gender
        nutrition_rows["weight_kg"] = weight
        nutrition_rows["height_cm"] = height
        nutrition_rows["food_preference"] = (
            food_preference
        )

        # ==================================
        # BMI
        # ==================================

        if (
            weight is not None
            and height is not None
        ):

            bmi = calculate_bmi(
                weight,
                height
            )

            nutrition_rows["BMI"] = bmi

            nutrition_rows["BMI_category"] = (
                get_bmi_category(bmi)
            )

        results.append(
            nutrition_rows
        )

    # ======================================
    # NO RESULTS
    # ======================================

    if not results:
        return pd.DataFrame()

    # ======================================
    # COMBINE
    # ======================================

    final_result = pd.concat(
        results,
        ignore_index=True
    )

    # ======================================
    # REMOVE DUPLICATES
    # ======================================

    final_result = (
        final_result
        .drop_duplicates(
            subset=[
                "fdc_id",
                "disease",
                "age_group",
                "rule_food"
            ]
        )
        .copy()
    )

    return final_result


# ==========================================
# GET AVOID FOODS
# ==========================================

def get_avoid_foods(
    age,
    disease,
    rules
):

    age_group = get_age_group(age)

    # ======================================
    # EMPTY RULE DATA
    # ======================================

    if rules is None or rules.empty:

        return pd.DataFrame(
            columns=[
                "food_name",
                "food_category",
                "recommendation",
                "priority",
                "reason"
            ]
        )

    # ======================================
    # REQUIRED COLUMNS CHECK
    # ======================================

    required_columns = [
        "disease",
        "age_group",
        "food_name",
        "food_category",
        "recommendation",
        "priority",
        "reason"
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in rules.columns
    ]

    if missing_columns:

        print(
            "\nMissing avoid-rule columns:",
            missing_columns
        )

        return pd.DataFrame(
            columns=required_columns[2:]
        )

    # ======================================
    # CLEAN VALUES
    # ======================================

    temp_rules = rules.copy()

    temp_rules["_disease_clean"] = (
        temp_rules["disease"]
        .astype(str)
        .str.strip()
        .str.lower()
    )

    temp_rules["_age_group_clean"] = (
        temp_rules["age_group"]
        .astype(str)
        .str.strip()
    )

    temp_rules["_recommendation_clean"] = (
        temp_rules["recommendation"]
        .astype(str)
        .str.strip()
        .str.lower()
    )

    # ======================================
    # FILTER DISEASE + AGE + AVOID
    # ======================================

    filtered = temp_rules[
        (
            temp_rules["_disease_clean"]
            == clean_text(disease)
        )
        &
        (
            temp_rules["_age_group_clean"]
            == age_group
        )
        &
        (
            temp_rules["_recommendation_clean"]
            == "avoid"
        )
    ].copy()


    filtered.drop(
        columns=[
            "_disease_clean",
            "_age_group_clean",
            "_recommendation_clean"
        ],
        inplace=True,
        errors="ignore"
    )

    if filtered.empty:
        return pd.DataFrame(
            columns=[
                "food_name",
                "food_category",
                "recommendation",
                "priority",
                "reason"
            
            ]
        )
    return(
        filtered[
            [
                "food_name",
                "food_category",
                "recommendation",
                "priority",
                "reason"
            ]
        ]
        .drop_duplicates()
        .reset_index(drop=True)
    )