import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import requests
from io import BytesIO
import pandas as pd

st.set_page_config(page_title="Matriz de Gartner", layout="wide")

st.title("📊 Matriz de Gartner Interativa")

st.subheader("📌 Insira os concorrentes e suas notas")

definir_dados = {
    "Concorrente": ["FluencyPass", "Fluency Academy", "Open English", "GoFluent", "Rosetta", "Voxy", "Nulinga", "Berlitz", "Yázigi", "Flexge", "Preply", "English Live"],
    "Execução": [None] * 12,
    "Visão": [None] * 12,
    "URL Logo": [
        "https://i.ibb.co/NVbyMKD/fluency-pass.png", "https://i.ibb.co/7tRhz0r/fluency-academy.png", "https://i.ibb.co/stC9gr6/open-english.png",
        "https://i.ibb.co/Dkqf08Y/gofluent.png", "https://i.ibb.co/HqDKqzg/rosetta.png", "https://i.ibb.co/bbXm5vN/voxy.png", "https://i.ibb.co/xSbgHzW/nulinga.png",
        "https://i.ibb.co/y0TmqmS/berlitz.png", "https://i.ibb.co/wM1n1Bh/yazigi.png", "https://i.ibb.co/cXtpCqy/flexge.png", "https://i.ibb.co/WDJtvmK/preply.png", "https://i.ibb.co/8gyt7HK/english-live.png"
    ]
}
df = st.data_editor(pd.DataFrame(definir_dados), num_rows="dynamic")

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

if st.button("📈 Gerar Matriz de Gartner"):
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
        nome, exec_val, visao_val, url_logo = row
        if exec_val is None or visao_val is None:
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
