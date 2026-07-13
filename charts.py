import pandas as pd
import plotly.express as px


def create_donut_chart(df):
    """
    Donut chart showing spending by subscription.
    """

    if df.empty:
        return None

    summary = (
        df.groupby("Description", as_index=False)["Amount"]
        .sum()
    )

    fig = px.pie(
        summary,
        names="Description",
        values="Amount",
        hole=0.55,
        title="Subscription Spending Distribution"
    )

    fig.update_traces(
        textposition="inside",
        textinfo="percent+label"
    )

    fig.update_layout(
        legend_title="Subscriptions",
        margin=dict(t=60, l=20, r=20, b=20)
    )

    return fig


def create_category_chart(df):
    """
    Bar chart showing spending by category.
    """

    if df.empty:
        return None

    summary = (
        df.groupby("Category", as_index=False)["Amount"]
        .sum()
    )

    fig = px.bar(
        summary,
        x="Category",
        y="Amount",
        color="Category",
        text="Amount",
        title="Monthly Spending by Category"
    )

    fig.update_traces(texttemplate="₹%{text:.0f}")

    fig.update_layout(
        xaxis_title="Category",
        yaxis_title="Amount (₹)"
    )

    return fig


def create_monthly_trend(df):
    """
    Monthly spending trend.
    """

    if df.empty:
        return None

    data = df.copy()

    data["Month"] = pd.to_datetime(data["Date"]).dt.to_period("M").astype(str)

    summary = (
        data.groupby("Month", as_index=False)["Amount"]
        .sum()
    )

    fig = px.line(
        summary,
        x="Month",
        y="Amount",
        markers=True,
        title="Monthly Subscription Spending"
    )

    fig.update_layout(
        xaxis_title="Month",
        yaxis_title="Amount (₹)"
    )

    return fig