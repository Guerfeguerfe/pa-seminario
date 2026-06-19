import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Inscrição para Seminário", page_icon="📋")

ARQUIVO = "inscricoes.csv"

LIMITE_POR_DIA = {
    "23/06/2026": 5,
    "30/06/2026": 5
}

st.title("Inscrição para Apresentação do Seminário")

st.write("Escolha o dia da apresentação. Cada dia terá no máximo 5 apresentações.")

nome_grupo = st.text_input("Nome do grupo")
tema = st.text_input("Tema do seminário")
integrantes = st.text_area("Nome dos integrantes do grupo")

dia = st.selectbox(
    "Escolha o dia da apresentação",
    ["23/06/2026", "30/06/2026"]
)

if os.path.exists(ARQUIVO):
    df = pd.read_csv(ARQUIVO, sep=";")
else:
    df = pd.DataFrame(columns=[
        "Nome do grupo",
        "Tema",
        "Integrantes",
        "Dia da apresentação"
    ])

inscricoes_dia = df[df["Dia da apresentação"] == dia]
vagas_restantes = LIMITE_POR_DIA[dia] - len(inscricoes_dia)

st.info(f"Vagas restantes para {dia}: {vagas_restantes}")

if st.button("Enviar inscrição"):
    if nome_grupo.strip() == "":
        st.error("Informe o nome do grupo.")
    elif tema.strip() == "":
        st.error("Informe o tema do seminário.")
    elif integrantes.strip() == "":
        st.error("Informe os integrantes do grupo.")
    elif vagas_restantes <= 0:
        st.error("Este dia já atingiu o limite de 5 apresentações. Escolha outro dia.")
    else:
        nova_inscricao = pd.DataFrame([{
            "Nome do grupo": nome_grupo,
            "Tema": tema,
            "Integrantes": integrantes,
            "Dia da apresentação": dia
        }])

        df = pd.concat([df, nova_inscricao], ignore_index=True)
        df.to_csv(ARQUIVO, sep=";", index=False)

        st.success("Inscrição realizada com sucesso!")
        st.balloons()
