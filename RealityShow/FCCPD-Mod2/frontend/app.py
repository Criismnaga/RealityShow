# app.py
import streamlit as st
import requests

# URL da API FastAPI
API_URL = "http://api:8000"  # Ajuste se necessário

# Função para enviar dados de cadastro para a API
def register_user(username, password, nome, email):
    data = {
        "username": username,
        "password": password,
        "nome": nome,
        "email": email
    }
    response = requests.post(f"{API_URL}/register", json=data)
    if response.status_code == 200:
        st.success("Usuário cadastrado com sucesso!")
    elif response.status_code == 400:
        st.error("Username ou email já cadastrado.")
    else:
        st.error("Erro ao registrar o usuário")

# Tela de cadastro no Streamlit
def registration_form():
    st.title("Cadastre-se no spin-off do BBB")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    nome = st.text_input("Nome")
    email = st.text_input("Email")

    if st.button("Registrar"):
        if username and password and nome and email:
            register_user(username, password, nome, email)
        else:
            st.warning("Por favor, preencha todos os campos.")

# Executa o formulário de registro
if __name__ == "__main__":
    registration_form()
