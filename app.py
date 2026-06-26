import streamlit as st

st.set_page_config(page_title="FinanceOS", layout="wide")

st.title("🏦 FinanceOS")

st.subheader("Ton cockpit financier")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Patrimoine net", "0 €")
col2.metric("Cash", "0 €")
col3.metric("ETF", "0 €")
col4.metric("Immobilier", "0 €")

st.divider()

st.write("🤖 Assistant financier")
st.info("FinanceOS est prêt. Prochaine étape : budget et suivi des dépenses.")
