import streamlit as st
import sqlite3
from datetime import datetime

st.set_page_config(page_title="FinanceOS", layout="wide")

st.title("🏦 FinanceOS — Copilote IA")

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

total = sum(d[1] for d in data)

# -----------------------------
# RÉSUMÉ
# -----------------------------
st.divider()

st.subheader("📊 Situation financière")

st.metric("Total dépenses", f"{total:.2f} €")
st.metric("Nombre d'opérations", len(data))

# -----------------------------
# IA COPILOTE
# -----------------------------
st.divider()

st.subheader("🤖 Copilote financier IA")

budget = st.number_input("Ton budget mensuel (€)", value=1500.0)

if st.button("Analyser ma situation"):

    # -----------------------------
    # ON CRÉE UN RÉSUMÉ SIMPLE (TRÈS IMPORTANT)
    # -----------------------------
    summary = f"""
    Situation financière de l'utilisateur :

    - Dépenses totales : {total:.2f} €
    - Nombre de transactions : {len(data)}
    - Budget mensuel : {budget:.2f} €
    - Reste : {budget - total:.2f} €

    Répartition :
    """

    categories = {}
    for _, amount, category in data:
        categories[category] = categories.get(category, 0) + amount

    for k, v in categories.items():
        summary += f"- {k} : {v:.2f} €\n"

    # -----------------------------
    # SIMULATION IA (VERSION GRATUITE SIMPLE)
    # -----------------------------
    st.subheader("Analyse IA")

    if total > budget:
        st.error("⚠️ Tu dépenses plus que ton budget.")
        st.write("👉 Priorité : réduire les dépenses non essentielles.")
        st.write("👉 Risque : déséquilibre financier.")
    elif total > budget * 0.8:
        st.warning("⚠️ Tu es proche de ton budget.")
        st.write("👉 Attention aux dépenses variables.")
    else:
        st.success("✔ Situation saine.")
        st.write("👉 Tu peux envisager d’investir une partie de ton surplus.")

    st.divider()

    st.subheader("Résumé généré pour IA (version future ChatGPT)")
    st.text(summary)
