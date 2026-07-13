from datetime import datetime


def generate_report(metrics, subscriptions, ai_suggestions):
    """
    Generate a downloadable text report.
    """

    report = []

    report.append("=" * 60)
    report.append("        SUBSCRIPTION WASTE DETECTOR REPORT")
    report.append("=" * 60)

    report.append(f"\nGenerated On : {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}")

    report.append("\n" + "=" * 60)
    report.append("DASHBOARD SUMMARY")
    report.append("=" * 60)

    report.append(f"Total Spending        : ₹{metrics['total_spending']:.2f}")
    report.append(f"Active Subscriptions  : {metrics['active_subscriptions']}")
    report.append(f"Possible Savings      : ₹{metrics['possible_savings']:.2f}")

    report.append("\n" + "=" * 60)
    report.append("DETECTED SUBSCRIPTIONS")
    report.append("=" * 60)

    if subscriptions.empty:
        report.append("No subscriptions detected.")
    else:
        for _, row in subscriptions.iterrows():
            report.append(
                f"{row['Description']} | ₹{row['Amount']} | {row['Category']}"
            )

    report.append("\n" + "=" * 60)
    report.append("AI COST-SAVING SUGGESTIONS")
    report.append("=" * 60)

    report.append(ai_suggestions)

    report.append("\n" + "=" * 60)
    report.append("END OF REPORT")
    report.append("=" * 60)

    return "\n".join(report)