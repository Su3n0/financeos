import streamlit as st
import sqlite3
from datetime import datetime

st.set_page_config(page_title="FinanceOS", layout="wide")

st.title("🏦 FinanceOS — Budget Mensuel")

# -----------------------------
# BASE DE DONNÉES
# -----------------------------
conn = sqlite3.connect("financeos.db", check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    label TEXT,
    amount REAL,
    category TEXT,
    date TEXT
)
""")
conn.commit()

# -----------------------------
# BUDGET MENSUEL
# -----------------------------
st.subheader("🎯 Budget mensuel")

budget = st.number_input("Ton budget mensuel (€)", min_value=0.0, value=1500.0, step=50.0)

# -----------------------------
# AJOUT DÉPENSE
# -----------------------------
st.subheader("➕ Ajouter une dépense")

col1, col2, col3 = st.columns(3)

with col1:
    label = st.text_input("Nom")

with col2:
    amount = st.number_input("Montant (€)", min_value=0.0, step=1.0)

with col3:
    category = st.selectbox("Catégorie", ["Alimentation", "Logement", "Transport", "Loisirs", "Autre"])

if st.button("Ajouter"):
    if label and amount > 0:
        c.execute(
            "INSERT INTO expenses (label, amount, category, date) VALUES (?, ?, ?, ?)",
            (label, amount, category, datetime.now().strftime("%Y-%m-%d %H:%M"))
        )
        conn.commit()
        st.success("Dépense ajoutée ✔")

# -----------------------------
# DONNÉES
# -----------------------------
c.execute("SELECT label, amount, category, date FROM expenses")
data = c.fetchall()

# -----------------------------
# FILTRE MOIS COURANT
# -----------------------------
current_month = datetime.now().strftime("%Y-%m")

monthly_data = [d for d in data if d[3].startswith(current_month)]

total = sum(d[1] for d in monthly_data)

# -----------------------------
# INDICATEURS
# -----------------------------
st.divider()

col1, col2, col3 = st.columns(3)

col1.metric("Dépenses du mois", f"{total:.2f} €")
col2.metric("Budget", f"{budget:.2f} €")

diff = budget - total
col3.metric("Reste", f"{diff:.2f} €")

# -----------------------------
# ALERTES
# -----------------------------
if total > budget:
    st.error("⚠️ Tu as dépassé ton budget ce mois-ci")
elif total > budget * 0.8:
    st.warning("⚠️ Attention, tu approches de ton budget")
else:
    st.success("✔ Budget sous contrôle")

# -----------------------------
# GRAPHIQUES
# -----------------------------
st.subheader("📊 Dépenses du mois")

if monthly_data:
    categories = {}

    for _, amount, category, _ in monthly_data:
        categories[category] = categories.get(category, 0) + amount

    chart_data = [
        {"category": k, "amount": v}
        for k, v in categories.items()
    ]

    st.bar_chart(chart_data, x="category", y="amount")
else:
    st.info("Aucune dépense ce mois-ci")
