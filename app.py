import io
import re
import math
from datetime import date, datetime

import pandas as pd
import plotly.express as px
import streamlit as st
import pdfplumber

st.set_page_config(
    page_title="Financial Planner",
    page_icon="₹",
    layout="wide"
)

# Premium Emerald, Champagne Gold and Ivory palette
GREEN = "#123C35"
JADE = "#1F6B5C"
GOLD = "#D6B36A"
IVORY = "#F7F5EF"
INK = "#30413B"
MUTED = "#6E7A73"
BORDER = "#E1E5DC"
WHITE = "#FFFFFF"

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@600;700&display=swap');

.stApp {background:#F7F5EF;color:#30413B;font-family:'DM Sans',sans-serif}
.block-container {max-width:1450px;padding-top:1.8rem;padding-bottom:3rem}
h1,h2,h3 {color:#123C35}
h1 {font-family:'Playfair Display',serif}
[data-testid="stSidebar"] {background:#123C35}
[data-testid="stSidebar"] * {color:#FFFFFF}
[data-testid="stMetric"] {
  background:#FFFFFF;border:1px solid #E1E5DC;
  border-radius:14px;padding:17px
}
[data-testid="stMetricValue"] {color:#123C35}
[data-testid="stMetricLabel"] p {color:#6E7A73}
div.stButton>button,div.stFormSubmitButton>button {
  background:#123C35;color:#FFFFFF;border:1px solid #123C35;
  border-radius:9px;font-weight:600
}
div.stButton>button:hover,div.stFormSubmitButton>button:hover {
  background:#1F6B5C;color:#FFFFFF;border-color:#1F6B5C
}
[data-testid="stAlert"] {
  background:#FFF3D6;border:1px solid #D6B36A;border-radius:12px
}
[data-testid="stAlert"] * {color:#49380C}
[data-testid="stProgressBar"] > div {background:#E1E5DC}
[data-testid="stProgressBar"] [role="progressbar"] {background:#D6B36A}
div[data-testid="stExpander"] {
  background:#FFFFFF;border:1px solid #E1E5DC;border-radius:12px
}
[data-testid="stDataFrame"] {background:#FFFFFF}
input,textarea {
  background:#FFFFFF !important;color:#30413B !important
}
hr {border-color:#E1E5DC}
.hero {
  background:linear-gradient(120deg,#123C35,#1F6B5C);
  border-radius:18px;padding:27px 30px;color:#FFFFFF;margin-bottom:22px
}
.hero h1 {color:#FFFFFF;font-size:35px;margin-bottom:7px}
.hero p {color:#E6EEE9;margin-bottom:0}
.eyebrow {font-size:12px;font-weight:700;letter-spacing:2px;color:#D6B36A}
.small-note {font-size:13px;color:#6E7A73}
</style>
""", unsafe_allow_html=True)

# FINANCIAL PLANNER GLOBAL LABEL CONTRAST
st.markdown("""
<style>
/* Main form labels: dark text on ivory */
[data-testid="stWidgetLabel"],
[data-testid="stWidgetLabel"] *,
[data-testid="stWidgetLabel"] p,
.stNumberInput label,
.stNumberInput label p,
.stTextInput label,
.stTextInput label p,
.stSelectbox label,
.stSelectbox label p,
.stDateInput label,
.stDateInput label p,
.stFileUploader label,
.stFileUploader label p,
.stRadio label,
.stCheckbox label,
.stSlider label,
.stSlider label p {
    color: #30413B !important;
    opacity: 1 !important;
}

/* Keep sidebar text readable on emerald */
[data-testid="stSidebar"] [data-testid="stWidgetLabel"],
[data-testid="stSidebar"] [data-testid="stWidgetLabel"] *,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] label p {
    color: #FFFFFF !important;
    opacity: 1 !important;
}

/* Readable inputs and dropdowns */
[data-baseweb="input"],
[data-baseweb="select"],
[data-baseweb="textarea"] {
    background: #FFFFFF !important;
    color: #30413B !important;
}
[data-baseweb="input"] input,
[data-baseweb="textarea"] textarea {
    color: #30413B !important;
    -webkit-text-fill-color: #30413B !important;
}

/* Plotly charts: readable legend, axes and titles */
[data-testid="stPlotlyChart"] .xtick text,
[data-testid="stPlotlyChart"] .ytick text,
[data-testid="stPlotlyChart"] .g-xtitle text,
[data-testid="stPlotlyChart"] .g-ytitle text,
[data-testid="stPlotlyChart"] .legend text,
[data-testid="stPlotlyChart"] .legendtitle text {
    fill: #30413B !important;
    opacity: 1 !important;
}
</style>
""", unsafe_allow_html=True)


# FINANCIAL PLANNER CHART READABILITY FIX
st.markdown("""
<style>
/* Force chart labels to use dark, readable colours */
[data-testid="stPlotlyChart"] .xtick text,
[data-testid="stPlotlyChart"] .ytick text,
[data-testid="stPlotlyChart"] .g-xtitle text,
[data-testid="stPlotlyChart"] .g-ytitle text,
[data-testid="stPlotlyChart"] .legend text,
[data-testid="stPlotlyChart"] .legendtitle text,
[data-testid="stPlotlyChart"] .gtitle,
[data-testid="stPlotlyChart"] .annotation-text {
    fill: #30413B !important;
    opacity: 1 !important;
    font-weight: 600 !important;
}

/* Clean chart background and visible grid lines */
[data-testid="stPlotlyChart"] .bglayer rect {
    fill: #FFFFFF !important;
}
[data-testid="stPlotlyChart"] .gridlayer path {
    stroke: #E1E5DC !important;
    stroke-opacity: 1 !important;
}
[data-testid="stPlotlyChart"] .zerolinelayer path {
    stroke: #B8C7BD !important;
}

/* Make chart toolbar icons visible */
[data-testid="stPlotlyChart"] .modebar-btn path {
    fill: #30413B !important;
}

/* Keep chart panels bright */
[data-testid="stPlotlyChart"] .plot-container {
    background-color: #FFFFFF !important;
}
</style>
""", unsafe_allow_html=True)


COLUMNS = ["Date", "Type", "Category", "Amount", "Description"]
TYPES = ["Income", "Expense", "Investment", "Debt Payment", "Other"]

DATE_PATTERN = re.compile(
    r"(?<!\d)(?:"
    r"\d{4}-\d{1,2}-\d{1,2}|"
    r"\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|"
    r"\d{1,2}[-/ ]+[A-Za-z]{3,9}[-/ ]+\d{2,4}|"
    r"\d{1,2}\s+[A-Za-z]{3,9}\s+\d{4}"
    r")(?!\d)",
    re.I
)

MONEY_PATTERN = re.compile(
    r"(?<![A-Za-z0-9])(?:₹\s*)?"
    r"(?:\(?-?\d{1,3}(?:,\d{3})+(?:\.\d{1,2})?\)?"
    r"|\(?-?\d{4,}(?:\.\d{1,2})?\)?"
    r"|\(?-?\d{1,3}\.\d{1,2}\)?)"
    r"(?![A-Za-z0-9])"
)


def parse_date(value):
    if value is None:
        return None

    if isinstance(value, (datetime, date)):
        return value.date() if isinstance(value, datetime) else value

    text = str(value).strip()
    formats = [
        "%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y",
        "%d/%m/%y", "%d-%m-%y", "%d %b %Y",
        "%d %B %Y", "%d-%b-%Y", "%d-%B-%Y",
        "%d/%b/%Y", "%d/%B/%Y"
    ]

    for fmt in formats:
        try:
            return datetime.strptime(text, fmt).date()
        except ValueError:
            continue

    return None


def categorize(description):
    text = str(description).lower()

    rules = [
        ("Housing / Rent", r"\brent\b|\bhousing\b|landlord"),
        ("Groceries", r"grocery|groceries|supermarket|vegetable|vegetables|provision"),
        ("Food & Dining", r"restaurant|swiggy|zomato|cafe|coffee|food|dining"),
        ("Transport", r"uber|ola cab|rapido|petrol|fuel|metro|bus fare|train|parking|transport"),
        ("Utilities", r"electricity|water bill|internet|broadband|mobile recharge|telephone|gas bill"),
        ("Healthcare", r"hospital|pharmacy|medical|doctor|clinic|medicine"),
        ("Shopping", r"shopping|amazon|flipkart|myntra|retail|clothing|fashion"),
        ("Education", r"school|college|tuition|course fee|education|university"),
        ("Insurance", r"insurance|premium"),
        ("Loan Payment", r"loan|emi|installment|instalment"),
        ("Investment", r"mutual fund|sip|investment|stocks|shares|broker"),
        ("Salary / Income", r"salary|payroll|wages"),
        ("Interest / Refund", r"interest|cashback|refund|reversal"),
        ("Entertainment", r"movie|cinema|netflix|spotify|gaming|entertainment"),
        ("Transfer", r"transfer|self transfer|own account")
    ]

    for category, pattern in rules:
        if re.search(pattern, text):
            return category

    return "Other"


def infer_type(description, marker=""):
    text = (str(description) + " " + str(marker)).lower()

    # Expenses take priority for purchases and payments.
    if re.search(
        r"\b(debit|dr|withdrawal|purchase|pos|atm|paid|"
        r"payment|emi|bill payment|card payment)\b",
        text
    ):
        return "Debt Payment" if re.search(r"\b(loan|emi)\b", text) else "Expense"

    if re.search(
        r"\b(salary|payroll|refund|cashback|interest credited|"
        r"deposit|credited|received|credit)\b",
        text
    ):
        return "Income"

    if re.search(r"mutual fund|sip|stocks|shares|investment", text):
        return "Investment"

    if re.search(r"\b(transfer|self transfer)\b", text):
        return "Other"

    return "Expense"


def parse_transaction_lines(pdf_text):
    rows = []
    lines = pdf_text.splitlines()

    month_names = (
        r"(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|"
        r"Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:t(?:ember)?)?|"
        r"Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)"
    )

    date_pattern = re.compile(
        rf"(?<!\w)(?:"
        rf"{month_names}\s+\d{{1,2}},?\s+\d{{4}}|"
        r"\d{4}[-/]\d{1,2}[-/]\d{1,2}|"
        r"\d{1,2}[-/]\d{1,2}[-/]\d{2,4}|"
        rf"\d{{1,2}}\s+{month_names}\s+\d{{4}}"
        r")(?!\w)",
        re.IGNORECASE
    )

    def parsed_date(value):
        value = " ".join(value.strip().split())
        formats = (
            "%b %d, %Y", "%B %d, %Y",
            "%b %d %Y", "%B %d %Y",
            "%Y-%m-%d", "%Y/%m/%d",
            "%d/%m/%Y", "%d-%m-%Y",
            "%d/%m/%y", "%d-%m-%y",
            "%d %b %Y", "%d %B %Y",
            "%d-%b-%Y", "%d-%B-%Y",
            "%m/%d/%Y"
        )
        for fmt in formats:
            try:
                return datetime.strptime(value, fmt).date()
            except ValueError:
                continue
        return None

    # Dedicated PhonePe format:
    # Sep 14, 2026 Paid to Merchant Debit INR 20.00
    phonepe_pattern = re.compile(
        rf"^(?P<date>{month_names}\s+\d{{1,2}},\s*\d{{4}})\s+"
        r"(?P<details>.*?)\s+"
        r"(?P<marker>Debit|Credit)\s+INR"
        r"(?:\s+(?P<amount>[\d,]+(?:\.\d{1,2})?))?\s*$",
        re.IGNORECASE
    )

    for i, raw_line in enumerate(lines):
        line = " ".join(raw_line.strip().split())
        match = phonepe_pattern.match(line)
        if not match:
            continue

        tx_date = parsed_date(match.group("date"))
        amount_text = match.group("amount")

        if not amount_text:
            for following in lines[i + 1:min(i + 4, len(lines))]:
                if re.search(r"Transaction\s+ID\s*:", following, re.I):
                    found = re.search(r"([\d,]+\.\d{2})\s*$", following.strip())
                    if found:
                        amount_text = found.group(1)
                        break

        if not tx_date or not amount_text:
            continue

        try:
            amount = abs(float(amount_text.replace(",", "")))
        except ValueError:
            continue

        if amount <= 0:
            continue

        description = " ".join(match.group("details").split())
        marker = match.group("marker").lower()
        category = categorize(description)
        tx_type = "Income" if marker == "credit" else "Expense"

        if category == "Loan Payment":
            tx_type = "Debt Payment"
        elif category == "Investment":
            tx_type = "Investment"

        rows.append({
            "Date": tx_date,
            "Type": tx_type,
            "Category": category,
            "Amount": round(amount, 2),
            "Description": description
        })

    # If the document is not PhonePe format, try general bank/UPI layouts.
    if not rows:
        dated_blocks = []

        for i, raw_line in enumerate(lines):
            line = " ".join(raw_line.strip().split())
            match = date_pattern.search(line)
            if match:
                tx_date = parsed_date(match.group())
                if tx_date:
                    dated_blocks.append((i, tx_date, match.start(), match.end()))

        amount_pattern = re.compile(
            r"(?<![A-Za-z0-9])(?:₹\s*|INR\s*)?"
            r"(\(?-?\d[\d,]*(?:\.\d{1,2})?\)?)"
            r"(?![A-Za-z0-9])",
            re.IGNORECASE
        )

        for position, (line_index, tx_date, ds, de) in enumerate(dated_blocks):
            next_index = (
                dated_blocks[position + 1][0]
                if position + 1 < len(dated_blocks)
                else min(len(lines), line_index + 5)
            )

            block_lines = lines[line_index:next_index]
            if not block_lines:
                continue

            first_line = block_lines[0]
            first_line = first_line[:ds] + " " + first_line[de:]
            combined = " ".join(
                [first_line] + [str(x) for x in block_lines[1:]]
            )
            combined = " ".join(combined.split())

            # Ignore statement headings and balance summaries.
            if re.search(
                r"opening balance|closing balance|statement summary|"
                r"total debit|total credit|page total",
                combined, re.I
            ):
                continue

            marker_match = re.search(
                r"\b(debit|dr|withdrawal|credit|cr|deposit)\b",
                combined, re.I
            )

            amounts = []
            for amount_match in amount_pattern.finditer(combined):
                raw_amount = amount_match.group(1)
                cleaned = raw_amount.replace(",", "").replace("(", "").replace(")", "")

                try:
                    number = abs(float(cleaned))
                except ValueError:
                    continue

                if number <= 0 or number > 1_000_000_000_000:
                    continue

                # Ignore likely long reference/account numbers.
                digits = re.sub(r"\D", "", raw_amount)
                if len(digits) >= 12:
                    continue

                amounts.append((amount_match.start(), amount_match.end(), number))

            if not amounts:
                continue

            # If an explicit DR/CR marker exists, use the nearest amount
            # immediately before it. Otherwise prefer the last amount,
            # which suits common rows where transaction amount is last.
            chosen = None
            if marker_match:
                before = [
                    item for item in amounts
                    if item[1] <= marker_match.start()
                ]
                if before:
                    chosen = before[-1]

            if chosen is None:
                # Avoid selecting the running balance where possible.
                chosen = amounts[-2] if len(amounts) >= 2 else amounts[-1]

            amount = chosen[2]

            description = combined
            description = date_pattern.sub(" ", description, count=1)
            description = amount_pattern.sub(" ", description)
            description = re.sub(
                r"\b(debit|dr|withdrawal|credit|cr|deposit|INR|UPI|"
                r"transaction\s+id|reference\s+no)\b",
                " ", description, flags=re.I
            )
            description = re.sub(r"\b\d{8,}\b", " ", description)
            description = " ".join(description.split()).strip(" -|:/")

            if len(description) < 2:
                description = "Unclear transaction description"

            marker = marker_match.group(1).lower() if marker_match else ""
            if marker in ("credit", "cr", "deposit"):
                tx_type = "Income"
            elif marker in ("debit", "dr", "withdrawal"):
                tx_type = "Expense"
            else:
                tx_type = infer_type(description)

            category = categorize(description)

            if category == "Loan Payment":
                tx_type = "Debt Payment"
            elif category == "Investment":
                tx_type = "Investment"

            rows.append({
                "Date": tx_date,
                "Type": tx_type,
                "Category": category,
                "Amount": round(amount, 2),
                "Description": description
            })

    result = pd.DataFrame(rows, columns=COLUMNS)

    if not result.empty:
        result = result.drop_duplicates(
            subset=["Date", "Type", "Amount", "Description"]
        ).reset_index(drop=True)

    return result

def extract_pdf(file_bytes, password=""):
    """Read selectable PDF text, supporting password-protected PDFs."""
    pages_text = []

    with pdfplumber.open(
        io.BytesIO(file_bytes),
        password=password or ""
    ) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text() or ""

            if page_text.strip():
                pages_text.append(page_text)
            else:
                # Table fallback for PDFs where text extraction is sparse.
                table_lines = []
                for table in (page.extract_tables() or []):
                    for row in table:
                        cells = [
                            str(cell).strip()
                            for cell in (row or [])
                            if cell is not None and str(cell).strip()
                        ]
                        if cells:
                            table_lines.append(" | ".join(cells))

                pages_text.append("\n".join(table_lines))

    return "\n".join(pages_text)

def clean_transactions(data):
    if data is None or data.empty:
        return pd.DataFrame(columns=COLUMNS)

    result = data.copy()

    for col in COLUMNS:
        if col not in result.columns:
            result[col] = ""

    result["Date"] = pd.to_datetime(
        result["Date"], errors="coerce"
    ).dt.date

    result["Amount"] = pd.to_numeric(
        result["Amount"], errors="coerce"
    )

    result["Type"] = result["Type"].fillna("Expense").astype(str)
    result["Category"] = result["Category"].fillna("Other").astype(str)
    result["Description"] = result["Description"].fillna("").astype(str)

    result = result.dropna(subset=["Date", "Amount"])
    result = result[result["Amount"] > 0]
    result = result[result["Type"].isin(TYPES)]

    return result[COLUMNS].reset_index(drop=True)


def sample_transactions():
    today = date.today()

    sample = [
        (-60, "Income", "Salary / Income", 40000, "Monthly salary"),
        (-59, "Expense", "Housing / Rent", 8000, "Monthly rent"),
        (-57, "Expense", "Groceries", 5000, "Supermarket"),
        (-55, "Expense", "Food & Dining", 4000, "Restaurant"),
        (-53, "Expense", "Transport", 3000, "Fuel and travel"),
        (-50, "Expense", "Shopping", 5000, "Shopping"),
        (-45, "Investment", "Investment", 5000, "Monthly SIP"),
        (-43, "Debt Payment", "Loan Payment", 3000, "Loan EMI"),
        (-30, "Income", "Salary / Income", 40000, "Monthly salary"),
        (-29, "Expense", "Housing / Rent", 8000, "Monthly rent"),
        (-27, "Expense", "Groceries", 4800, "Supermarket"),
        (-25, "Expense", "Food & Dining", 3500, "Restaurant"),
        (-23, "Expense", "Transport", 2800, "Fuel and travel"),
        (-21, "Expense", "Shopping", 4500, "Shopping"),
        (-20, "Investment", "Investment", 5000, "Monthly SIP"),
        (-18, "Debt Payment", "Loan Payment", 3000, "Loan EMI"),
    ]

    return pd.DataFrame([
        {
            "Date": today + pd.Timedelta(days=offset),
            "Type": kind,
            "Category": category,
            "Amount": amount,
            "Description": description
        }
        for offset, kind, category, amount, description in sample
    ], columns=COLUMNS).assign(
        Date=lambda d: pd.to_datetime(d["Date"]).dt.date
    )


if "transactions" not in st.session_state:
    st.session_state.transactions = pd.DataFrame(columns=COLUMNS)

if "confirmed" not in st.session_state:
    st.session_state.confirmed = False

if "source_name" not in st.session_state:
    st.session_state.source_name = ""

if "budgets" not in st.session_state:
    st.session_state.budgets = {}


with st.sidebar:
    st.markdown(
        f"<div style='font-size:24px;font-weight:700;color:{GOLD}'>"
        "Financial Planner</div>",
        unsafe_allow_html=True
    )
    st.caption("PERSONAL FINANCE ANALYTICS")
    st.divider()

    page = st.radio(
        "WORKSPACE",
        [
            "1. Upload & Review",
            "2. Spending Analysis",
            "3. Monthly Budget Plan"
        ]
    )

    st.divider()
    st.caption("Review all extracted transactions before relying on calculations.")

    if st.button("Clear current data", use_container_width=True):
        st.session_state.transactions = pd.DataFrame(columns=COLUMNS)
        st.session_state.confirmed = False
        st.session_state.source_name = ""
        st.session_state.pop("review_editor", None)
        st.rerun()


st.markdown("""
<div class="hero">
  <div class="eyebrow">PERSONAL FINANCE INTELLIGENCE</div>
  <h1>Understand your money. Plan your future.</h1>
  <p>Upload an expense PDF, review the transactions, understand your spending
  and create a practical budget for next month.</p>
</div>
""", unsafe_allow_html=True)


if page == "1. Upload & Review":
    st.header("Upload your financial document")
    st.write(
        "Start with a text-based bank statement, expense report or transaction PDF. "
        "You can also try the demo data to explore the website."
    )

    pdf_file = st.file_uploader(
        "Choose a PDF document",
        type=["pdf"],
        help="Upload a regular or password-protected PDF."
    )

    pdf_password = st.text_input(
        "PDF password (if required)",
        type="password",
        placeholder="Enter the password supplied by your bank or payment app",
        help="Leave this blank for an unprotected PDF. Enter the correct password for protected PDFs."
    )

    c1, c2 = st.columns(2)

    with c1:
        extract_clicked = st.button(
            "Extract transactions from PDF",
            use_container_width=True
        )

    with c2:
        demo_clicked = st.button(
            "Load demo transactions",
            use_container_width=True
        )

    if extract_clicked:
        if pdf_file is None:
            st.warning("First choose a PDF document.")
        else:
            try:
                with st.spinner("Reading your PDF and extracting transaction rows..."):
                    text = extract_pdf(pdf_file.getvalue(), password=pdf_password)

                if not text.strip():
                    st.error(
                        "No selectable text was found. This PDF may be scanned "
                        "or image-based. OCR support is not enabled in this version."
                    )
                else:
                    extracted = parse_transaction_lines(text)

                    if extracted.empty:
                        st.warning(
                            "Text was read, but transaction rows could not be "
                            "reliably identified. Try another statement or add "
                            "transactions manually below."
                        )
                    else:
                        st.session_state.transactions = extracted
                        st.session_state.confirmed = False
                        st.session_state.source_name = pdf_file.name
                        st.session_state.pop("review_editor", None)
                        st.success(
                            f"Found {len(extracted)} candidate transactions. "
                            "Review the table carefully before confirming."
                        )
            except Exception as exc:
                st.error(
                    "Could not open this PDF. Check the password and try again. "
                    "Some PDF encryption methods or document layouts may not be supported."
                )
                with st.expander("Technical error details"):
                    st.code(str(exc))

    if demo_clicked:
        st.session_state.transactions = sample_transactions()
        st.session_state.confirmed = False
        st.session_state.source_name = "Demo data"
        st.session_state.pop("review_editor", None)
        st.rerun()

    if st.session_state.source_name:
        st.caption(f"Current data source: {st.session_state.source_name}")

    if not st.session_state.transactions.empty:
        st.divider()
        st.subheader("Review and correct extracted transactions")
        st.info(
            "PDF layouts vary. Check dates, descriptions, amounts and transaction "
            "types. In bank statements with a running balance, the amount can be "
            "misidentified; correct any incorrect rows in the table below."
        )

        review_data = st.session_state.transactions.copy()
        review_data["Date"] = pd.to_datetime(
            review_data["Date"], errors="coerce"
        )

        with st.form("transaction_review_form"):
            edited = st.data_editor(
                review_data,
                key="review_editor",
                num_rows="dynamic",
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Date": st.column_config.DateColumn(
                        "Date", format="DD/MM/YYYY"
                    ),
                    "Type": st.column_config.SelectboxColumn(
                        "Type", options=TYPES, required=True
                    ),
                    "Category": st.column_config.TextColumn("Category"),
                    "Amount": st.column_config.NumberColumn(
                        "Amount (₹)", min_value=0.0, format="%.2f"
                    ),
                    "Description": st.column_config.TextColumn("Description")
                }
            )

            confirmed = st.form_submit_button(
                "Confirm transactions and save for analysis",
                use_container_width=True
            )

        if confirmed:
            cleaned = clean_transactions(edited)

            if cleaned.empty:
                st.error(
                    "No valid transaction rows remain. Check dates and amounts."
                )
            else:
                st.session_state.transactions = cleaned
                st.session_state.confirmed = True
                st.success(
                    f"Confirmed {len(cleaned)} transactions. "
                    "Open Spending Analysis to view your results."
                )

        with st.expander("Add a transaction manually"):
            with st.form("manual_transaction_form", clear_on_submit=True):
                a, b, c = st.columns(3)
                tx_date = a.date_input("Date", value=date.today())
                tx_type = b.selectbox("Type", TYPES)
                tx_amount = c.number_input(
                    "Amount (₹)", min_value=0.01, value=1000.0, step=100.0
                )

                d, e = st.columns(2)
                tx_category = d.text_input(
                    "Category", placeholder="Groceries, rent, salary..."
                )
                tx_description = e.text_input(
                    "Description", placeholder="Transaction details"
                )

                add_clicked = st.form_submit_button("Add transaction")

                if add_clicked:
                    if not tx_category.strip():
                        st.error("Enter a category.")
                    else:
                        new_row = pd.DataFrame([{
                            "Date": tx_date,
                            "Type": tx_type,
                            "Category": tx_category.strip(),
                            "Amount": tx_amount,
                            "Description": tx_description.strip()
                        }], columns=COLUMNS)

                        st.session_state.transactions = pd.concat(
                            [st.session_state.transactions, new_row],
                            ignore_index=True
                        )
                        st.session_state.confirmed = False
                        st.success("Transaction added. Confirm the table again.")
                        st.rerun()

        st.download_button(
            "Download reviewed transactions as CSV",
            data=st.session_state.transactions.to_csv(
                index=False
            ).encode("utf-8"),
            file_name="reviewed_financial_transactions.csv",
            mime="text/csv"
        )

    else:
        st.markdown("### What happens after uploading?")
        a, b, c = st.columns(3)
        a.markdown("**1. Read PDF**")
        a.caption("Extract candidate dates, descriptions and amounts.")
        b.markdown("**2. Review**")
        b.caption("Correct any extraction errors before analysis.")
        c.markdown("**3. Get insights**")
        c.caption("Calculate spending, categories and a monthly budget.")


elif page == "2. Spending Analysis":
    st.header("Your spending analysis")

    if st.session_state.transactions.empty:
        st.info("Upload a PDF or load demo transactions in Upload & Review first.")
        st.stop()

    if not st.session_state.confirmed:
        st.warning(
            "These transactions have not been confirmed. Review the table first "
            "to reduce the risk of incorrect financial calculations."
        )

    df = clean_transactions(st.session_state.transactions)

    income = df.loc[df["Type"] == "Income", "Amount"].sum()
    expenses = df.loc[df["Type"] == "Expense", "Amount"].sum()
    investments = df.loc[df["Type"] == "Investment", "Amount"].sum()
    debt = df.loc[df["Type"] == "Debt Payment", "Amount"].sum()
    cash_flow = income - expenses - investments - debt
    savings_rate = (cash_flow / income * 100) if income > 0 else 0

    a, b, c, d = st.columns(4)
    a.metric("Recorded income", f"₹{income:,.0f}")
    b.metric("Expenses", f"₹{expenses:,.0f}")
    c.metric("Investments", f"₹{investments:,.0f}")
    d.metric("Remaining cash flow", f"₹{cash_flow:,.0f}")

    st.divider()

    expense_df = df[df["Type"] == "Expense"].copy()

    if not expense_df.empty:
        left, right = st.columns([1.1, 1])

        with left:
            st.subheader("Where did your money go?")
            category_totals = (
                expense_df.groupby("Category", as_index=False)["Amount"]
                .sum()
                .sort_values("Amount", ascending=False)
            )

            fig = px.bar(
                category_totals,
                x="Amount",
                y="Category",
                orientation="h",
                text_auto=".2s",
                color_discrete_sequence=[JADE]
            )
            fig.update_layout(
                height=390,
                plot_bgcolor=WHITE,
                paper_bgcolor=WHITE,
                font_color=INK,
                yaxis={"categoryorder": "total ascending"},
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)

        with right:
            st.subheader("Expense share")
            fig = px.pie(
                category_totals,
                values="Amount",
                names="Category",
                hole=0.6,
                color_discrete_sequence=[
                    GREEN, JADE, GOLD, "#94B5A5",
                    "#C6D3C8", "#A5AEB1", "#B79E84"
                ]
            )
            fig.update_layout(
                height=390,
                paper_bgcolor=WHITE,
                font_color=INK,
                legend_title_text=""
            )
            st.plotly_chart(fig, use_container_width=True)

        st.subheader("Category-wise details")
        category_totals["Share of expenses (%)"] = (
            category_totals["Amount"] / expenses * 100
        ).round(1) if expenses else 0

        st.dataframe(
            category_totals.rename(
                columns={"Amount": "Total spent (₹)"}
            ),
            hide_index=True,
            use_container_width=True
        )

        highest = category_totals.iloc[0]
        st.markdown("### What the numbers tell you")
        st.write(
            f"The highest recorded spending category is **{highest['Category']}**, "
            f"at **₹{highest['Amount']:,.0f}**. Review the transactions in this "
            "category to decide whether any spending can be adjusted."
        )

        if income > 0:
            st.write(
                f"Recorded cash flow after expenses, investments and debt payments "
                f"is **₹{cash_flow:,.0f}**. The calculated ratio is "
                f"**{savings_rate:.1f}% of recorded income**."
            )
        else:
            st.info(
                "Income was not identified in this data. Enter your monthly "
                "income in Monthly Budget Plan to plan a budget."
            )

    else:
        st.info("No rows are marked as Expense. Check transaction types in the review table.")

    st.subheader("Transaction history")
    st.dataframe(
        df.sort_values("Date", ascending=False),
        hide_index=True,
        use_container_width=True
    )

    st.download_button(
        "Export complete analysis data as CSV",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name="financial_analysis.csv",
        mime="text/csv"
    )


elif page == "3. Monthly Budget Plan":
    st.subheader("Monthly Budget Planner")
    st.write(
        "Select one month, review that month's expenses, confirm your commitments, "
        "and create an editable plan for next month."
    )

    source = pd.DataFrame(st.session_state.transactions).copy()

    if source.empty:
        st.warning("Upload and confirm a PDF, or load demo data first.")
        st.stop()

    required = ["Date", "Type", "Category", "Amount", "Description"]
    for col in required:
        if col not in source.columns:
            source[col] = 0.0 if col == "Amount" else ""

    source["Date"] = pd.to_datetime(source["Date"], errors="coerce").dt.date
    source["Amount"] = pd.to_numeric(
        source["Amount"], errors="coerce"
    ).fillna(0).abs()
    source["Type"] = source["Type"].fillna("Transfer / Review").astype(str)
    source["Category"] = source["Category"].fillna("Other").astype(str)

    months = pd.to_datetime(
        source["Date"], errors="coerce"
    ).dt.strftime("%Y-%m")

    available_months = sorted(months.dropna().unique().tolist(), reverse=True)

    if not available_months:
        st.error("No valid transaction dates found. Correct the dates in Upload & Review PDF.")
        st.stop()

    source_name = re.sub(
        r"[^A-Za-z0-9_-]",
        "_",
        str(st.session_state.get("source_name", "session"))
    )[:35] or "session"

    selected_month = st.selectbox(
        "Select the reference month",
        available_months,
        format_func=lambda value: datetime.strptime(
            value, "%Y-%m"
        ).strftime("%B %Y"),
        key=f"budget_reference_v3_{source_name}"
    )

    month_label = datetime.strptime(
        selected_month, "%Y-%m"
    ).strftime("%B %Y")

    month_data = source.loc[months == selected_month].copy()

    st.caption(
        f"Reference month: {month_label}. Use a complete monthly statement "
        "where possible. All defaults below use this month only."
    )

    review_state = st.session_state.get(
        "review_ready", st.session_state.get("confirmed", True)
    )
    if not review_state:
        st.warning("Review and confirm extracted transactions before relying on this plan.")

    if "Review required" in month_data.columns:
        review_flags = month_data["Review required"].fillna(False).astype(bool)
        if review_flags.any():
            st.warning(
                f"{int(review_flags.sum())} transaction(s) need verification. "
                "Correct them in Upload & Review PDF."
            )

    # Prevent older loan/EMI rows from being counted in both expenses and debt.
    loan_category = month_data["Category"].astype(str).str.contains(
        r"loan|emi|debt", case=False, na=False
    )
    old_loan_as_expense = (
        (month_data["Type"] == "Expense") & loan_category
    )
    debt_mask = (
        (month_data["Type"] == "Debt Payment") | old_loan_as_expense
    )
    expense_mask = (
        (month_data["Type"] == "Expense") & ~old_loan_as_expense
    )

    monthly_income_found = float(
        month_data.loc[month_data["Type"] == "Income", "Amount"].sum()
    )
    monthly_debt_found = float(
        month_data.loc[debt_mask, "Amount"].sum()
    )
    monthly_investments_found = float(
        month_data.loc[month_data["Type"] == "Investment", "Amount"].sum()
    )

    expenses = month_data.loc[expense_mask].copy()

    # Transfers and unknown transaction types are excluded until reviewed.
    known_types = ["Income", "Expense", "Investment", "Debt Payment"]
    unknown = month_data.loc[~month_data["Type"].isin(known_types)].copy()

    if not unknown.empty:
        st.warning(
            f"{len(unknown)} transaction(s) are marked Transfer / Review or "
            "another unclassified type. They are excluded from the estimated "
            "remaining balance until reviewed."
        )
        with st.expander("View unclassified transactions"):
            st.dataframe(unknown, use_container_width=True, hide_index=True)
            st.caption(
                "Classify genuine purchases as Expense, genuine income as Income, "
                "and transfers between your own accounts as Transfer / Review."
            )

    if old_loan_as_expense.any():
        st.info(
            "Some loan/EMI rows were labelled Expense. They are treated as debt "
            "payments here to avoid counting them twice. Correct the transaction "
            "type in the review table too."
        )

    if expenses.empty:
        st.warning(
            f"No ordinary expenses were identified in {month_label}. "
            "Review the transaction types or select another month."
        )
        st.stop()

    history = expenses.groupby("Category")["Amount"].sum().sort_index()

    essential_terms = (
        "housing", "rent", "grocer", "utility", "health", "medical",
        "education", "transport", "fuel", "insurance", "electricity",
        "water", "internet", "school", "childcare"
    )

    def explain_target(category):
        name = str(category).strip().lower()

        if name in ("other", "unknown", "uncategorized", "transfer / review", ""):
            return "Review the category; no automatic reduction"

        if any(term in name for term in essential_terms):
            return "Essential/regular cost; start at the recorded level"

        return "Flexible spending; optional 10% lower starting target"

    saved_by_month = st.session_state.get("financial_budget_plans_v3", {})
    saved_targets = saved_by_month.get(selected_month, {})

    rows = []
    for category, actual in history.items():
        category = str(category)
        approach = explain_target(category)

        if approach.startswith("Flexible"):
            suggested = round(float(actual) * 0.90, 2)
        else:
            suggested = round(float(actual), 2)

        suggested = max(0.0, float(saved_targets.get(category, suggested)))

        rows.append({
            "Category": category,
            "Recorded spending (₹)": round(float(actual), 2),
            "Suggested monthly budget (₹)": suggested,
            "Why this target?": approach
        })

    budget_table = pd.DataFrame(rows)

    st.subheader("1. Set realistic category budgets")
    st.caption(
        "Essential categories are not automatically cut. Flexible categories "
        "start with a suggested 10% reduction, which you can change. These are "
        "editable starting targets, not compulsory spending limits."
    )

    editor_key = (
        f"budget_table_v3_{selected_month}_{source_name}_{len(month_data)}"
    )

    edited_plan = st.data_editor(
        budget_table,
        key=editor_key,
        use_container_width=True,
        hide_index=True,
        disabled=["Recorded spending (₹)", "Why this target?"],
        column_config={
            "Category": st.column_config.TextColumn("Category", required=True),
            "Recorded spending (₹)": st.column_config.NumberColumn(
                "Recorded spending (₹)", format="%.2f"
            ),
            "Suggested monthly budget (₹)": st.column_config.NumberColumn(
                "Suggested monthly budget (₹)",
                min_value=0.0,
                format="%.2f",
                required=True
            ),
            "Why this target?": st.column_config.TextColumn("Why this target?")
        }
    )

    actual_amounts = pd.to_numeric(
        edited_plan["Recorded spending (₹)"], errors="coerce"
    ).fillna(0).clip(lower=0)

    targets = pd.to_numeric(
        edited_plan["Suggested monthly budget (₹)"], errors="coerce"
    ).fillna(0).clip(lower=0)

    planned_expenses = float(targets.sum())
    actual_expenses = float(actual_amounts.sum())

    st.markdown("### Manual Budget Entry v3")
    st.caption(
        "AI budget saripokapothe, nee own category and amount ikkada add cheyyachu."
    )

    _manual_month_key = str(selected_month)
    _manual_store = st.session_state.setdefault(
        "financial_manual_budget_items_v3", {}
    )
    _manual_items = _manual_store.setdefault(_manual_month_key, {})

    with st.form(key=f"manual_budget_form_v3_{_manual_month_key}"):
        _manual_category_input = st.text_input(
            "Your category name",
            placeholder="Example: Medical, School Fees, Family Support"
        )
        _manual_amount_input = st.number_input(
            "Monthly budget amount (?)",
            min_value=0.0,
            value=0.0,
            step=500.0
        )
        _manual_add_clicked = st.form_submit_button("Add Manual Category")

    if _manual_add_clicked:
        _new_category = _manual_category_input.strip()
        _ai_categories = {
            str(value).strip().casefold()
            for value in edited_plan["Category"].dropna().tolist()
        }
        _manual_categories = {
            str(value).strip().casefold() for value in _manual_items
        }

        if not _new_category:
            st.warning("Please enter a category name.")
        elif _new_category.casefold() in _ai_categories:
            st.warning(
                "This category already exists in the AI table. "
                "Change its suggested budget there instead."
            )
        elif _new_category.casefold() in _manual_categories:
            st.warning("This manual category already exists.")
        else:
            _manual_items[_new_category] = float(_manual_amount_input)
            _manual_store[_manual_month_key] = _manual_items
            st.success(f"Added '{_new_category}' to your budget.")

    if _manual_items:
        st.markdown("#### Edit or remove manual categories")

        _remove_category = None

        for _idx, _name in enumerate(list(_manual_items.keys())):
            _col1, _col2, _col3 = st.columns([2, 2, 1])

            with _col1:
                st.write(_name)

            with _col2:
                _edited_amount = st.number_input(
                    f"{_name} monthly amount (?)",
                    min_value=0.0,
                    value=float(_manual_items.get(_name, 0.0)),
                    step=500.0,
                    key=f"manual_amount_v3_{_manual_month_key}_{_idx}"
                )
                _manual_items[_name] = float(_edited_amount)

            with _col3:
                if st.button(
                    "Remove",
                    key=f"manual_remove_v3_{_manual_month_key}_{_idx}"
                ):
                    _remove_category = _name

        if _remove_category is not None:
            _manual_items.pop(_remove_category, None)
            _manual_store[_manual_month_key] = _manual_items
            st.rerun()

        _manual_store[_manual_month_key] = _manual_items

        _manual_rows = pd.DataFrame([
            {
                "Category": _name,
                "Recorded spending (?)": 0.0,
                "Suggested monthly budget (?)": float(_amount),
                "Why this target?": "Manually entered by you"
            }
            for _name, _amount in _manual_items.items()
        ])

        edited_plan = pd.concat(
            [edited_plan, _manual_rows],
            ignore_index=True
        )

        # Recalculate totals after adding manual categories.
        actual_amounts = pd.to_numeric(
            edited_plan["Recorded spending (?)"], errors="coerce"
        ).fillna(0).clip(lower=0)

        targets = pd.to_numeric(
            edited_plan["Suggested monthly budget (?)"],
            errors="coerce"
        ).fillna(0).clip(lower=0)

        planned_expenses = float(targets.sum())
        actual_expenses = float(actual_amounts.sum())

    st.subheader("2. Confirm income and financial commitments")
    st.write(
        "The defaults below come from the selected month. If the statement does "
        "not contain all your income or commitments, enter the correct monthly totals."
    )

    c1, c2, c3 = st.columns(3)

    monthly_income = c1.number_input(
        "Monthly take-home income (₹)",
        min_value=0.0,
        value=max(0.0, monthly_income_found),
        step=1000.0,
        key=f"budget_income_v3_{selected_month}_{source_name}"
    )

    monthly_debt = c2.number_input(
        "Monthly loan/debt payments (₹)",
        min_value=0.0,
        value=max(0.0, monthly_debt_found),
        step=500.0,
        key=f"budget_debt_v3_{selected_month}_{source_name}"
    )

    monthly_investment = c3.number_input(
        "Planned monthly investments (₹)",
        min_value=0.0,
        value=max(0.0, monthly_investments_found),
        step=500.0,
        key=f"budget_invest_v3_{selected_month}_{source_name}"
    )

    remaining = (
        monthly_income
        - planned_expenses
        - monthly_debt
        - monthly_investment
    )

    st.subheader("3. Final monthly budget summary")

    m1, m2, m3 = st.columns(3)
    m1.metric("Monthly income", f"₹{monthly_income:,.2f}")
    m2.metric("Planned expenses", f"₹{planned_expenses:,.2f}")
    m3.metric("Loan/debt payments", f"₹{monthly_debt:,.2f}")

    m4, m5 = st.columns(2)
    m4.metric("Planned investments", f"₹{monthly_investment:,.2f}")

    remaining_label = (
        "Potential balance before unclassified items"
        if not unknown.empty else "Potential money remaining"
    )
    m5.metric(remaining_label, f"₹{remaining:,.2f}")

    change = actual_expenses - planned_expenses

    if change >= 0:
        st.caption(
            f"Your proposed category budgets are ₹{change:,.2f} below the "
            f"recorded expenses for {month_label}."
        )
    else:
        st.caption(
            f"Your proposed category budgets are ₹{abs(change):,.2f} above "
            f"recorded expenses for {month_label}."
        )

    if monthly_income <= 0:
        st.warning("Enter your monthly take-home income to check affordability.")
    elif remaining < 0:
        st.error(
            "Your planned expenses, debt payments and investments exceed income. "
            "Review the figures and adjust flexible categories or commitments."
        )
    elif not unknown.empty:
        st.warning(
            f"Approximately ₹{remaining:,.2f} remains before unclassified "
            "transactions. Review those transactions before relying on the balance."
        )
    else:
        st.markdown(
            f"""
            <div style="
                background:#E4F3E8;
                border:1px solid #9AC9A8;
                border-radius:12px;
                padding:18px 20px;
                color:#174C36;
                margin:12px 0;
            ">
                <div style="font-size:20px;font-weight:700;margin-bottom:8px;">
                    ✓ Good to go!
                </div>
                <div style="font-size:15px;line-height:1.7;">
                    Under these assumptions, approximately
                    <strong>₹{remaining:,.2f}</strong> may remain after the
                    listed expenses, debt payments and investments.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.subheader("4. Save or download your plan")

    if st.button(
        "Save category budgets for this month",
        type="primary",
        key=f"save_budget_v3_{selected_month}_{source_name}"
    ):
        plans = st.session_state.get("financial_budget_plans_v3", {})
        plans[selected_month] = dict(zip(
            edited_plan["Category"].fillna("Other").astype(str).tolist(),
            targets.tolist()
        ))
        st.session_state.financial_budget_plans_v3 = plans
        st.success(f"Budget targets for {month_label} saved for this session.")

    download_plan = edited_plan.copy()
    download_plan["Reference month"] = month_label
    download_plan["Monthly income (₹)"] = monthly_income
    download_plan["Loan/debt payments (₹)"] = monthly_debt
    download_plan["Planned investments (₹)"] = monthly_investment
    download_plan["Potential remaining (₹)"] = remaining

    st.download_button(
        "Download monthly budget plan (CSV)",
        data=download_plan.to_csv(index=False).encode("utf-8"),
        file_name=f"financial_planner_budget_{selected_month}.csv",
        mime="text/csv"
    )

    st.info(
        "This plan uses the selected month's recorded expenses. It protects categories "
        "that appear essential and only proposes a modest starting reduction for other "
        "categories. Verify the PDF extraction, income and commitments, and adjust targets "
        "to your real household needs. This is an estimate, not financial advice."
    )
st.divider()
st.caption(
    "Financial Planner | Educational financial analytics. "
    "PDF extraction can be imperfect, so verify transactions before relying on results. "
    "This app does not connect to bank accounts or provide personalized investment advice."
)
