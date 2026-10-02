# 🧾 Receipt Expense Tracker

A simple **Receipt Expense Tracker** built using **Python, Streamlit, OCR, OpenCV, Pandas, and SQLite**.

This application allows users to upload a receipt image, automatically extract the text and expenses using **OCR**, analyze the spending, store expenses in a **SQLite database**, and suggest recipes based on the detected grocery items.

---

##  Project Overview

Manually entering expenses from receipts can be time-consuming. This project automates the process by using **Optical Character Recognition (OCR)** to read receipt images and identify the purchased items and their prices.

The extracted expenses can then be:

- Viewed in a structured table
- Analyzed using total and average price
- Visualized using a bar chart
- Stored in a SQLite database
- Viewed later through expense history
- Used to generate recipe suggestions

---

##  Project Workflow

```text
Receipt Image
     ↓
Image Preprocessing
     ↓
OCR using Tesseract
     ↓
Extracted Text
     ↓
Expense Parser
     ↓
Item + Price
     ↓
Expense Analysis
     ↓
┌───────────────────┬───────────────────┐
│                   │                   │
↓                   ↓                   ↓
Expense Chart   SQLite Database   Recipe Suggestions
                    ↓
              Expense History
```

---

##  Features

### 🧾 1. Receipt Upload

Users can upload receipt images in:

- JPG
- JPEG
- PNG

### 🔍 2. OCR Text Extraction

The application uses **Tesseract OCR** to extract text from the uploaded receipt.

OpenCV is used for image preprocessing to improve OCR readability.

The preprocessing includes:

- Grayscale conversion
- Image resizing
- Gaussian blur
- Adaptive thresholding

### 💰 3. Expense Extraction

The extracted OCR text is processed using Python and regular expressions.

The application identifies:

```text
Item Name + Price
```

For example:

```text
Tomato        40
Potato        50
Rice          120
```

The parser also ignores unwanted receipt information such as:

- Total
- Subtotal
- GST
- CGST
- SGST
- Tax
- Discount
- Cash
- Change
- Balance
- Round Off

### 📊 4. Expense Analysis

The application calculates:

- Total Expense
- Number of Items
- Average Price

Example:

```text
Total Expense: ₹450.00
Number of Items: 5
Average Price: ₹90.00
```

### 📈 5. Expense Visualization

A bar chart is generated to visualize the price of each detected item.

This makes it easier to understand which items contributed to the expense.

### 💾 6. SQLite Database

The application uses **SQLite** to store expenses.

Each expense contains:

| Column | Description |
|---|---|
| ID | Unique expense ID |
| Item | Purchased item |
| Price | Item price |
| Date | Date and time of saving |

The database is automatically created as:

```text
expenses.db
```

### 📜 7. Expense History

Previously saved expenses can be viewed from the **Expense History** section.

The application displays:

- Expense ID
- Item
- Price
- Date

It also calculates the total amount of all saved expenses.

### 🗑️ 8. Delete Expenses

Users can select a particular expense ID and delete it from the database.

The application also provides an option to clear the complete expense history.

### 🍳 9. Recipe Suggestions

The application uses the detected grocery items to suggest possible recipes.

For example, if the receipt contains:

```text
Rice
Tomato
Onion
```

The application can suggest:

```text
Tomato Rice
```

The recipe system calculates how many ingredients required for a recipe are available in the detected items.

---

##  Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Streamlit | Web application interface |
| Tesseract OCR | Extract text from receipt images |
| Pytesseract | Python interface for Tesseract |
| OpenCV | Image preprocessing |
| NumPy | Image and numerical processing |
| Pillow | Image handling |
| Pandas | Data processing and analysis |
| SQLite | Expense database |
| Regular Expressions | Item and price extraction |

---

##  Project Structure

```text
Receipt Expense Tracker/
│
├── app.py
├── ocr.py
├── expense_parser.py
├── recipe.py
├── database.py
├── requirements.txt
├── .gitignore
├── README.md
│
└── expenses.db
```

> `expenses.db` is automatically created when the application runs.

---

## File Description

## 1. `app.py`

This is the **main application file**.

It is responsible for:

- Creating the Streamlit interface
- Uploading receipt images
- Calling the OCR module
- Calling the expense parser
- Displaying detected expenses
- Calculating expense statistics
- Displaying charts
- Calling the recipe suggestion module
- Saving expenses to SQLite
- Displaying expense history
- Deleting expenses

---

## 2. `ocr.py`

This file handles **OCR processing**.

The receipt image goes through preprocessing before being passed to Tesseract.

### Processing Flow

```text
Receipt Image
      ↓
Convert to NumPy Array
      ↓
Convert RGB → BGR
      ↓
Grayscale
      ↓
Resize
      ↓
Gaussian Blur
      ↓
Adaptive Thresholding
      ↓
Tesseract OCR
      ↓
Extracted Text
```

