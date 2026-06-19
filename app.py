import streamlit as st
import pandas as pd
import os

st.set_page_config(
    page_title="Inscrição para Seminário",
    page_icon="📋",
    layout="centered"
)

ARQUIVO = "inscricoes.csv"

LIMITE_POR_DIA = {
    "23/06/2026": 5,
    "30/06/2026": 5
}

st.title("Inscrição para Apresentação do Seminário")

st.write(
    "Escolha o dia da apresentação. Cada dia terá no máximo "
    "5 apresentações, totalizando 10 apresentações."
)

# Criar ou carregar arquivo de inscrições
if os.path.exists(ARQUIVO):
    df = pd.read_csv(ARQUIVO, sep=";")
else:
    df = pd.DataFrame(columns=[
        "Nome do grupo",
        "Tema",
        "Integrantes",
        "Dia da apresentação"
    ])

# Painel de vagas
st.subheader("Vagas disponíveis")

for dia_opcao, limite in LIMITE_POR_DIA.items():
    ocupadas = len(df[df["Dia da apresentação"] == dia_opcao])
    restantes = limite - ocupadas

    if restantes > 0:
        st.success(
            f"{dia_opcao}: {ocupadas} de {limite} vagas ocupadas. "
            f"Restam {restantes} vaga(s)."
        )
    else:
        st.error(
            f"{dia_opcao}: {ocupadas} de {limite} vagas ocupadas. "
            "VAGAS ESGOTADAS."
        )

# Mostrar apenas dias com vagas disponíveis
dias_disponiveis = []

for dia_opcao, limite in LIMITE_POR_DIA.items():
    ocupadas = len(df[df["Dia da apresentação"] == dia_opcao])
    if ocupadas < limite:
        dias_disponiveis.append(dia_opcao)

st.divider()

st.subheader("Formulário de inscrição")

if len(dias_disponiveis) == 0:
    st.error("Todas as vagas foram preenchidas.")
else:
    nome_grupo = st.text_input("Nome do grupo")
    tema = st.text_input("Tema do seminário")
    integrantes = st.text_area("Nome dos integrantes do grupo")

    dia = st.selectbox(
        "Escolha o dia da apresentação",
        dias_disponiveis
    )

    ocupadas_dia = len(df[df["Dia da apresentação"] == dia])
    vagas_restantes = LIMITE_POR_DIA[dia] - ocupadas_dia

    st.info(f"Vagas restantes para {dia}: {vagas_restantes}")

    if st.button("Enviar inscrição"):
        if nome_grupo.strip() == "":
            st.error("Informe o nome do grupo.")
        elif tema.strip() == "":
            st.error("Informe o tema do seminário.")
        elif integrantes.strip() == "":
            st.error("Informe os integrantes do grupo.")
        elif vagas_restantes <= 0:
            st.error("Este dia já atingiu o limite de 5 apresentações.")
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
            st.rerun()

st.divider()

st.subheader("Grupos já inscritos")

if df.empty:
    st.info("Ainda não há grupos inscritos.")
else:
    for dia_opcao in LIMITE_POR_DIA.keys():
        st.markdown(f"### {dia_opcao}")

        inscritos_dia = df[df["Dia da apresentação"] == dia_opcao]

        if inscritos_dia.empty:
            st.write("Nenhum grupo inscrito neste dia.")
        else:
            tabela = inscritos_dia[[
                "Nome do grupo",
                "Tema",
                "Integrantes"
            ]].reset_index(drop=True)

            tabela.index = tabela.index + 1
            st.dataframe(tabela, use_container_width=True)
