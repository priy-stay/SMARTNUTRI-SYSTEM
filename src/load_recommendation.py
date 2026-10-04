import pandas as pd
from database import get_database_connection
from sqlalchemy import text

print("==========================================")
print("   SMARTNUTRI RECOMMENDATION UPDATE")
print("==========================================")

file_path = "output/smartnutri_ai_results.csv"

print("\nLoading latest AI recommendation file...")

df = pd.read_csv(file_path)

print("Recommendation rows:", len(df))


# -------------------------------------------------
# REQUIRED COLUMNS
# -------------------------------------------------

required_columns = [
    "disease",
    "age_group",
    "food_category",
    "food_name",
    "recommendation",
    "priority",
    "reason"
]

missing_columns = [
    column
    for column in required_columns
    if column not in df.columns
]

if missing_columns:

    print("\nERROR: Missing columns:")
    print(missing_columns)

    exit()


# -------------------------------------------------
# SELECT REQUIRED COLUMNS
# -------------------------------------------------

upload_df = df[required_columns].copy()


# -------------------------------------------------
# CLEAN DATA
# -------------------------------------------------

upload_df = upload_df.drop_duplicates()

upload_df = upload_df.dropna(
    subset=[
        "disease",
        "food_name",
        "recommendation"
    ]
)

print("Rows ready for MySQL:", len(upload_df))


# -------------------------------------------------
# DATABASE CONNECTION
# -------------------------------------------------

print("\nConnecting to MySQL...")

engine = get_database_connection()

print("MySQL connection successful!")


# -------------------------------------------------
# REMOVE OLD AI RESULTS
# -------------------------------------------------

print("\nRemoving previous recommendation results...")

with engine.begin() as connection:

    connection.execute(
        text(
            "TRUNCATE TABLE smartnutri_recommendations"
        )
    )

print("Previous recommendation results removed.")


# -------------------------------------------------
# UPLOAD LATEST RESULTS
# -------------------------------------------------

print("\nUploading latest AI recommendations...")

upload_df.to_sql(
    "smartnutri_recommendations",
    con=engine,
    if_exists="append",
    index=False,
    chunksize=500
)


print("\n==========================================")
print("   RECOMMENDATION UPDATE COMPLETED")
print("==========================================")

print("Uploaded rows:", len(upload_df))