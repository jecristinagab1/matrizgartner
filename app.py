import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import requests
from io import BytesIO

st.set_page_config(page_title="Matriz de Gartner", layout="wide")

st.title("📊 Matriz de Gartner Interativa")

# Dados iniciais
dados_iniciais = [
    ["FluencyPass", 3.4, 3.0, "https://i.ibb.co/NVbyMKD/fluency-pass.png"],
    ["Fluency Academy", 3.2, 3.0, "https://i.ibb.co/7tRhz0r/fluency-academy.png"],
    ["Open English", 4.0, 4.0, "https://i.ibb.co/stC9gr6/open-english.png"],
    ["GoFluent", 3.0, 3.2, "https://i.ibb.co/Dkqf08Y/gofluent.png"],
    ["Rosetta", 2.4, 2.6, "https://i.ibb.co/HqDKqzg/rosetta.png"],
    ["Voxy", 3.6, 4.0, "https://i.ibb.co/bbXm5vN/voxy.png"],
    ["Nulinga", 2.6, 2.4, "https://i.ibb.co/xSbgHzW/nulinga.png"],
    ["Berlitz", 2.8, 3.0, "https://i.ibb.co/y0TmqmS/berlitz.png"],
    ["Yázigi", 2.8, 2.4, "https://i.ibb.co/wM1n1Bh/yazigi.png"],
    ["Flexge", 3.2, 2.8, "https://i.ibb.co/cXtpCqy/flexge.png"],
    ["Preply", 3.6, 2.8, "https://i.ibb.co/WDJtvmK/preply.png"],
    ["English Live", 4.6, 3.8, "https://i.ibb.co/8gyt7HK/english-live.png"]
]

df = pd.DataFrame(dados_iniciais, columns=["Concorrente", "Nota Execução", "Nota Visão", "URL Logo"])

df = st.data_editor(df, num_rows="dynamic")

# Função para carregar imagem
@st.cache_data
def carregar_imagem(url_logo):
    if not url_logo:
        return None
    try:
        response = requests.get(url_logo)
        img_data = BytesIO(response.content)
        return OffsetImage(plt.imread(img_data, format='png'), zoom=0.20)
    except:
        return None

# Layout dos botões
col1, col2, col3 = st.columns([2, 2, 4])
with col1:
    gerar_grafico = st.button("📈 Gerar gráfico", key="gerar_grafico")
with col2:
    adicionar_concorrente = st.button("➕ Adicionar concorrente", key="adicionar")
with col3:
    colar_notas = st.button("📋 Colar Notas (Exec, Visão)", key="colar_notas")

if gerar_grafico:
    st.subheader("📊 Gráfico da Matriz de Gartner")
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_xlim(1, 5)
    ax.set_ylim(1, 5)
    ax.axhline(y=3, color="gray", linestyle="--", linewidth=1)
    ax.axvline(x=3, color="gray", linestyle="--", linewidth=1)
    ax.set_xlabel("Visão")
    ax.set_ylabel("Execução")
    ax.grid(True, linestyle='--', linewidth=0.5)

    for _, row in df.iterrows():
        try:
            exec_val = float(row["Nota Execução"])
            visao_val = float(row["Nota Visão"])
            url_logo = row["URL Logo"]
            nome = row["Concorrente"]
        except ValueError:
            continue
        
        cor = "green" if exec_val > 3 and visao_val > 3 else "red" if exec_val <= 3 and visao_val <= 3 else "orange" if exec_val > 3 else "blue"
        img = carregar_imagem(url_logo)
        if img:
            ab = AnnotationBbox(img, (visao_val, exec_val), frameon=False)
            ax.add_artist(ab)
        else:
            ax.plot(visao_val, exec_val, marker='o', color=cor, markersize=10)
        ax.text(visao_val + 0.1, exec_val, nome, fontsize=9)
    
    st.pyplot(fig)
    st.download_button("📥 Baixar Imagem", fig.savefig, file_name="matriz_gartner.png", mime="image/png")

