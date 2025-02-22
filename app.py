import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import requests
from io import BytesIO

# Configuração da página
st.set_page_config(page_title="Análise de Concorrência", layout="wide")

# Inicialização do estado
if "concorrentes" not in st.session_state:
    st.session_state.concorrentes = pd.DataFrame(
        columns=["Concorrente", "Nota Execução", "Nota Visão", "URL Logo"]
    )

if "gerar_grafico" not in st.session_state:
    st.session_state.gerar_grafico = False

# Função para gerar o gráfico
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

# Título e descrição
st.title("📊 Análise de Concorrência")
st.subheader("Adicione, edite e visualize o posicionamento dos concorrentes.")

# Adicionar novo concorrente
with st.expander("➕ Adicionar Concorrente"):
    novo_nome = st.text_input("Nome do Concorrente")
    nova_exec = st.number_input("Nota Execução", 1.0, 5.0, 3.0, step=0.1)
    nova_visao = st.number_input("Nota Visão", 1.0, 5.0, 3.0, step=0.1)
    nova_url = st.text_input("URL do Logo")
    
    if st.button("Adicionar"):
        if novo_nome and nova_url:
            novo_concorrente = pd.DataFrame(
                [[novo_nome, nova_exec, nova_visao, nova_url]],
                columns=st.session_state.concorrentes.columns
            )
            st.session_state.concorrentes = pd.concat([
                st.session_state.concorrentes, novo_concorrente
            ], ignore_index=True)
            st.success("Concorrente adicionado com sucesso!")

# Lista de concorrentes
st.write("### 📋 Lista de Concorrentes")
st.session_state.concorrentes = st.data_editor(
    st.session_state.concorrentes,
    num_rows="dynamic",
    key="data_editor"
)

# Botão para gerar o gráfico
if st.button("📈 Gerar Gráfico"):
    st.session_state.gerar_grafico = True

# Exibir o gráfico
if st.session_state.gerar_grafico:
    fig = gerar_grafico(st.session_state.concorrentes)
    st.pyplot(fig)
