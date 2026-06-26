import streamlit as st
import sqlite3
from datetime import datetime

st.set_page_config(page_title="FinanceOS", layout="wide")

st.title("🏦 FinanceOS — Budget (version sauvegardée)")

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
        st.success("Dépense enregistrée ✔")
    else:
        st.warning("Remplis correctement les champs")

# -----------------------------
# LECTURE DONNÉES
# -----------------------------
c.execute("SELECT label, amount, category, date FROM expenses ORDER BY id DESC")
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
# HISTORIQUE
# -----------------------------
st.divider()

st.subheader("📋 Historique")

if data:
    for d in data:
        st.write(f"• {d[0]} — {d[1]} € ({d[2]}) — {d[3]}")
else:
    st.info("Aucune dépense enregistrée")
