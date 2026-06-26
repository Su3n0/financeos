import streamlit as st

st.set_page_config(page_title="FinanceOS", layout="wide")

st.title("🏦 FinanceOS — Budget")

# -----------------------------
# INITIALISATION
# -----------------------------
if "expenses" not in st.session_state:
    st.session_state.expenses = []

# -----------------------------
# AJOUT DÉPENSE
# -----------------------------
st.subheader("➕ Ajouter une dépense")

col1, col2, col3 = st.columns(3)

with col1:
    label = st.text_input("Nom (ex: courses, loyer)")

with col2:
    amount = st.number_input("Montant (€)", min_value=0.0, step=1.0)

with col3:
    category = st.selectbox("Catégorie", ["Alimentation", "Logement", "Transport", "Loisirs", "Autre"])

if st.button("Ajouter"):
    if label and amount > 0:
        st.session_state.expenses.append({
            "label": label,
            "amount": amount,
            "category": category
        })
        st.success("Dépense ajoutée ✔")
    else:
        st.warning("Remplis le nom et le montant")

# -----------------------------
# AFFICHAGE BUDGET
# -----------------------------
st.divider()

st.subheader("📊 Résumé")

total = sum(e["amount"] for e in st.session_state.expenses)

col1, col2 = st.columns(2)

col1.metric("Total dépenses", f"{total:.2f} €")
col2.metric("Nombre d'opérations", len(st.session_state.expenses))

# -----------------------------
# LISTE DÉPENSES
# -----------------------------
st.divider()

st.subheader("📋 Historique")

if st.session_state.expenses:
    for e in reversed(st.session_state.expenses):
        st.write(f"• {e['label']} — {e['amount']} € ({e['category']})")
else:
    st.info("Aucune dépense enregistrée pour le moment.")
