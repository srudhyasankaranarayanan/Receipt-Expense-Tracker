import streamlit as st
from PIL import Image
import pandas as pd

from ocr import extract_text
from expense_parser import extract_expenses
from recipe import find_recipes

from database import (
    create_database,
    add_expense,
    get_expenses,
    get_total_expense,
    delete_expense,
    clear_expenses
)


# ---------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------

st.set_page_config(
    page_title="Receipt Expense Tracker",
    page_icon="🧾",
    layout="wide"
)


# ---------------------------------------------------
# CREATE DATABASE
# ---------------------------------------------------

create_database()


# ---------------------------------------------------
# TITLE
# ---------------------------------------------------

st.title("🧾 Receipt Expense Tracker")

st.write(
    "Upload a receipt to extract expenses using OCR, "
    "analyze your spending, and get recipe suggestions."
)


# ---------------------------------------------------
# RECEIPT UPLOAD
# ---------------------------------------------------

st.subheader("📤 Upload Receipt")

uploaded_file = st.file_uploader(
    "Choose a receipt image",
    type=["jpg", "jpeg", "png"]
)


# ---------------------------------------------------
# PROCESS RECEIPT
# ---------------------------------------------------

if uploaded_file:

    image = Image.open(uploaded_file)

    st.image(
        image,
        caption="Uploaded Receipt",
        use_container_width=True
    )


    # ------------------------------------------------
    # OCR PROCESSING
    # ------------------------------------------------

    if st.button("🔍 Process Receipt"):

        with st.spinner("Reading receipt..."):

            text = extract_text(image)

        st.session_state["ocr_text"] = text

        st.success("✅ Receipt processed successfully!")


# ---------------------------------------------------
# DISPLAY OCR TEXT
# ---------------------------------------------------

if "ocr_text" in st.session_state:

    st.subheader("📝 OCR Extracted Text")

    text = st.session_state["ocr_text"]

    st.text_area(
        "Extracted Text",
        text,
        height=200
    )


    # ------------------------------------------------
    # EXPENSE EXTRACTION
    # ------------------------------------------------

    expenses = extract_expenses(text)


    if expenses:

        st.subheader("💰 Detected Expenses")


        # Convert expenses to DataFrame

        df = pd.DataFrame(expenses)


        # ------------------------------------------------
        # DISPLAY EXPENSE TABLE
        # ------------------------------------------------

        display_df = df.copy()

        display_df["Price"] = display_df["Price"].apply(
            lambda x: f"₹{x:.2f}"
        )

        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True
        )


        # ------------------------------------------------
        # SUMMARY
        # ------------------------------------------------

        total_expense = df["Price"].sum()

        number_of_items = len(df)

        average_price = df["Price"].mean()


        col1, col2, col3 = st.columns(3)


        with col1:

            st.metric(
                "💰 Total Expense",
                f"₹{total_expense:.2f}"
            )


        with col2:

            st.metric(
                "🛒 Number of Items",
                number_of_items
            )


        with col3:

            st.metric(
                "📊 Average Price",
                f"₹{average_price:.2f}"
            )


        # ------------------------------------------------
        # SAVE EXPENSES TO SQLITE
        # ------------------------------------------------

        st.subheader("💾 Save Expenses")

        if st.button("💾 Save Expenses to Database"):

            for _, row in df.iterrows():

                add_expense(
                    row["Item"],
                    row["Price"]
                )

            st.success(
                "✅ Expenses saved successfully!"
            )


        # ------------------------------------------------
        # EXPENSE CHART
        # ------------------------------------------------

        st.subheader("📊 Expense Chart")

        chart_df = df.set_index("Item")

        st.bar_chart(
            chart_df["Price"]
        )


        # ------------------------------------------------
        # RECIPE SUGGESTIONS
        # ------------------------------------------------

        st.subheader("🍳 Recipe Suggestions")

        available_items = df["Item"].tolist()

        suggestions = find_recipes(
            available_items
        )


        if suggestions:

            for recipe in suggestions:

                st.write(
                    f"### 🍽️ {recipe['Recipe']}"
                )

                st.write(
                    f"**Match:** "
                    f"{recipe['Match']:.0f}%"
                )

                st.write(
                    "Available ingredients: "
                    + ", ".join(
                        recipe["Available"]
                    )
                )

                st.divider()

        else:

            st.info(
                "No matching recipes found."
            )


    else:

        st.warning(
            "⚠️ No expenses could be detected "
            "from the receipt."
        )


# ---------------------------------------------------
# EXPENSE HISTORY
# ---------------------------------------------------

st.divider()

st.subheader("📜 Expense History")


saved_expenses = get_expenses()


if saved_expenses:

    history_df = pd.DataFrame(
        saved_expenses,
        columns=[
            "ID",
            "Item",
            "Price",
            "Date"
        ]
    )


    # ------------------------------------------------
    # DISPLAY HISTORY
    # ------------------------------------------------

    display_history = history_df.copy()

    display_history["Price"] = (
        display_history["Price"]
        .apply(lambda x: f"₹{x:.2f}")
    )


    st.dataframe(
        display_history,
        use_container_width=True,
        hide_index=True
    )


    # ------------------------------------------------
    # TOTAL SAVED EXPENSE
    # ------------------------------------------------

    total_saved = get_total_expense()


    st.metric(
        "💰 Total Saved Expenses",
        f"₹{total_saved:.2f}"
    )


    # ------------------------------------------------
    # DELETE ONE EXPENSE
    # ------------------------------------------------

    st.subheader("🗑️ Delete Expense")


    expense_ids = [
        expense[0]
        for expense in saved_expenses
    ]


    selected_id = st.selectbox(
        "Select Expense ID",
        expense_ids
    )


    if st.button("🗑️ Delete Selected Expense"):

        delete_expense(
            selected_id
        )

        st.success(
            "✅ Expense deleted successfully!"
        )

        st.rerun()


    # ------------------------------------------------
    # CLEAR ALL EXPENSES
    # ------------------------------------------------

    st.subheader("⚠️ Clear Expense History")


    if st.button("🗑️ Clear All Expenses"):

        clear_expenses()

        st.success(
            "✅ All expense history cleared!"
        )

        st.rerun()


else:

    st.info(
        "No saved expenses yet. "
        "Upload a receipt and click "
        "'Save Expenses to Database'."
    )