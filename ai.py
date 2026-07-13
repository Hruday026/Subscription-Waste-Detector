def get_ai_suggestions(subscriptions):
    """
    Generate offline AI-like cost-saving suggestions.
    """

    if subscriptions.empty:
        return "No subscriptions detected."

    suggestions = []

    total = subscriptions["Amount"].sum()

    suggestions.append("💡 AI Cost-Saving Suggestions\n")

    # High-cost subscriptions
    high = subscriptions[subscriptions["Category"] == "High"]

    if not high.empty:
        suggestions.append("High Monthly Expenses:")
        for _, row in high.iterrows():
            suggestions.append(
                f"- {row['Description']} (₹{row['Amount']:.2f}) "
                "→ Review if you still use it regularly."
            )

    # Medium-cost subscriptions
    medium = subscriptions[subscriptions["Category"] == "Medium"]

    if not medium.empty:
        suggestions.append("\nMedium Monthly Expenses:")
        for _, row in medium.iterrows():
            suggestions.append(
                f"- {row['Description']} "
                "→ Consider switching to a family or student plan."
            )

    # Low-cost subscriptions
    low = subscriptions[subscriptions["Category"] == "Low"]

    if not low.empty:
        suggestions.append(
            "\nLow-cost subscriptions are generally affordable, "
            "but review whether you actively use them."
        )

    suggestions.append("\nGeneral Recommendations:")

    suggestions.append(
        "- Cancel subscriptions you haven't used in the last month."
    )

    suggestions.append(
        "- Bundle streaming services where possible."
    )

    suggestions.append(
        "- Use annual plans if they provide better value."
    )

    suggestions.append(
        "- Check renewal reminders before each billing cycle."
    )

    suggestions.append(
        f"\nEstimated Monthly Subscription Spending: ₹{total:.2f}"
    )

    return "\n".join(suggestions)