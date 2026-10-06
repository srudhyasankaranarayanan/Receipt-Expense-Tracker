import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from ocr import extract_text
from expense_parser import parse_expenses
from database import create_table, add_expense, get_expenses


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Smart Receipt & Grocery Expense Tracker",
    page_icon="🧾",
    layout="wide"
)


# --------------------------------------------------
# CREATE DATABASE TABLE
# --------------------------------------------------

create_table()


# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title("🧾 Smart Receipt & Grocery Expense Tracker")

st.write(
    "Upload a printed receipt or handwritten grocery paper "
    "to extract and analyze your expenses."
)


# --------------------------------------------------
# IMAGE UPLOAD
# --------------------------------------------------

uploaded_file = st.file_uploader(
    "Upload Receipt / Handwritten Grocery Paper",
    type=["jpg", "jpeg", "png"]
)


# --------------------------------------------------
# OCR PROCESSING
# --------------------------------------------------

if uploaded_file is not None:

    st.subheader("📷 Uploaded Image")

    image = st.image(
        uploaded_file,
        caption="Uploaded Image",
        use_container_width=True
    )


    # Read image
    from PIL import Image

    input_image = Image.open(uploaded_file)


    # --------------------------------------------------
    # EXTRACT TEXT BUTTON
    # --------------------------------------------------

    if st.button("🔍 Extract Text"):

        with st.spinner("Reading image using OCR..."):

            extracted_text = extract_text(input_image)


        st.subheader("📝 Extracted Text")

        if extracted_text:

            st.text_area(
                "OCR Result",
                extracted_text,
                height=200
            )

        else:

            st.warning(
                "No text detected. Try a clearer image."
            )


        # --------------------------------------------------
        # EXPENSE PARSING
        # --------------------------------------------------

        df = parse_expenses(extracted_text)


        if not df.empty:

            st.subheader("💰 Detected Expenses")

            st.dataframe(
                df,
                use_container_width=True
            )


            # --------------------------------------------------
            # CALCULATIONS
            # --------------------------------------------------

            total = df["Price"].sum()

            average = df["Price"].mean()

            item_count = len(df)


            col1, col2, col3 = st.columns(3)


            with col1:
                st.metric(
                    "💰 Total Expense",
                    f"₹{total:.2f}"
                )


            with col2:
                st.metric(
                    "📦 Number of Items",
                    item_count
                )


            with col3:
                st.metric(
                    "📊 Average Price",
                    f"₹{average:.2f}"
                )


            # --------------------------------------------------
            # SAVE TO DATABASE
            # --------------------------------------------------

            if st.button("💾 Save Expenses"):

                for _, row in df.iterrows():

                    add_expense(
                        row["Item"],
                        row["Price"]
                    )

                st.success(
                    "Expenses saved successfully!"
                )


            # --------------------------------------------------
            # EXPENSE CHART
            # --------------------------------------------------

            st.subheader("📊 Expense Chart")

            fig, ax = plt.subplots()

            ax.bar(
                df["Item"],
                df["Price"]
            )

            ax.set_xlabel("Item")

            ax.set_ylabel("Price")

            ax.set_title("Item-wise Expenses")

            plt.xticks(rotation=45)

            st.pyplot(fig)


        else:

            st.warning(
                "Could not identify item-price pairs."
            )


# --------------------------------------------------
# EXPENSE HISTORY
# --------------------------------------------------

st.divider()

st.subheader("📜 Expense History")


history = get_expenses()


if history:

    history_df = pd.DataFrame(
        history,
        columns=[
            "ID",
            "Item",
            "Price",
            "Date"
        ]
    )

    st.dataframe(
        history_df,
        use_container_width=True
    )

else:

    st.info(
        "No expenses have been saved yet."
    )