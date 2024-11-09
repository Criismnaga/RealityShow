import streamlit as st
import requests

BASE_URL = "http://api:8000"

def register_user(username, password, nome, email):
    url = f"{BASE_URL}/register"
    payload = {
        "username": username,
        "password": password,
        "nome": nome,
        "email": email
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        st.success("User registered successfully!")
    else:
        st.error(f"Error: {response.json().get('detail', 'Unknown error')}")

def login_user(username, password):
    url = f"{BASE_URL}/login"
    payload = {
        "username": username,
        "password": password
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        st.success("Login successful!")
        return True
    else:
        st.error("Invalid credentials.")
        return False

def get_all_inscriptions():
    url = f"{BASE_URL}/inscricoes"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to fetch inscriptions.")
        return []

def get_approved_inscriptions():
    url = f"{BASE_URL}/inscricoes/aprovados"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to fetch approved inscriptions.")
        return []

def create_inscription(participante_id, formulario):
    url = f"{BASE_URL}/inscricao"
    payload = {
        "participante_id": participante_id,
        "formulario": formulario
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        st.success("Inscription created successfully!")
    else:
        st.error(f"Error: {response.json().get('detail', 'Unknown error')}")

def update_inscription_status(inscricao_id, status):
    url = f"{BASE_URL}/inscricao/{inscricao_id}"
    payload = {
        "status": status
    }
    response = requests.put(url, json=payload)
    if response.status_code == 200:
        st.success("Inscription status updated successfully!")
    else:
        st.error("Failed to update inscription status.")

def delete_inscription(inscricao_id):
    url = f"{BASE_URL}/inscricao/{inscricao_id}"
    response = requests.delete(url)
    if response.status_code == 200:
        st.success("Inscription deleted successfully!")
    else:
        st.error("Failed to delete inscription.")

def get_participant_by_username(username):
    url = f"{BASE_URL}/participante/{username}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to fetch participant information.")
        return None

def get_all_logins():
    url = f"{BASE_URL}/logins"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to fetch logins.")
        return []

st.title("User Authentication and Inscription Management")

auth_mode = st.sidebar.selectbox("Choose mode", ["Login", "Register", "Inscriptions", "Admin Panel"])

if auth_mode == "Register":
    st.header("Register New User")
    new_username = st.text_input("Username")
    new_password = st.text_input("Password", type="password")
    new_name = st.text_input("Full Name")
    new_email = st.text_input("Email")

    if st.button("Register"):
        if new_username and new_password and new_name and new_email:
            register_user(new_username, new_password, new_name, new_email)
        else:
            st.warning("Please fill in all fields")

elif auth_mode == "Login":
    st.header("User Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username and password:
            login_success = login_user(username, password)
            if login_success:
                st.info("Now you can access user-specific features.")
        else:
            st.warning("Please enter both username and password")

elif auth_mode == "Inscriptions":
    st.header("User Inscriptions")
    participante_id = st.number_input("Participant ID", min_value=1, step=1)
    formulario = st.text_area("Form Data (in JSON format)")

    if st.button("Submit Inscription"):
        if participante_id and formulario:
            create_inscription(participante_id, formulario)
        else:
            st.warning("Please fill in all fields")

elif auth_mode == "Admin Panel":
    st.header("Admin Panel")

    st.subheader("View All Inscriptions")
    inscriptions = get_all_inscriptions()
    st.write(inscriptions)

    st.subheader("View Approved Inscriptions")
    approved_inscriptions = get_approved_inscriptions()
    st.write(approved_inscriptions)

    st.subheader("Update Inscription Status")
    inscricao_id = st.number_input("Inscription ID", min_value=1, step=1)
    new_status = st.selectbox("Status", ["Aprovado", "Rejeitado"])
    if st.button("Update Status"):
        if inscricao_id:
            update_inscription_status(inscricao_id, new_status)

    st.subheader("Delete Inscription")
    del_inscricao_id = st.number_input("Inscription ID to delete", min_value=1, step=1)
    if st.button("Delete Inscription"):
        if del_inscricao_id:
            delete_inscription(del_inscricao_id)

    st.subheader("View All Logins")
    logins = get_all_logins()
    st.write(logins)

    st.subheader("Search Participant by Username")
    search_username = st.text_input("Username to search")
    if st.button("Search"):
        participant = get_participant_by_username(search_username)
        st.write(participant)