The extracted text is returned to `app.py`.

---

## 3. `expense_parser.py`

This module converts OCR text into structured expense data.

It uses **regular expressions** to detect lines containing:

```text
Item + Price
```

The extracted information is stored in the following format:

```python
{
    "Item": "Tomato",
    "Price": 40.0
}
```

The module also filters out unwanted receipt information such as taxes and totals.

---

## 4. `recipe.py`

This file contains the recipe suggestion logic.

It contains:

- Recipe names
- Required ingredients
- Ingredient aliases
- Ingredient normalization
- Recipe matching

For example:

```text
Tomato Rice

Required:
Rice
Tomato
Onion
```

If the receipt contains some or all of these ingredients, the application calculates the recipe match percentage.

---

## 5. `database.py`

This module manages the SQLite database.

It provides functions for:

```text
Create Database
       ↓
Add Expense
       ↓
Get Expenses
       ↓
Get Total Expense
       ↓
Delete Expense
       ↓
Clear Expenses
```

The database table is:

```text
expenses
```

with the following columns:

```text
id
item
price
date
```

---

## 6. `requirements.txt`

This file contains the Python libraries required to run the project.

```text
streamlit
pandas
Pillow
pytesseract
opencv-python
numpy
```

> SQLite does not need to be added to `requirements.txt` because `sqlite3` is included with Python.

---

# ⚙️ Installation

## Step 1: Clone the Repository

Clone the project from GitHub:

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

Move into the project directory:

```bash
cd "Receipt Expense Tracker"
```

---

## Step 2: Create a Virtual Environment

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

---

## Step 3: Install Python Dependencies

Run:

```bash
pip install -r requirements.txt
```

---

## Tesseract OCR Installation

Tesseract OCR is required because `pytesseract` acts as a Python interface for the Tesseract OCR engine.

Install **Tesseract OCR** separately on Windows.

After installation, the `ocr.py` file should contain the correct Tesseract path.

Example:

```python
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)
```

If Tesseract is installed in another location, update the path accordingly.

---

## SQLite Database

The project uses SQLite for storing expenses.

No separate database server is required.

When the application runs, the database is automatically created:

```text
expenses.db
```

The database contains the following table:

```text
expenses
```

### Table Structure

| Column | Type | Description |
|---|---|---|
| id | INTEGER | Primary key |
| item | TEXT | Expense item |
| price | REAL | Expense amount |
| date | TEXT | Date and time |

---

## Running the Application

After installing all dependencies and Tesseract OCR, run:

```bash
streamlit run app.py
```

The Streamlit application will open in the browser.

---

## How to Use

### Step 1 — Upload Receipt

Upload a receipt image using the file uploader.

Supported formats:

```text
.jpg
.jpeg
.png
```

### Step 2 — Process Receipt

Click:

```text
🔍 Process Receipt
```

The application processes the image using OCR.

### Step 3 — View Extracted Text

The OCR output is displayed in the application.

Example:

```text
Tomato 40
Potato 50
Rice 120
Onion 30
```

### Step 4 — View Detected Expenses

The expense parser extracts the item names and prices.

Example:

| Item | Price |
|---|---:|
| Tomato | ₹40.00 |
| Potato | ₹50.00 |
| Rice | ₹120.00 |
| Onion | ₹30.00 |

### Step 5 — Analyze Expenses

The application calculates:

```text
Total Expense
Number of Items
Average Price
```

### Step 6 — Save Expenses

Click:

```text
💾 Save Expenses to Database
```

The detected expenses are stored in SQLite.

### Step 7 — View Expense Chart

The application generates a bar chart showing the prices of the detected items.

### Step 8 — Get Recipe Suggestions

The application checks the detected grocery items against the recipe database.

Example:

```text
Available Items:
Rice
Tomato
Onion

Recipe:
Tomato Rice

Match:
100%
```

### Step 9 — View Expense History

Previously saved expenses can be viewed under:

```text
📜 Expense History
```

### Step 10 — Delete Expenses

A particular expense can be selected using its ID and deleted.

The application also provides:

```text
🗑️ Clear All Expenses
```

to remove the complete expense history.

---

## Core Concepts Used

This project demonstrates several important Python and AI-related concepts.

### Python

- Functions
- Lists
- Dictionaries
- Loops
- Conditional statements
- Modules and imports

### OCR

- Optical Character Recognition
- Image preprocessing
- Text extraction

### Computer Vision

- Grayscale conversion
- Image resizing
- Gaussian blur
- Thresholding

### Data Processing

- Pandas DataFrame
- Data filtering
- Aggregation
- Statistical calculations

### Database

- SQLite
- SQL `CREATE TABLE`
- `INSERT`
- `SELECT`
- `DELETE`
- Primary key
- Parameterized queries

### Regular Expressions

Used to identify item names and prices from OCR-generated text.

