import pandas as pd

print("Loading USDA Food Data...")

food = pd.read_csv(
    "data/food.csv",
    low_memory=False
)

print("\n========== LEGUMES / BEANS ==========")

keywords = (
    r"lentil|bean|chickpea|garbanzo|"
    r"mung|moong|green gram|"
    r"split pea|pea"
)

legumes = food[
    food["description"].astype(str).str.contains(
        keywords,
        case=False,
        na=False,
        regex=True
    )
]

# Remove nutrient-related records
legumes = legumes[
    ~legumes["description"].astype(str).str.match(
        r"^(Moisture|Vitamin|Protein|Fat|Carbohydrate|"
        r"Fiber|Calcium|Iron|Sodium|Potassium|"
        r"Magnesium|Zinc|Folate|Niacin|Thiamin|"
        r"Energy|Cholesterol|Sugars)",
        case=False,
        na=False
    )
]

print(
    legumes[
        ["fdc_id", "description"]
    ]
    .head(50)
    .to_string(index=False)
)

print("\nTotal matching records:", len(legumes))

print("\n========== CHECK COMPLETED ==========")