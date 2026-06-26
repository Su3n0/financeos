import streamlit as st
import sqlite3
from datetime import datetime

st.set_page_config(page_title="FinanceOS", layout="wide")

st.title("🏦 FinanceOS — Budget + Graphiques")

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
c.execute("SELECT label, amount, category FROM expenses")
data = c.fetchall()

# -----------------------------
# RÉSUMÉ
# -----------------------------
st.divider()

st.subheader("📊 Résumé")

total = sum(row[1] for row in data)

col1, col2 = st.columns(2)
col1.metric("Total dépenses", f"{total:.2f} €")
col2.metric("Nombre d'opérations", len(data))

# -----------------------------
# GRAPHIQUE 1 : PAR CATÉGORIE (camembert)
# -----------------------------
st.subheader("🥧 Répartition des dépenses")

if data:
    categories = {}
    for _, amount, category in data:
        categories[category] = categories.get(category, 0) + amount

    chart_data = [
        {"category": k, "amount": v}
        for k, v in categories.items()
    ]

    st.bar_chart(chart_data, x="category", y="amount")

# -----------------------------
# GRAPHIQUE 2 : LISTE DES DÉPENSES
# -----------------------------
st.subheader("📊 Dépenses individuelles")

if data:
    chart_data2 = [
        {"label": d[0], "amount": d[1]}
        for d in data
    ]

    st.bar_chart(chart_data2, x="label", y="amount")
else:
    st.info("Aucune donnée")
