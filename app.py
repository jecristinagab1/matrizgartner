import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import requests
from io import BytesIO

# ------------------
# CONFIGURAÇÃO INICIAL
# ------------------
st.set_page_config(page_title="Análise de Concorrência", layout="wide")

# Inicializa os dados na sessão do Streamlit
if "concorrentes" not in st.session_state:
    st.session_state.concorrentes = pd.DataFrame(
        [
            ["FluencyPass", 0, 0, "https://i.ibb.co/NVbyMKD/fluency-pass.png"],
            ["Fluency Academy", 0, 0, "https://i.ibb.co/7tRhz0r/fluency-academy.png"],
            ["Open English", 0, 0, "https://i.ibb.co/stC9gr6/open-english.png"],
            ["GoFluent", 0, 0, "https://i.ibb.co/Dkqf08Y/gofluent.png"],
            ["Rosetta", 0, 0, "https://i.ibb.co/HqDKqzg/rosetta.png"],
            ["Voxy", 0, 0, "https://i.ibb.co/bbXm5vN/voxy.png"],
            ["Nulinga", 0, 0, "https://i.ibb.co/xSbgHzW/nulinga.png"],
            ["Berlitz", 0, 0, "https://i.ibb.co/y0TmqmS/berlitz.png"],
            ["Yázigi", 0, 0, "https://i.ibb.co/wM1n1Bh/yazigi.png"],
            ["Flexge", 0, 0, "https://i.ibb.co/cXtpCqy/flexge.png"],
            ["Preply", 0, 0, "https://i.ibb.co/WDJtvmK/preply.png"],
            ["English Live", 0, 0, "https://i.ibb.co/8gyt7HK/english-live.png"],
        ],
        columns=["Concorrente", "Nota Execução", "Nota Visão", "URL Logo"]
    )

# ------------------
# FUNÇÃO PARA GERAR GRÁFICO
# ------------------
def gerar_grafico(df):
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_xlim(1, 5)
    ax.set_ylim(1, 5)
    ax.axhline(y=3, color="gray", linestyle="--", linewidth=1)
    ax.axvline(x=3, color="gray", linestyle="--", linewidth=1)
    ax.set_xlabel("Visão")
    ax.set_ylabel("Execução")
    ax.grid(True, linestyle='--', linewidth=0.5)
    
    for _, row in df.iterrows():
        try:
            response = requests.get(row["URL Logo"])
            img_data = BytesIO(response.content)
            img = plt.imread(img_data, format='png')
            imagebox = OffsetImage(img, zoom=0.2)
            ab = AnnotationBbox(imagebox, (row["Nota Visão"], row["Nota Execução"]), frameon=False)
            ax.add_artist(ab)
        except:
            ax.scatter(row["Nota Visão"], row["Nota Execução"], marker='o', color='blue', s=100)
    
    return fig

# ------------------
# INTERFACE PRINCIPAL
# ------------------
st.title("📊 Análise de Concorrência")
st.subheader("Adicione, edite e visualize o posicionamento dos concorrentes.")

# Formulário para adicionar novos concorrentes
with st.expander("➕ Adicionar Concorrente"):
    novo_nome = st.text_input("Nome do Concorrente")
    nova_exec = st.number_input("Nota Execução", 1.0, 5.0, 3.0, step=0.1)
    nova_visao = st.number_input("Nota Visão", 1.0, 5.0, 3.0, step=0.1)
    nova_url = st.text_input("URL do Logo")
    if st.button("Adicionar"):
        if novo_nome and nova_url:
            st.session_state.concorrentes = pd.concat([
                st.session_state.concorrentes,
                pd.DataFrame([[novo_nome, nova_exec, nova_visao, nova_url]], columns=st.session_state.concorrentes.columns)
            ], ignore_index=True)
            st.success(f"{novo_nome} adicionado!")
            st.experimental_rerun()

# Exibe a tabela editável
st.write("### 📋 Lista de Concorrentes")
st.session_state.concorrentes = st.data_editor(st.session_state.concorrentes, num_rows="dynamic")

# Botão para gerar gráfico
if st.button("📈 Gerar Gráfico"):
    fig = gerar_grafico(st.session_state.concorrentes)
    st.pyplot(fig)

# Baixar o gráfico como imagem
if "grafico_gerado" in st.session_state and st.session_state.grafico_gerado:
    st.download_button("📥 Baixar Gráfico", data=fig.savefig(BytesIO(), format="png"), file_name="grafico.png", mime="image/png")


