import streamlit as st
import pandas as pd
from datetime import date

from utils import load_file, load_sample_data, add_subscription
from detector import (
    detect_subscriptions,
    add_category,
    calculate_metrics,
    get_upcoming_renewals,
)
from charts import (
    create_donut_chart,
    create_category_chart,
    create_monthly_trend,
)
from ai import get_ai_suggestions
from report import generate_report


st.set_page_config(
    page_title="Subscription Waste Detector",
    page_icon="💳",
    layout="wide"
)

st.title("💳 Subscription Waste Detector")
st.markdown(
    "Detect recurring subscriptions, monitor spending, and reduce unnecessary expenses."
)

# -------------------------------
# SESSION STATE
# -------------------------------

if "manual_df" not in st.session_state:
    st.session_state.manual_df = pd.DataFrame(
        columns=[
            "Date",
            "Description",
            "Amount",
            "RenewalDate"
        ]
    )

# -------------------------------
# SIDEBAR
# -------------------------------

st.sidebar.header("📂 Upload Expenses")

uploaded_file = st.sidebar.file_uploader(
    "Upload CSV or Excel",
    type=["csv", "xlsx"]
)

st.sidebar.markdown("---")

st.sidebar.header("➕ Add Subscription")

description = st.sidebar.text_input(
    "Subscription Name"
)

amount = st.sidebar.number_input(
    "Monthly Cost (₹)",
    min_value=0.0,
    step=10.0
)

renewal = st.sidebar.date_input(
    "Renewal Date",
    value=date.today()
)

if st.sidebar.button("Add Subscription"):

    st.session_state.manual_df = add_subscription(
        st.session_state.manual_df,
        description,
        amount,
        renewal
    )

    st.sidebar.success("Subscription Added!")

# -------------------------------
# LOAD DATA
# -------------------------------

if uploaded_file:

    df = load_file(uploaded_file)

else:

    df = load_sample_data()

# Merge manually added subscriptions

if not st.session_state.manual_df.empty:

    df = pd.concat(
        [df, st.session_state.manual_df],
        ignore_index=True
    )

# -------------------------------
# DETECT SUBSCRIPTIONS
# -------------------------------

subscriptions = detect_subscriptions(df)

subscriptions = add_category(subscriptions)

metrics = calculate_metrics(subscriptions)

# -------------------------------
# METRIC CARDS
# -------------------------------

st.subheader("📊 Dashboard")

c1, c2, c3 = st.columns(3)

with c1:
    st.metric(
        "💰 Total Spending",
        f"₹{metrics['total_spending']:.2f}"
    )

with c2:
    st.metric(
        "📦 Active Subscriptions",
        metrics["active_subscriptions"]
    )

with c3:
    st.metric(
        "💸 Possible Savings",
        f"₹{metrics['possible_savings']:.2f}"
    )

st.markdown("---")
# =====================================================
# DETECTED SUBSCRIPTIONS
# =====================================================

st.subheader("📋 Detected Subscriptions")

left_col, right_col = st.columns([1.2, 1])

with left_col:

    if subscriptions.empty:

        st.warning("No subscriptions detected.")

    else:

        for _, row in subscriptions.iterrows():

            if row["Category"] == "Low":
                color = "#d4edda"
                emoji = "🟢"

            elif row["Category"] == "Medium":
                color = "#fff3cd"
                emoji = "🟡"

            else:
                color = "#f8d7da"
                emoji = "🔴"

            st.markdown(
                f"""
<div style="
padding:15px;
margin-bottom:10px;
border-radius:10px;
background-color:{color};
border-left:8px solid gray;
">

<h4>{emoji} {row['Description']}</h4>

<b>Monthly Cost:</b> ₹{row['Amount']:.2f}<br>
<b>Category:</b> {row['Category']}

</div>
""",
                unsafe_allow_html=True
            )

# =====================================================
# DONUT CHART
# =====================================================

with right_col:

    st.subheader("🍩 Spending Distribution")

    donut = create_donut_chart(subscriptions)

    if donut is not None:
        st.plotly_chart(
            donut,
            use_container_width=True
        )

st.markdown("---")

# =====================================================
# CATEGORY BAR CHART
# =====================================================

st.subheader("📊 Spending by Category")

bar = create_category_chart(subscriptions)

if bar is not None:

    st.plotly_chart(
        bar,
        use_container_width=True
    )

st.markdown("---")

# =====================================================
# MONTHLY TREND
# =====================================================

st.subheader("📈 Monthly Spending Trend")

trend = create_monthly_trend(subscriptions)

if trend is not None:

    st.plotly_chart(
        trend,
        use_container_width=True
    )

st.markdown("---")

# =====================================================
# RENEWAL REMINDERS
# =====================================================

st.subheader("⏰ Upcoming Renewals")

renewals = get_upcoming_renewals(subscriptions)

if renewals:

    for item in renewals:

        st.warning(
            f"⚠️ {item['Description']} renews in "
            f"{item['DaysLeft']} day(s) "
            f"on {item['RenewalDate']}"
        )

else:

    st.success("✅ No subscriptions renewing within the next 7 days.")

st.markdown("---")
# =====================================================
# AI COST-SAVING SUGGESTIONS
# =====================================================

st.subheader("🤖 AI Cost-Saving Suggestions")

ai_response = get_ai_suggestions(subscriptions)

with st.expander("Click to View AI Suggestions"):

    st.write(ai_response)

st.markdown("---")

# =====================================================
# DOWNLOAD REPORT
# =====================================================

st.subheader("📄 Download Report")

report = generate_report(
    metrics,
    subscriptions,
    ai_response
)

st.download_button(
    label="⬇️ Download Report",
    data=report,
    file_name="Subscription_Report.txt",
    mime="text/plain"
)

st.markdown("---")

# =====================================================
# RAW DATA
# =====================================================

st.subheader("📋 Raw Subscription Data")

st.dataframe(
    subscriptions,
    use_container_width=True
)

st.markdown("---")

# =====================================================
# PROJECT SUMMARY
# =====================================================

st.success("✅ Analysis Completed Successfully!")

st.markdown(
"""
### Features Included

- 📂 CSV / Excel Upload
- ➕ Manual Subscription Entry
- 🔍 Automatic Subscription Detection
- 💰 Dashboard Metrics
- 📋 Color-Coded Subscription Cards
- 🍩 Spending Distribution Chart
- 📊 Spending Category Chart
- 📈 Monthly Spending Trend
- ⏰ Renewal Reminders
- 🤖 AI Cost-Saving Suggestions (Offline)
- 📄 Download Report
- 📋 Raw Data Viewer

---
Developed using **Python**, **Streamlit**, **Pandas**, and **Plotly**.

SmartBridge Project - Subscription Waste Detector
"""
)