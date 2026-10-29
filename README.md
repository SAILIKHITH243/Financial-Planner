# Financial Planner

A personal finance analysis and monthly budgeting application built with Python and Streamlit.

<p align="center">
  <a href="https://github.com/SAILIKHITH243/Financial-Planner">GitHub Repository</a>
  &nbsp; | &nbsp;
  <a href="https://financial-planner-mmdx9umyocdxcwwsmgmhdc.streamlit.app/">Live Demo</a>
</p>

## Overview

Financial Planner helps users organize transaction records from supported PDF statements, review income and spending, explore category-level expenses, and prepare a monthly budget. It combines transaction review, financial summaries, interactive charts, and CSV exports in a single interface.

The application is intended to support personal budgeting decisions. Users should verify extracted transactions and review all budget assumptions before relying on the results.

## Key Features

- **PDF statement import:** Extract candidate transaction details from supported text-based PDF statements.
- **Password-protected PDFs:** Enter a document password when required and supported by the PDF.
- **Transaction review:** Inspect and correct transaction dates, descriptions, amounts, categories, and types.
- **Manual entry:** Add transactions that were not extracted or need to be recorded separately.
- **Financial summaries:** Review recorded income, expenses, investments, debt payments, and estimated cash flow.
- **Spending analysis:** Explore category-level spending using interactive charts.
- **Monthly budget planning:** Review and adjust suggested category budgets.
- **Custom categories:** Add budget categories to suit individual needs.
- **Budget balance estimate:** Estimate the remaining balance after planned expenses, debt payments, and investments.
- **CSV export:** Download reviewed transaction data and budget details for further analysis.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application logic and financial calculations |
| Streamlit | Web application interface |
| Pandas | Data cleaning, filtering, and aggregation |
| Plotly | Interactive financial charts |
| pdfplumber | Text extraction from supported PDF statements |

## Application Workflow

1. **Import:** Upload a supported PDF statement and enter its password if required.
2. **Review:** Check extracted transaction rows against the original statement and correct any errors.
3. **Categorize:** Verify transaction types and categories; add missing transactions manually when needed.
4. **Analyze:** Review financial summaries and category-level spending charts.
5. **Plan:** Select a month and adjust the proposed budget, income, debt payments, and investments.
6. **Export:** Download available transaction or budget data as CSV.

## Budget Calculation

The application estimates a potential remaining balance using:

**Potential remaining balance = Monthly income − Planned expenses − Debt payments − Planned investments**

For example, if monthly income is ₹50,000, planned expenses are ₹25,000, debt payments are ₹5,000, and planned investments are ₹5,000, the estimated remaining balance is ₹15,000.

This is an arithmetic estimate based on the values entered. Users should confirm that expenses and commitments are categorized consistently and are not counted twice.

## Getting Started

### Prerequisites

- Python 3.10 or a compatible newer version
- pip
- A modern web browser

### 1. Clone the repository

```bash
git clone https://github.com/SAILIKHITH243/Financial-Planner.git
cd Financial-Planner
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the application

Once the project's `app.py` file is present in the project root, run:

```bash
streamlit run app.py
```

Open the local URL displayed in the terminal. Streamlit commonly uses `http://localhost:8501`.

## Live Application

**Live Demo:** [Open Financial Planner](https://financial-planner-mmdx9umyocdxcwwsmgmhdc.streamlit.app/)

The application is hosted on Streamlit Community Cloud. Open the live demo to explore the interface and try the available features. When using demo or personal financial data, verify extracted transactions and review calculations before relying on the results.

## Limitations

- PDF extraction may not support every bank or payment-app statement layout.
- Scanned or image-only PDFs require OCR, which is not included in the current text-extraction workflow.
- Extracted transaction records must be manually checked.
- Budget suggestions are rule-based starting points, not machine-learning predictions or professional financial advice.
- Session-based values are not a substitute for durable database storage.
- Results depend on the completeness and accuracy of the data entered.

## Privacy and Security

Financial statements and transaction exports may contain sensitive personal information.

- Do not commit real statements, passwords, account details, API keys, or private transaction data to a public repository.
- Review staged files before committing changes.
- Keep secrets out of source code and repository history.
- A multi-user hosted version should implement appropriate authentication, access controls, and secure storage.

The application is a budgeting aid and does not provide professional financial, investment, lending, or tax advice.

## Future Enhancements

Potential improvements include:

- Persistent storage for budgets and transaction records
- Broader support for statement formats
- OCR for scanned statements
- Automated tests for extraction and budget calculations
- Improved validation for duplicate transactions and ambiguous amounts
- Budget-versus-actual comparisons

## Repository Structure

The expected core project files include:

```text
Financial-Planner/
├── app.py
├── README.md
├── requirements.txt
├── .gitignore
└── Financial_Planner_Project_Article.md
```

The repository structure may change as the project develops.

## License

No license has been specified yet. Add a license before allowing others to reuse or distribute this project.

## Author

**Sai Likhith**

GitHub: [SAILIKHITH243](https://github.com/SAILIKHITH243)
