import streamlit as st
from database import SessionLocal, Item, init_db

init_db()

st.set_page_config(page_title="Gestão Home Lab", layout="wide")

st.title("🛠️ Sistema de Gestão - Rafael")

db = SessionLocal()

col_form, col_list = st.columns([1, 2])

with col_form:
    st.subheader("Novo Item")
    with st.form("cadastro"):
        nome = st.text_input("Nome do Equipamento/Software")
        status = st.selectbox("Status", ["Ativo", "Manutenção", "Offline"])
        if st.form_submit_button("Cadastrar"):
            novo = Item(nome=nome, status=status)
            db.add(novo)
            db.commit()
            st.success("Cadastrado com sucesso!")
            st.rerun()

with col_list:
    st.subheader("Inventário Atual")
    itens = db.query(Item).all()

    for item in itens:
        with st.container(border=True):
            c1, c2, c3 = st.columns([3, 1, 1])
            c1.write(f"**{item.nome}**")
            c2.info(item.status)
            if c3.button("🗑️", key=f"del_{item.id}"):
                db.delete(item)
                db.commit()
                st.rerun()

db.close()