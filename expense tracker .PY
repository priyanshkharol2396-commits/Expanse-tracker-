import streamlit as st
import google.generativeai as genai
import pandas as pd
import matplotlib.pyplot as plt
import time

# Setup Google Gemini AI key and model
API_KEY = " api key "
genai.configure(api_key=API_KEY)
chat_model = genai.GenerativeModel("gemini-2.5-flash")

# Initialize or load expense data
if "expense_data" not in st.session_state:
    st.session_state.expense_data = pd.DataFrame(columns=["Category", "Amount"])

# Sidebar: Theme toggle and clear button
with st.sidebar:
    st.header("Control Panel")
    dark_mode = st.checkbox("Dark Mode", value=False, help="Switch app theme")

    if st.button("Reset Expenses"):
        st.session_state.expense_data = pd.DataFrame(columns=["Category", "Amount"])
        st.experimental_rerun()

    st.markdown("Created by Priyansh Kharol | Expense Tracker v1.0")

# Apply theme styles (simple CSS)
dark_css = """
<style>
body {background-color: #121212; color: #ddd;}
.sidebar-content {background-color: #222; color: #eee; font-weight: 600;}
</style>
"""
light_css = """
<style>
body {background-color: #fafafa; color: #222;}
.sidebar-content {background-color: #004080; color: white; font-weight: 600;}
</style>
"""
st.markdown(dark_css if dark_mode else light_css, unsafe_allow_html=True)

# Page title
st.title("Personal Expense Tracker with AI")

# Expense entry form
with st.form("add_expense_form", clear_on_submit=True):
    cat = st.selectbox("Choose category:", ["Food", "Transport", "Entertainment", "Shopping", "Bills", "Others"])
    amt = st.number_input("Amount (₹)", min_value=0.0, format="%.2f")
    add_clicked = st.form_submit_button("Add")

if add_clicked and amt > 0:
    new_row = pd.DataFrame({"Category": [cat], "Amount": [amt]})
    st.session_state.expense_data = pd.concat([st.session_state.expense_data, new_row], ignore_index=True)
    st.success(f"Added ₹{amt:.2f} to {cat}")

# Show current records
st.subheader("Expense Records")
st.dataframe(st.session_state.expense_data)

# Pie chart showing expense distribution
if not st.session_state.expense_data.empty:
    st.subheader("Category-wise Expense")
    fig, ax = plt.subplots()
    summary = st.session_state.expense_data.groupby("Category")["Amount"].sum()
    ax.pie(summary, labels=summary.index, autopct="%1.1f%%", startangle=140)
    st.pyplot(fig)

    # AI tips button
    total = summary.sum()
    budget_prompt = f"Total monthly spending is ₹{total:.2f}. Give me simple budgeting tips to save money."

    if st.button("Ask AI for Budget Tips"):
        with st.spinner("Asking AI for tips..."):
            start = time.time()
            answer = chat_model.generate_content(budget_prompt)
            end = time.time()

            st.markdown("### AI Budgeting Suggestions")
            st.write(answer.text)
            st.info(f"Response received in {end - start:.2f} seconds.")
