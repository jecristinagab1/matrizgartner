import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import requests
from io import BytesIO

st.set_page_config(page_title="Matriz de Gartner", layout="wide")

st.title("📊 Matriz de Gartner Interativa")

# Inicializa ou recupera os dados
if "df" not in st.session_state:
    dados_iniciais = [
        ["FluencyPass", None, None, "https://i.ibb.co/NVbyMKD/fluency-pass.png"],
        ["Fluency Academy", None, None, "https://i.ibb.co/7tRhz0r/fluency-academy.png"],
        ["Open English", None, None, "https://i.ibb.co/stC9gr6/open-english.png"],
        ["GoFluent", None, None, "https://i.ibb.co/Dkqf08Y/gofluent.png"],
        ["Rosetta", None, None, "https://i.ibb.co/HqDKqzg/rosetta.png"],
        ["Voxy", None, None, "https://i.ibb.co/bbXm5vN/voxy.png"],
        ["Nulinga", None, None, "https://i.ibb.co/xSbgHzW/nulinga.png"],
        ["Berlitz", None, None, "https://i.ibb.co/y0TmqmS/berlitz.png"],
        ["Yázigi", None, None, "https://i.ibb.co/wM1n1Bh/yazigi.png"],
        ["Flexge", None, None, "https://i.ibb.co/cXtpCqy/flexge.png"],
        ["Preply", None, None, "https://i.ibb.co/WDJtvmK/preply.png"],
        ["English Live", None, None, "https://i.ibb.co/8gyt7HK/english-live.png"]
    ]
    st.session_state.df = pd.DataFrame(dados_iniciais, columns=["Concorrente", "Nota Execução", "Nota Visão", "URL Logo"])

df = st.session_state.df

# Editor de dados
df = st.data_editor(df, num_rows="dynamic")

# Corrige colagem de notas com vírgula
for col in ["Nota Execução", "Nota Visão"]:
    df[col] = df[col].astype(str).replace("None", "").str.replace(",", ".", regex=True)
    df[col] = pd.to_numeric(df[col], errors='coerce').astype("Float64")

st.session_state.df = df

# Função para carregar imagem
@st.cache_data
def carregar_imagem(url_logo):
    if not url_logo:
        return None
    try:
        response = requests.get(url_logo)
        img_data = BytesIO(response.content)
        return OffsetImage(plt.imread(img_data, format='png'), zoom=0.08)  # Reduz tamanho do logo
    except:
        return None

# Gerar gráfico
if st.button("📈 Gerar gráfico"):
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
            exec_val = float(row["Nota Execução"]) if pd.notna(row["Nota Execução"]) else None
            visao_val = float(row["Nota Visão"]) if pd.notna(row["Nota Visão"]) else None
            url_logo = row["URL Logo"]
            if exec_val is None or visao_val is None:
                continue
        except ValueError:
            continue
        
        img = carregar_imagem(url_logo)
        if img:
            ab = AnnotationBbox(img, (visao_val, exec_val), frameon=False)
            ax.add_artist(ab)
    
    st.pyplot(fig)
    
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("⬅️ Voltar"):
            st.experimental_rerun()
    with col2:
        img_bytes = BytesIO()
        fig.savefig(img_bytes, format='png')
        img_bytes.seek(0)
        st.download_button("📥 Salvar imagem", img_bytes, file_name="matriz_gartner.png", mime="image/png")


