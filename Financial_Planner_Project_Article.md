# Financial Planner: A Practical Approach to Personal Finance Analysis

## 1. Introduction

Managing personal finances involves understanding income, expenses, investments, and regular commitments. Bank statements and payment-app records contain much of this information, but reviewing them manually can be repetitive, especially when a statement contains many transactions.

Financial Planner is a Python application with a Streamlit interface. It is intended to help users upload supported PDF statements, review extracted transaction records, analyze spending, and prepare an editable monthly budget.

The project focuses on organizing financial information and making budget calculations easier to follow. It does not make financial decisions on behalf of the user. Extracted transactions need to be checked, and suggested budget amounts can be adjusted to reflect individual circumstances.

## 2. Problem Statement

Financial statements often contain many rows with dates, descriptions, amounts, and debit or credit indicators. Manually reviewing these records can make it difficult to identify spending patterns and calculate monthly totals.

Different financial providers also use different statement formats. Some statements include running balances alongside transaction amounts. Descriptions can be abbreviated, and the meaning of a transaction may not be immediately clear.

Transfers between a person's own accounts should not necessarily be treated as spending. Loan payments may need to be separated from ordinary expenses, while investments should be tracked independently.

A practical finance application therefore needs more than a way to extract numbers from a PDF. It needs a review process, clear transaction categories, meaningful summaries, and budget calculations that users can verify.

## 3. Project Objectives

The project has four main objectives:

1. Reduce repetitive data entry by extracting candidate transaction details from supported PDF statements.
2. Let users review and correct extracted records before analysis.
3. Present recorded spending through category summaries, financial metrics, and interactive charts.
4. Help users prepare a monthly budget that considers expenses, income, debt payments, and investments.

These objectives create a straightforward process from transaction records to a proposed budget.

## 4. Technology Stack

### Python

Python provides the application logic, transaction parsing, categorization, and budget calculations. It is used to process financial records and prepare the data for analysis.

### Streamlit

Streamlit provides the application interface, including file upload controls, editable tables, input fields, buttons, summary metrics, and navigation between the main sections.

### Pandas

Pandas organizes transactions in data frames. It supports date conversion, numeric validation, filtering by month, grouping transactions by category, calculating totals, and exporting data to CSV.

### Plotly

Plotly creates interactive charts that help users examine recorded expenses by category and understand how spending is distributed.

### pdfplumber

pdfplumber extracts selectable text from supported PDF documents. The application processes that text and attempts to identify transaction dates, descriptions, types, and amounts.

Each technology has a defined role: PDF extraction supplies candidate information, Python and Pandas process it, Plotly presents the analysis, and Streamlit connects the workflow.

## 5. Application Workflow

### 5.1 Uploading a Statement

The user selects a PDF statement. A password field is available when the document is protected. The application extracts available text and attempts to identify transaction rows.

PDF layouts differ. Descriptions may wrap across lines, and amounts may appear near running balances. Some documents contain scanned images instead of selectable text. The current text-extraction workflow does not include OCR for image-only PDFs.

Successful extraction should not be treated as proof that every transaction has been identified correctly.

### 5.2 Reviewing Transactions

After extraction, the user can inspect and correct the transaction table. Dates, descriptions, amounts, categories, and transaction types should be checked before the records are confirmed. The application also provides a way to add individual transactions manually.

This step matters because errors in the source data affect the financial analysis. For example, a payment incorrectly classified as income can distort the calculated cash flow. A debt payment classified as an ordinary expense can also affect how the budget is interpreted.

Users should compare extracted records with the original statement before relying on the results.

### 5.3 Analyzing Spending

The Spending Analysis section calculates totals from the recorded transaction types. It distinguishes income, ordinary expenses, investments, and debt payments. Interactive charts group recorded expenses by category.

These summaries describe the transactions available in the application. An incomplete statement or an incorrectly classified row can change the results. The figures should be interpreted in the context of the quality of the source data.

### 5.4 Preparing a Monthly Budget

The Monthly Budget Plan section uses recorded spending from a selected reference month to suggest initial category budgets.

Essential or regular expenses generally start at their recorded level. Some flexible categories may start with a suggested amount approximately 10 percent below recorded spending.

