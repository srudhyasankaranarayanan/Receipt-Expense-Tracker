import re
import pandas as pd


def clean_price(value):

    value = value.replace(",", "")
    value = value.replace("₹", "")
    value = value.replace("Rs", "")
    value = value.replace("INR", "")

    # Common OCR mistakes
    value = value.replace("O", "0")
    value = value.replace("o", "0")
    value = value.replace("I", "1")
    value = value.replace("l", "1")

    match = re.search(
        r"\d+(?:\.\d{1,2})?",
        value
    )

    if match:
        return float(match.group())

    return None


def parse_expenses(text):

    expenses = []

    lines = text.split("\n")

    for line in lines:

        line = line.strip()

        if not line:
            continue

        # --------------------------------------------------
        # IGNORE HEADER / FOOTER
        # --------------------------------------------------

        lower = line.lower()

        ignored_words = [
            "s.no",
            "item",
            "qty",
            "rate",
            "amount",
            "total",
            "discount",
            "payment",
            "received",
            "thank",
            "receipt",
            "customer",
            "date",
            "address",
            "net amount"
        ]

        if any(
            word in lower
            for word in ignored_words
        ):
            continue

        # --------------------------------------------------
        # FIND NUMBERS
        # --------------------------------------------------

        numbers = re.findall(
            r"\d+(?:\.\d{1,2})?",
            line
        )

        if len(numbers) < 2:
            continue

        # Convert numbers
        numeric_values = []

        for number in numbers:

            try:
                numeric_values.append(
                    float(number)
                )
            except:
                pass

        if len(numeric_values) < 2:
            continue

        # --------------------------------------------------
        # ITEM NAME
        # --------------------------------------------------

        # Remove numbers from line
        item = re.sub(
            r"\d+(?:\.\d{1,2})?",
            "",
            line
        )

        # Remove punctuation
        item = re.sub(
            r"[|:₹]",
            "",
            item
        )

        item = item.strip()

        # Remove common unwanted words
        item = re.sub(
            r"\(.*?\)",
            "",
            item
        )

        item = item.strip()

        # --------------------------------------------------
        # VALID ITEM CHECK
        # --------------------------------------------------

        if len(item) < 2:
            continue

        if item.lower() in [
            "total",
            "discount",
            "cash",
            "amount"
        ]:
            continue

        # --------------------------------------------------
        # PRICE
        # --------------------------------------------------

        price = numeric_values[-1]

        # Ignore very large numbers that may be dates
        if price > 100000:
            continue

        expenses.append({
            "Item": item.title(),
            "Price": price
        })

    return pd.DataFrame(
        expenses,
        columns=["Item", "Price"]
    )