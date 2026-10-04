# SMARTNUTRI SYSTEM

## AI Based Age & Disease Food Recommendation Dashboard

SMARTNUTRI SYSTEM is a data-driven food recommendation project that uses real USDA food and nutrient data to generate food recommendations based on user age, health condition, food preference, weight and height.

The project combines Python, MySQL, AI/ML-based recommendation logic and Power BI to create an end-to-end food recommendation and analytics system.

## Technologies Used

- Python
- Pandas
- MySQL
- SQL
- Power BI
- AI/ML Recommendation
- Streamlit
- USDA FoodData Central data

## Project Workflow

User Details
        ↓
Disease & Food Rules
        ↓
Python Data Processing
        ↓
AI Recommendation Engine
        ↓
MySQL Database
        ↓
Power BI Dashboard

## Main Features

- Age-based food recommendation
- Disease-based food recommendation
- Food preference filtering
- BMI calculation
- Recommended food identification
- Moderate food classification
- Avoid food identification
- Priority-based recommendation
- AI scoring
- Real USDA food and nutrient data
- MySQL database integration
- Streamlit Admin Panel
- Add, Edit, Delete and View disease-food rules
- Power BI dashboard
- Dynamic recommendation update workflow

## Real Dataset

The project uses real USDA food and nutrient data.

### Dataset Information

- Food records: 87,990
- Food nutrient records: 170,469
- Nutrient records: 477

### Disease Rules

Current disease categories:

- Anemia
- Diabetes
- High Cholesterol
- Hypertension
- Obesity

Total disease-food rules: 97

## Database

MySQL database name:

`smartnutri`

Main tables:

- `food`
- `food_nutrient`
- `nutrient`
- `disease_food_rules`
- `smartnutri_recommendations`

## Admin Panel

The Streamlit Admin Panel provides:

- View existing rules
- Add new rules
- Edit existing rules
- Delete rules

Disease and food rules are stored in MySQL so that the recommendation system can use updated rule data.

## AI Recommendation

The Python recommendation engine:

1. Accepts user details.
2. Determines the user's age group.
3. Calculates BMI.
4. Loads disease rules from MySQL.
5. Searches real USDA food records.
6. Applies food preference filtering.
7. Generates Recommended and Moderate foods.
8. Identifies Avoid foods.
9. Calculates an AI recommendation score.
10. Saves the final recommendation results.

## Power BI Dashboard

The Power BI dashboard provides:

- Total Foods
- Total Diseases
- Total Food Rules
- Disease filtering
- Age Group filtering
- Disease-wise recommendation analysis
- Age Group analysis
- Recommendation distribution
- Food recommendation details

## Future Update Workflow

The system is designed for future data updates:

Admin Panel
→ MySQL Disease Rules
→ Python AI Recommendation Engine
→ Recommendation Results
→ MySQL Recommendation Table
→ Power BI Refresh

This allows validated new disease-food rules to be added without changing the core recommendation code.

## Project Structure

```text
SmartNutri_Project
│
├── README.md
├── smartnutri dashboard.pbix
├── smartnutri.sql
│
├── admin
│   └── admin_app.py
│
├── data
│   ├── disease_food_rules.csv
│   ├── food.csv
│   ├── food_nutrient.csv
│   └── nutrient.csv
│
├── database
├── models
│
├── output
│   ├── smartnutri_ai_results.csv
│   └── smartnutri_recommendations.csv
│
└── src
    ├── check_food_names.py
    ├── create_recommendation_csv.py
    ├── database.py
    ├── data_cleaning.py
    ├── data_loader.py
    ├── feature_engineering.py
    ├── load_recommendation.py
    ├── recommendation_engine.py
    ├── smartnutri_ai.py
    ├── test_setup.py
    └── upload_data.py