For instance, if recorded spending for a flexible category was ₹5,000, the suggested starting amount could be ₹4,500. This is only a starting point. The user can increase or decrease the amount according to personal needs.

A reduction may not be appropriate for every category. Rent, education fees, healthcare, family responsibilities, and travel can change from month to month. Users should decide which amounts are realistic rather than treating the suggestions as fixed limits.

The application also allows custom categories when the available budget categories do not match the user's needs.

### 5.5 Reviewing Financial Commitments

The user enters or verifies monthly income, debt payments, and planned investments. These values are considered separately from category-level expenses.

Separating these components makes the arithmetic easier to understand and helps avoid counting a commitment twice. The accuracy of the final balance depends on correct entries and consistent treatment of budget categories.

## 6. Understanding the Budget Calculation

The application estimates the potential remaining balance using this formula:

**Potential remaining balance = Monthly income - Planned expenses - Debt payments - Planned investments**

Consider a person with monthly income of ₹50,000. If planned category expenses total ₹25,000, debt payments total ₹5,000, and planned investments total ₹5,000, the estimated remaining balance is ₹15,000.

Now suppose the person adds a manual category with a budget of ₹2,000. Planned category expenses should increase to ₹27,000. If the other values remain unchanged, the estimated remaining balance should become ₹13,000.

This example illustrates an important implementation requirement: manually entered categories must be included in the same planned-expense total used by the final summary. The displayed figures should match the values used by the calculation and the downloaded budget.

A negative balance means that the entered plan exceeds the entered income. It is a reason to review the figures, not an automatic instruction to cancel a particular payment. Some commitments may be essential or contractually required.

The budget summary is intended to make the arithmetic visible. It does not guarantee that the source data is complete or that the plan is suitable for every household.

## 7. Data Quality and Limitations

Financial analysis depends on reliable source data. PDF extraction can miss transactions, misidentify amounts, or confuse a transaction amount with a running balance. Users should verify extracted rows against the original statement.

The current budgeting method uses rules and recorded spending to create starting targets. It is not a trained machine-learning model, does not forecast financial markets, and does not recommend specific investment products.

Session-based application state also has limitations. It should not be treated as reliable, permanent database storage. A more complete version would preserve monthly plans consistently and include automated tests for financial calculations.

## 8. Privacy and Security

Financial statements can contain names, account details, transaction histories, and other sensitive information. Real statements, passwords, transaction exports, and secret keys should not be committed to a public GitHub repository.

A `.gitignore` file helps exclude common private file types, but it does not replace checking which files have been staged for a commit. Repository contents should be inspected before every push.

The application is a personal budgeting aid, not a replacement for professional financial, investment, or tax advice. Users should verify original transactions and the assumptions behind their budget before acting on the results.

A hosted version intended for multiple users would require stronger authentication, access controls, and secure storage.

## 9. Testing and Future Improvements

Testing should cover transaction extraction, data cleaning, budget calculations, and the displayed interface.

Transaction tests can use sample statements containing known dates and amounts. Data-cleaning tests should check invalid dates, missing amounts, duplicate records, and unsupported transaction types.

Budget calculations should be tested using fixed inputs. For example, with monthly income of ₹50,000, category expenses of ₹27,000, debt payments of ₹5,000, and investments of ₹5,000, the expected remaining balance is ₹13,000. Adding another category with a budget of ₹2,000 should reduce that balance to ₹11,000, provided the other figures remain unchanged.

The interface should also be checked after adding or editing manual categories. The values shown in the summary should agree with the calculated total and the downloaded budget.

Future work could include persistent local database storage, support for more statement formats, OCR for scanned documents, and automated tests that run whenever budget calculations change. Another useful improvement would be a comparison between the original budget suggestion and the revised plan.

Before the project is offered as a service to multiple users, additional controls would be needed to protect sensitive financial records.

## 10. Conclusion

Financial Planner combines PDF text extraction, transaction review, spending analysis, interactive charts, and monthly budgeting in a single Streamlit application.

Its purpose is to make financial records easier to inspect and turn them into a budget that can be adjusted to individual needs. The usefulness of the result depends on data quality, consistent calculations, and careful review by the user.

With stronger testing, persistent storage, and broader support for statement formats, the application could become a more dependable tool for personal finance review.
