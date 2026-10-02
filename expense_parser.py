import re


def extract_expenses(text):

    expenses = []

    lines = text.split("\n")

    ignored_words = [
        "total",
        "subtotal",
        "grand total",
        "gst",
        "tax",
        "cgst",
        "sgst",
        "discount",
        "amount",
        "cash",
        "change",
        "balance",
        "round off"
    ]

    for line in lines:

        line = line.strip()

        if not line:
            continue

        # Replace multiple spaces with one space
        line = re.sub(r"\s+", " ", line)

        # Find numbers at the end of the line
        match = re.search(
            r"(.+?)\s+(?:₹\s*)?(\d+(?:\.\d{1,2})?)$",
            line
        )

        if not match:
            continue

        item = match.group(1).strip()
        price = float(match.group(2))

        # Remove unwanted symbols
        item = re.sub(
            r"[^A-Za-z0-9\s\-]",
            "",
            item
        ).strip()

        if not item:
            continue

        # Ignore totals and other non-product lines
        item_lower = item.lower()

        if any(
            word in item_lower
            for word in ignored_words
        ):
            continue

        # Avoid invalid prices
        if price <= 0:
            continue

        # Avoid lines that contain only numbers
        if not re.search(r"[A-Za-z]", item):
            continue

        expenses.append({
            "Item": item.title(),
            "Price": price
        })

    return expenses