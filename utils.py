import pandas as pd


REQUIRED_COLUMNS = [
    "Date",
    "Description",
    "Amount",
    "RenewalDate"
]


def load_file(uploaded_file):
    """
    Load CSV or Excel file.
    """

    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)

    elif uploaded_file.name.endswith(".xlsx"):
        df = pd.read_excel(uploaded_file)

    else:
        raise ValueError("Only CSV and Excel files are supported.")

    return clean_data(df)


def load_sample_data():
    """
    Load sample data from data/sample.csv
    """

    df = pd.read_csv("data/sample.csv")

    return clean_data(df)


def clean_data(df):
    """
    Standardize the dataframe.
    """

    df.columns = df.columns.str.strip()

    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]

    if missing:
        raise ValueError(
            f"Missing columns: {', '.join(missing)}"
        )

    df["Date"] = pd.to_datetime(df["Date"])

    df["RenewalDate"] = pd.to_datetime(
        df["RenewalDate"],
        errors="coerce"
    )

    df["Amount"] = pd.to_numeric(
        df["Amount"],
        errors="coerce"
    )

    df = df.dropna(subset=["Description", "Amount"])

    df = df.reset_index(drop=True)

    return df


def add_subscription(
    df,
    description,
    amount,
    renewal_date
):
    """
    Add a manually entered subscription.
    """

    new_row = pd.DataFrame({
        "Date": [pd.Timestamp.today()],
        "Description": [description],
        "Amount": [amount],
        "RenewalDate": [renewal_date]
    })

    df = pd.concat(
        [df, new_row],
        ignore_index=True
    )

    return df