### Streamlit

Used to create the interactive web application.

---

## Overall System Architecture

```text
                   ┌──────────────────┐
                   │   Receipt Image  │
                   └────────┬─────────┘
                            │
                            ▼
                   ┌──────────────────┐
                   │   OCR Module     │
                   │    (ocr.py)      │
                   └────────┬─────────┘
                            │
                            ▼
                   ┌──────────────────┐
                   │ Extracted Text   │
                   └────────┬─────────┘
                            │
                            ▼
                ┌────────────────────────┐
                │   Expense Parser       │
                │ (expense_parser.py)    │
                └────────────┬───────────┘
                             │
                             ▼
                  ┌────────────────────┐
                  │ Item + Price Data  │
                  └───────┬────────────┘
                          │
              ┌───────────┼───────────────┐
              │           │               │
              ▼           ▼               ▼
       ┌────────────┐ ┌───────────┐ ┌───────────────┐
       │   Expense  │ │  SQLite   │ │    Recipe     │
       │  Analysis  │ │ Database  │ │ Suggestions   │
       └──────┬─────┘ └─────┬─────┘ └───────────────┘
              │             │
              ▼             ▼
       ┌────────────┐ ┌───────────────┐
       │   Chart    │ │ Expense       │
       │            │ │ History       │
       └────────────┘ └───────────────┘
```

---

## Example Output

### Detected Expenses

```text
Item              Price
-----------------------
Rice              ₹120
Tomato            ₹40
Potato            ₹50
Onion             ₹30
```

### Expense Summary

```text
Total Expense     : ₹240
Number of Items   : 4
Average Price     : ₹60
```

### Recipe Suggestion

```text
🍽️ Tomato Rice

Match: 100%

Available ingredients:
Rice, Tomato, Onion
```

---

## Data and Privacy

The application stores saved expenses locally using:

```text
expenses.db
```

Since the database may contain personal expense information, it is recommended **not to upload `expenses.db` to GitHub**.

Add the following to `.gitignore`:

```text
venv/
__pycache__/
*.pyc
expenses.db
```

---

## Current Limitations

The current version has some limitations:

- OCR accuracy depends on the quality of the receipt image.
- Different receipt formats may produce different OCR results.
- Handwritten receipts may not be recognized accurately.
- The expense parser is based on regular expressions and receipt patterns.
- Recipe suggestions are based on the predefined recipe list.
- Saving the same receipt multiple times can create duplicate database entries.
- Tesseract OCR must be installed separately on the system.

---

## Future Enhancements

The project can be extended with:

- 📱 Mobile-friendly interface
- 🔐 User login and authentication
- 📊 Monthly expense reports
- 📅 Daily/weekly/monthly filtering
- 📈 Advanced expense analytics
- 🥧 Category-wise expense charts
- 🧾 Support for more receipt formats
- 🌐 Multi-language OCR
- 🤖 AI-based expense categorization
- 🥗 More recipe recommendations
- 🔎 Search and filter expense history
- 📥 Export expenses to CSV or Excel
- 🧠 Duplicate receipt detection
- ☁️ Cloud database integration

---

##  Project Objective

The main objective of this project is to develop a simple application that can automatically convert receipt images into structured expense information.

The project combines:

```text
OCR
+
Image Processing
+
Python
+
Data Analysis
+
Database
+
Recipe Recommendation
```

This reduces manual expense entry and provides users with an easy way to track and understand their spending.

---

## Learning Outcomes

Through this project, the following concepts were practiced:

- Building a Python application
- Working with OCR
- Image preprocessing using OpenCV
- Extracting structured information from unstructured text
- Using regular expressions
- Working with Pandas
- Creating interactive Streamlit applications
- Connecting Python with SQLite
- Performing CRUD operations
- Creating data visualizations
- Implementing rule-based recommendations
- Organizing a project into multiple Python modules

---

## Final Project Structure

```text
Receipt Expense Tracker/
│
├── app.py
│   └── Main Streamlit application
│
├── ocr.py
│   └── OCR and image preprocessing
│
├── expense_parser.py
│   └── Extract item names and prices
│
├── recipe.py
│   └── Recipe recommendation logic
│
├── database.py
│   └── SQLite database operations
│
├── requirements.txt
│   └── Python dependencies
│
├── .gitignore
│   └── Files excluded from Git
│
└── README.md
    └── Project documentation
```

---

## Author

**Srudhya Sankaranarayanan**

B.Sc. Computer Science with Artificial Intelligence  
SDNB Vaishnav College for Women

---

### Complete Workflow

```text
Upload Receipt
      ↓
Extract Text
      ↓
Detect Expenses
      ↓
Analyze Spending
      ↓
Save to Database
      ↓
View History
      ↓
Get Recipe Suggestions
```
⭐ **If you find this project useful, consider giving the repository a star!**
