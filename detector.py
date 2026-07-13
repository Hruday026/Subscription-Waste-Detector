import pandas as pd

# Known subscription services
KNOWN_SUBSCRIPTIONS = [
    "Netflix",
    "Spotify",
    "ChatGPT",
    "Adobe",
    "Amazon Prime",
    "YouTube Premium",
    "Disney+",
    "Apple Music",
    "Google One",
    "Microsoft 365",
    "Canva",
    "JioHotstar",
    "Amazon Music",
    "Hotstar"
]


def detect_subscriptions(df):
    """
    Detect known subscriptions and recurring payments.
    """

    data = df.copy()

    # Detect known services
    data["KnownSubscription"] = data["Description"].str.lower().apply(
        lambda x: any(service.lower() in x for service in KNOWN_SUBSCRIPTIONS)
    )

    # Detect recurring transactions
    recurring = (
        data.groupby(["Description", "Amount"])
        .size()
        .reset_index(name="Count")
    )

    recurring = recurring[recurring["Count"] >= 2]

    recurring["Recurring"] = True

    data = data.merge(
        recurring[["Description", "Amount", "Recurring"]],
        on=["Description", "Amount"],
        how="left"
    )

    data["Recurring"] = data["Recurring"].fillna(False)

    data = data[
        (data["KnownSubscription"]) |
        (data["Recurring"])
    ].copy()

    return data.reset_index(drop=True)


def classify_subscription(amount):
    """
    Cost category.
    """

    if amount < 300:
        return "Low"

    elif amount < 1000:
        return "Medium"

    else:
        return "High"


def add_category(df):
    """
    Add Low / Medium / High category.
    """

    df = df.copy()

    df["Category"] = df["Amount"].apply(classify_subscription)

    return df


def calculate_metrics(df):
    """
    Dashboard metrics.
    """

    total_spending = float(df["Amount"].sum())

    active_subscriptions = df["Description"].nunique()

    possible_savings = float(
        df[df["Category"] == "High"]["Amount"].sum()
    )

    return {
        "total_spending": total_spending,
        "active_subscriptions": active_subscriptions,
        "possible_savings": possible_savings
    }


def get_upcoming_renewals(df, days=7):
    """
    Renewal reminders.
    """

    today = pd.Timestamp.today().normalize()

    reminders = []

    for _, row in df.iterrows():

        if pd.isna(row["RenewalDate"]):
            continue

        renewal = pd.to_datetime(row["RenewalDate"]).normalize()

        diff = (renewal - today).days

        if 0 <= diff <= days:

            reminders.append({
                "Description": row["Description"],
                "RenewalDate": renewal.strftime("%Y-%m-%d"),
                "DaysLeft": diff
            })

    return reminders