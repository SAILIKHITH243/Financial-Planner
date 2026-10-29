# Financial Planner

**GitHub Repository:** [SAILIKHITH243/Financial-Planner](https://github.com/SAILIKHITH243/Financial-Planner)  
**Live Website:** Not deployed yet. A public application URL will be added after deployment.

Financial Planner is a personal finance application built with Python and Streamlit. It is designed to help users review transaction records, understand spending patterns, and prepare a monthly budget based on recorded expenses and financial commitments.

The application brings transaction review, spending analysis, category-level budgeting, and CSV export into one interface.

## Features

- Extract candidate transaction records from supported PDF statements.
- Enter a password when a PDF document is protected.
- Review and correct extracted dates, descriptions, amounts, categories, and transaction types.
- Add transactions manually when required.
- Analyze recorded income, expenses, investments, and debt payments.
- Explore category-level spending with interactive charts.
- Prepare and edit a monthly budget.
- Add custom budget categories to reflect individual needs.
- Estimate the remaining balance after planned expenses, debt payments, and investments.
- Export reviewed transaction data and budget details to CSV.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application logic and financial calculations |
| Streamlit | Web interface and interactive controls |
| Pandas | Data cleaning, filtering, and aggregation |
| Plotly | Interactive charts |
| pdfplumber | Text extraction from supported PDF documents |

## Getting Started

### Requirements

- Python 3.10 or a compatible newer version
- pip
- A modern web browser

### Install dependencies

From the project directory, run:

```powershell
pip install -r requirements.txt
```

### Run the application

```powershell
streamlit run app.py
```

Open the local URL printed in the terminal. Streamlit commonly uses `http://localhost:8501`.

## How to Use

### Upload and review

Select a supported PDF statement and enter its password if required. The extracted rows are candidate transactions, so check the dates, descriptions, amounts, categories, and transaction types against the original statement before confirming the records. Individual transactions can also be entered manually.

### Analyze spending

Review the recorded income, expenses, investments, debt payments, and cash flow. Category charts help users understand how recorded expenses are distributed. The results depend on the completeness and accuracy of the transaction data.

### Prepare a monthly budget

Select a reference month and review the suggested category budgets. Essential or regular categories generally start at their recorded level. Some flexible categories may receive a suggested reduction of approximately 10 percent. These are starting suggestions, not compulsory limits.

Users can adjust the proposed amounts and add custom categories. Monthly income, debt payments, and planned investments should also be verified before relying on the final balance.

### Export results

Use the CSV download options to save reviewed transactions or the current budget for further analysis in spreadsheet software.

## Budget Calculation

The application estimates the potential remaining balance using:

**Potential remaining balance = Monthly income - Planned expenses - Debt payments - Planned investments**

For example, monthly income of ₹50,000, planned category expenses of ₹25,000, debt payments of ₹5,000, and planned investments of ₹5,000 leave an estimated balance of ₹15,000.

If a new category adds ₹2,000 to planned expenses, the remaining balance should decrease to ₹13,000 if the other values stay unchanged. Users should verify that the displayed totals match the values entered.

## Limitations

- PDF extraction may not work for every bank or payment-app statement layout.
- Scanned, image-only PDFs are not supported by the current text-extraction workflow unless OCR is added.
- Extracted transactions need manual verification.
- Budget suggestions are rule-based starting points, not machine-learning predictions.
- Session-based values are not a substitute for durable database storage.
- The application is a budgeting aid, not professional financial, investment, lending, or tax advice.

## Privacy and Security

Financial statements and transaction exports may contain sensitive information. Do not commit real statements, passwords, account details, API keys, or private transaction data to a public repository.

The `.gitignore` file helps exclude common private file types, but repository contents should still be reviewed before each commit. A hosted version intended for multiple users would require suitable authentication, access controls, and secure storage.

## Future Improvements

Potential improvements include persistent storage for monthly budgets, broader statement-format support, OCR for scanned documents, automated tests for budget calculations, and a comparison between the original budget suggestion and a revised plan.

## License

Add an appropriate license before distributing the project for reuse.

## Author

**Sai Likhith**
