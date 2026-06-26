import streamlit as st
import sqlite3
import requests
from datetime import datetime

st.set_page_config(page_title="FinanceOS", layout="wide")

st.title("🏦 FinanceOS — Copilote IA sécurisé")

# -----------------------------
# IA (clé sécurisée via Streamlit Secrets)
# -----------------------------
def ask_ai(prompt):
    API_KEY = st.secrets["OPENAI_API_KEY"]

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": "Tu es un conseiller financier."},
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers=headers,
        json=data
    )

    st.write("DEBUG API RESPONSE:")
    st.write(response.json())  # 👈 IMPORTANT

    return "STOP DEBUG"

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
# DASHBOARD
# -----------------------------
st.divider()

st.subheader("📊 Situation financière")

budget = st.number_input("Budget mensuel (€)", value=1500.0)

col1, col2 = st.columns(2)
col1.metric("Dépenses", f"{total:.2f} €")
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

# -----------------------------
# IA
# -----------------------------
st.divider()

st.subheader("🤖 Copilote IA")

if st.button("💬 Analyser mon budget"):

    summary = f"""
    Situation financière :

    - Dépenses totales : {total:.2f} €
    - Budget mensuel : {budget:.2f} €
    - Reste : {budget - total:.2f} €
    - Nombre de transactions : {len(data)}

    Détail :
    """

    categories = {}
    for _, amount, category in data:
        categories[category] = categories.get(category, 0) + amount

    for k, v in categories.items():
        summary += f"- {k} : {v:.2f} €\n"

    with st.spinner("Analyse de l'IA..."):
        result = ask_ai(summary)

    st.subheader("🧠 Analyse IA")
    st.write(result)
