import sys
import os
import pandas as pd
import streamlit as st
from sqlalchemy import text

# -------------------------------------------------
# CONNECT TO EXISTING SMARTNUTRI DATABASE
# -------------------------------------------------

SRC_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "src")
)

sys.path.append(SRC_PATH)

from database import get_database_connection


# -------------------------------------------------
# PAGE CONFIGURATION
# -------------------------------------------------

st.set_page_config(
    page_title="SMARTNUTRI Admin Panel",
    page_icon="🥗",
    layout="wide"
)


# -------------------------------------------------
# TITLE
# -------------------------------------------------

st.title("🥗 SMARTNUTRI SYSTEM")
st.subheader("Admin Panel - Disease Food Rule Management")

st.write(
    "Use this panel to add, edit, delete and view disease food rules."
)


# -------------------------------------------------
# DATABASE CONNECTION
# -------------------------------------------------

try:
    engine = get_database_connection()

    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))

    st.success("MySQL Database Connected Successfully!")

except Exception as e:
    st.error("Database connection failed.")
    st.code(str(e))
    st.stop()


# -------------------------------------------------
# LOAD RULES
# -------------------------------------------------

def load_rules():

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
        ORDER BY rule_id
    """

    with engine.connect() as connection:
        return pd.read_sql(text(query), connection)


# -------------------------------------------------
# INSERT RULE
# -------------------------------------------------

def add_rule(
    disease,
    age_group,
    food_category,
    food_name,
    recommendation,
    priority,
    reason
):

    query = text("""
        INSERT INTO disease_food_rules
        (
            disease,
            age_group,
            food_category,
            food_name,
            recommendation,
            priority,
            reason
        )
        VALUES
        (
            :disease,
            :age_group,
            :food_category,
            :food_name,
            :recommendation,
            :priority,
            :reason
        )
    """)

    with engine.begin() as connection:

        connection.execute(
            query,
            {
                "disease": disease,
                "age_group": age_group,
                "food_category": food_category,
                "food_name": food_name,
                "recommendation": recommendation,
                "priority": priority,
                "reason": reason
            }
        )


# -------------------------------------------------
# UPDATE RULE
# -------------------------------------------------

def update_rule(
    rule_id,
    disease,
    age_group,
    food_category,
    food_name,
    recommendation,
    priority,
    reason
):

    query = text("""
        UPDATE disease_food_rules
        SET
            disease = :disease,
            age_group = :age_group,
            food_category = :food_category,
            food_name = :food_name,
            recommendation = :recommendation,
            priority = :priority,
            reason = :reason
        WHERE rule_id = :rule_id
    """)

    with engine.begin() as connection:

        connection.execute(
            query,
            {
                "rule_id": rule_id,
                "disease": disease,
                "age_group": age_group,
                "food_category": food_category,
                "food_name": food_name,
                "recommendation": recommendation,
                "priority": priority,
                "reason": reason
            }
        )


# -------------------------------------------------
# DELETE RULE
# -------------------------------------------------

def delete_rule(rule_id):

    query = text("""
        DELETE FROM disease_food_rules
        WHERE rule_id = :rule_id
    """)

    with engine.begin() as connection:

        connection.execute(
            query,
            {
                "rule_id": rule_id
            }
        )


# -------------------------------------------------
# TABS
# -------------------------------------------------

tab1, tab2, tab3, tab4 = st.tabs(
    [
        "➕ Add Rule",
        "✏️ Edit Rule",
        "🗑️ Delete Rule",
        "📋 View Rules"
    ]
)


# =================================================
# TAB 1 - ADD RULE
# =================================================

with tab1:

    st.header("Add New Disease Food Rule")

    with st.form("add_rule_form"):

        disease = st.text_input(
            "Disease / Health Condition"
        )

        age_group = st.selectbox(
            "Age Group",
            [
                "16-25",
                "26-40",
                "41-50",
                "51+"
            ]
        )

        food_category = st.text_input(
            "Food Category"
        )

        food_name = st.text_input(
            "Food Name"
        )

        recommendation = st.selectbox(
            "Recommendation",
            [
                "Recommended",
                "Moderate",
                "Avoid"
            ]
        )

        priority = st.selectbox(
            "Priority",
            [
                "High",
                "Medium",
                "Low"
            ]
        )

        reason = st.text_area(
            "Reason"
        )

        add_button = st.form_submit_button(
            "Add Rule"
        )

        if add_button:

            if (
                disease.strip() == ""
                or food_category.strip() == ""
                or food_name.strip() == ""
                or reason.strip() == ""
            ):

                st.warning(
                    "Please fill all required fields."
                )

            else:

                try:

                    add_rule(
                        disease.strip(),
                        age_group,
                        food_category.strip(),
                        food_name.strip(),
                        recommendation,
                        priority,
                        reason.strip()
                    )

                    st.success(
                        "New disease food rule added successfully!"
                    )

                    st.rerun()

                except Exception as e:

                    st.error(
                        "Unable to add rule."
                    )

                    st.code(str(e))


# =================================================
# TAB 2 - EDIT RULE
# =================================================

with tab2:

    st.header("Edit Existing Disease Food Rule")

    rules = load_rules()

    if rules.empty:

        st.info("No rules available.")

    else:

        rule_ids = rules["rule_id"].tolist()

        selected_id = st.selectbox(
            "Select Rule ID",
            rule_ids
        )

        selected_rule = rules[
            rules["rule_id"] == selected_id
        ].iloc[0]

        with st.form("edit_rule_form"):

            disease = st.text_input(
                "Disease / Health Condition",
                value=str(
                    selected_rule["disease"]
                )
            )

            age_group = st.selectbox(
                "Age Group",
                [
                    "16-25",
                    "26-40",
                    "41-50",
                    "51+"
                ],
                index=[
                    "16-25",
                    "26-40",
                    "41-50",
                    "51+"
                ].index(
                    str(selected_rule["age_group"])
                )
                if str(selected_rule["age_group"])
                in [
                    "16-25",
                    "26-40",
                    "41-50",
                    "51+"
                ]
                else 0
            )

            food_category = st.text_input(
                "Food Category",
                value=str(
                    selected_rule["food_category"]
                )
            )

            food_name = st.text_input(
                "Food Name",
                value=str(
                    selected_rule["food_name"]
                )
            )

            recommendation_options = [
                "Recommended",
                "Moderate",
                "Avoid"
            ]

            current_recommendation = str(
                selected_rule["recommendation"]
            )

            recommendation = st.selectbox(
                "Recommendation",
                recommendation_options,
                index=(
                    recommendation_options.index(
                        current_recommendation
                    )
                    if current_recommendation
                    in recommendation_options
                    else 0
                )
            )

            priority_options = [
                "High",
                "Medium",
                "Low"
            ]

            current_priority = str(
                selected_rule["priority"]
            )

            priority = st.selectbox(
                "Priority",
                priority_options,
                index=(
                    priority_options.index(
                        current_priority
                    )
                    if current_priority
                    in priority_options
                    else 0
                )
            )

            reason = st.text_area(
                "Reason",
                value=str(
                    selected_rule["reason"]
                )
            )

            update_button = st.form_submit_button(
                "Update Rule"
            )

            if update_button:

                try:

                    update_rule(
                        selected_id,
                        disease.strip(),
                        age_group,
                        food_category.strip(),
                        food_name.strip(),
                        recommendation,
                        priority,
                        reason.strip()
                    )

                    st.success(
                        "Rule updated successfully!"
                    )

                    st.rerun()

                except Exception as e:

                    st.error(
                        "Unable to update rule."
                    )

                    st.code(str(e))


# =================================================
# TAB 3 - DELETE RULE
# =================================================

with tab3:

    st.header("Delete Disease Food Rule")

    rules = load_rules()

    if rules.empty:

        st.info("No rules available.")

    else:

        selected_delete_id = st.selectbox(
            "Select Rule ID to Delete",
            rules["rule_id"].tolist()
        )

        selected_delete_rule = rules[
            rules["rule_id"] == selected_delete_id
        ].iloc[0]

        st.warning(
            "You are about to delete this rule:"
        )

        st.write(
            "Disease:",
            selected_delete_rule["disease"]
        )

        st.write(
            "Food:",
            selected_delete_rule["food_name"]
        )

        st.write(
            "Recommendation:",
            selected_delete_rule["recommendation"]
        )

        confirm_delete = st.checkbox(
            "I confirm that I want to delete this rule."
        )

        if st.button(
            "Delete Rule",
            type="primary"
        ):

            if not confirm_delete:

                st.warning(
                    "Please confirm deletion first."
                )

            else:

                try:

                    delete_rule(
                        selected_delete_id
                    )

                    st.success(
                        "Rule deleted successfully!"
                    )

                    st.rerun()

                except Exception as e:

                    st.error(
                        "Unable to delete rule."
                    )

                    st.code(str(e))


# =================================================
# TAB 4 - VIEW RULES
# =================================================

with tab4:

    st.header("All Disease Food Rules")

    rules = load_rules()

    if rules.empty:

        st.info("No disease food rules available.")

    else:

        st.metric(
            "Total Disease Food Rules",
            len(rules)
        )

        st.dataframe(
            rules,
            use_container_width=True,
            hide_index=True
        )