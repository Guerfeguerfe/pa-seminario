import streamlit as st

st.set_page_config(
    page_title="Seminário de Projetos Agropecuários",
    page_icon="📚",
    layout="centered"
)

st.title("Seminário de Projetos Agropecuários")

st.subheader("Formulário de inscrição")

st.write("""
Este sistema foi criado para organizar as inscrições dos alunos
no seminário da disciplina de Projetos Agropecuários.
""")

nome = st.text_input("Nome completo")
matricula = st.text_input("Matrícula")
curso = st.text_input("Curso")
email = st.text_input("E-mail")
tema = st.text_area("Tema do seminário")

if st.button("Enviar inscrição"):
    if nome and matricula and curso and email and tema:
        st.success("Inscrição realizada com sucesso!")

        st.write("### Dados enviados")
        st.write(f"**Nome:** {nome}")
        st.write(f"**Matrícula:** {matricula}")
        st.write(f"**Curso:** {curso}")
        st.write(f"**E-mail:** {email}")
        st.write(f"**Tema:** {tema}")
    else:
        st.error("Preencha todos os campos antes de enviar.")
