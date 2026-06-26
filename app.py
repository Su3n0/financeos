import streamlit as st
import sqlite3
from datetime import datetime

st.set_page_config(page_title="FinanceOS", layout="wide")

st.title("🏦 FinanceOS — IA locale intelligente")

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
    label = st.text_input("Nom de la dépense")

with col2:
    amount = st.number_input("Montant (€)", min_value=0.0, step=1.0)

with col3:
    category = st.selectbox(
        "Catégorie",
        ["Alimentation", "Logement", "Transport", "Loisirs", "Autre"]
    )

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
# BUDGET
# -----------------------------
st.divider()

st.subheader("📊 Budget mensuel")

budget = st.number_input("Budget mensuel (€)", value=1500.0, step=50.0)

col1, col2 = st.columns(2)
col1.metric("Dépenses totales", f"{total:.2f} €")
col2.metric("Reste", f"{budget - total:.2f} €")

# -----------------------------
# GRAPHIQUES
# -----------------------------
st.subheader("📊 Répartition des dépenses")

if data:
    categories = {}

    for _, amount, category in data:
        categories[category] = categories.get(category, 0) + amount

    chart_data = [
        {"category": k, "amount": v}
        for k, v in categories.items()
    ]

    st.bar_chart(chart_data, x="category", y="amount")
else:
    st.info("Aucune dépense enregistrée")

# -----------------------------
# IA LOCALE SIMULÉE
# -----------------------------
st.divider()

st.subheader("🤖 Copilote financier (IA locale)")

def ask_ai(total, budget, data):
    categories = {}
    for _, amount, category in data:
        categories[category] = categories.get(category, 0) + amount

    percent_used = (total / budget) * 100 if budget > 0 else 0
    top_category = max(categories, key=categories.get) if categories else None

    if total == 0:
        return "Tu n’as encore aucune dépense. Ajoute des transactions pour obtenir une analyse."

    message = "🧠 Analyse financière intelligente :\n\n"

    # Situation globale
    if percent_used > 100:
        message += "⚠️ Tu as dépassé ton budget mensuel.\n\n"
    elif percent_used > 80:
        message += "⚠️ Tu es proche de ton budget.\n\n"
    elif percent_used > 50:
        message += "⚖️ Dépenses modérées, surveille ton rythme.\n\n"
    else:
        message += "✔ Bonne gestion de ton budget.\n\n"

    # Catégorie principale
    if top_category:
        message += f"📊 Dépense principale : {top_category}\n\n"

        if top_category == "Loisirs":
            message += "💡 Conseil : surveille tes dépenses loisirs.\n"
        elif top_category == "Alimentation":
            message += "💡 Conseil : optimise tes achats alimentaires.\n"
        elif top_category == "Logement":
            message += "💡 Conseil : dépense fixe importante à surveiller.\n"
        else:
            message += "💡 Conseil : équilibre tes dépenses.\n"

    # Épargne
    savings = budget - total

    if savings > 0:
        message += f"\n💰 Épargne possible ce mois-ci : {savings:.2f} €"
    else:
        message += "\n💰 Tu es en déficit ce mois-ci."

    return message


if st.button("💬 Analyser ma situation"):

    with st.spinner("Analyse en cours..."):
        result = ask_ai(total, budget, data)

    st.subheader("🧠 Résultat de l’IA")
    st.write(result)
