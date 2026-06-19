import streamlit as st
import pandas as pd
import os

st.markdown(
    """
# 🌱 Projetos Agropecuários

## Seminário de Projetos Agropecuários (2026.1)

### Universidade Federal do Ceará

**Departamento de Economia Agrícola**

**Prof. Rogério César Pereira de Araújo**

---
"""
)

ARQUIVO = "inscricoes.csv"

LIMITE_POR_DIA = {
    "23/06/2026": 5,
    "30/06/2026": 5
}

COLUNAS = [
    "Nome",
    "Matrícula",
    "E-mail",
    "Nome do grupo",
    "Tema",
    "Integrantes",
    "Dia da apresentação"
]

st.title("Inscrição para Apresentação do Seminário")

if os.path.exists(ARQUIVO):
    df = pd.read_csv(ARQUIVO, sep=";", dtype=str)
else:
    df = pd.DataFrame(columns=COLUNAS)

for coluna in COLUNAS:
    if coluna not in df.columns:
        df[coluna] = ""

st.subheader("Vagas disponíveis")

for dia_opcao, limite in LIMITE_POR_DIA.items():
    ocupadas = len(df[df["Dia da apresentação"] == dia_opcao])
    restantes = limite - ocupadas

    st.success(
        f"{dia_opcao}: {ocupadas} de {limite} vagas disponíveis. "
        f"Restam {restantes} vaga(s)."
    )
else:
    st.error(
        f"{dia_opcao}: {ocupadas} de {limite} vagas disponíveis. "
        "VAGAS ESGOTADAS."
    )

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
    nome = st.text_input("Nome do participante responsável")
    matricula = st.text_input("Matrícula")
    email = st.text_input("E-mail institucional")
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
        matricula_limpa = matricula.strip()
        email_limpo = email.strip().lower()

        matriculas_existentes = df["Matrícula"].fillna("").astype(str).str.strip()
        emails_existentes = df["E-mail"].fillna("").astype(str).str.strip().str.lower()

        if nome.strip() == "":
            st.error("Informe o nome do participante responsável.")
        elif matricula_limpa == "":
            st.error("Informe a matrícula.")
        elif email_limpo == "":
            st.error("Informe o e-mail institucional.")
        elif nome_grupo.strip() == "":
            st.error("Informe o nome do grupo.")
        elif tema.strip() == "":
            st.error("Informe o tema do seminário.")
        elif integrantes.strip() == "":
            st.error("Informe os integrantes do grupo.")
        elif matricula_limpa in matriculas_existentes.values:
            st.error("Esta matrícula já possui inscrição registrada.")
        elif email_limpo in emails_existentes.values:
            st.error("Este e-mail já possui inscrição registrada.")
        elif vagas_restantes <= 0:
            st.error("Este dia já atingiu o limite de 5 apresentações.")
        else:
            nova_inscricao = pd.DataFrame([{
                "Nome": nome.strip(),
                "Matrícula": matricula_limpa,
                "E-mail": email_limpo,
                "Nome do grupo": nome_grupo.strip(),
                "Tema": tema.strip(),
                "Integrantes": integrantes.strip(),
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
                "Nome",
                "Matrícula",
                "E-mail"
            ]].reset_index(drop=True)

            tabela.index = tabela.index + 1
            st.dataframe(tabela, use_container_width=True)

            tabela.index = tabela.index + 1
            st.dataframe(tabela, use_container_width=True)
