import streamlit as st  # type: ignore
import requests  # type: ignore

BASE_URL = "http://api:8000"

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Carrega o CSS personalizado:
local_css("./frontend/styles.css")

# Carrega a fonte personalizada:
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

# Funções da API
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
        user_data = response.json()
        return user_data
    else:
        st.error("Invalid credentials.")
        return None

def create_inscription(participante_id, formulario):
    url = f"{BASE_URL}/inscricao"
    response = requests.post(url, json={"participante_id": participante_id, "formulario": formulario})
    if response.status_code == 200:
        st.success("Inscription created successfully!")
    else:
        st.error(f"Error: {response.json().get('detail', 'Unknown error')}")

def get_all_inscriptions():
    url = f"{BASE_URL}/inscricoes"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to fetch inscriptions.")
        return []

# Inicializa o estado da sessão para login e dados do participante
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "auth_mode" not in st.session_state:
    st.session_state["auth_mode"] = "Login"
if "participant_id" not in st.session_state:
    st.session_state["participant_id"] = None
if "participant_name" not in st.session_state:
    st.session_state["participant_name"] = None

# Layout principal
st.title("User Authentication and Inscription Management")

# Seleciona o modo de autenticação
available_modes = ["Login", "Register", "Admin Panel"]
auth_mode = st.sidebar.selectbox(
    "Choose mode", 
    available_modes,
    index=available_modes.index(st.session_state["auth_mode"]) if st.session_state["auth_mode"] in available_modes else 0
)

# Define o auth_mode manualmente para "Inscriptions" caso o usuário esteja logado
if st.session_state["logged_in"]:
    auth_mode = "Inscriptions"

# Aba de Registro
if auth_mode == "Register":
    st.markdown("<div class='form-container'>", unsafe_allow_html=True)
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
    st.markdown("</div>", unsafe_allow_html=True)

# Aba de Login
elif auth_mode == "Login":
    st.markdown("<div class='form-container'>", unsafe_allow_html=True)
    st.header("User Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username and password:
            user_data = login_user(username, password)
            if user_data:
                # Armazena as informações do participante no estado da sessão
                st.session_state["logged_in"] = True
                st.session_state["auth_mode"] = "Inscriptions"
                st.session_state["participant_id"] = user_data["id"]
                st.session_state["participant_name"] = user_data["nome"]
                st.experimental_rerun()  # Redireciona automaticamente para "Inscriptions"
        else:
            st.warning("Please enter both username and password")
    st.markdown("</div>", unsafe_allow_html=True)

# Aba de Inscrições
elif auth_mode == "Inscriptions":
    st.markdown("<div class='form-container'>", unsafe_allow_html=True)
    st.header("User Inscriptions")
    
    # Exibe o ID e o nome do participante logado
    participante_id = st.session_state.get("participant_id", "ID não encontrado")
    nome = st.session_state.get("participant_name", "Nome não encontrado")
    
    st.write(f"**Participant ID**: {participante_id}")
    st.write(f"**Participant Name**: {nome}")
    
    # Botão de Logout
    if st.button("Logout"):
        st.session_state["logged_in"] = False
        st.session_state["auth_mode"] = "Login"
        st.session_state["participant_id"] = None
        st.session_state["participant_name"] = None
        st.experimental_rerun()  # Redireciona para a tela de Login
    
    # Campos do formulário de inscrição
    idade = st.number_input("Idade", min_value=0, step=1)
    instagram = st.text_input("@ no Instagram")
    seguidores = st.number_input("Quantidade de seguidores", min_value=0, step=1)
    idade_coluna = st.number_input("Idade da sua coluna", min_value=0, step=1)
    apelido_colegio = st.text_input("Apelido da época do colégio")
    animal_rep = st.text_area("Qual animal mais te representa e por quê?")
    habilidade = st.text_input("Uma habilidade secreta")
    estacao_ano = st.text_area("Se você fosse uma estação do ano, qual seria e por quê?")
    superpoder = st.text_input("Que superpoder você gostaria de ter?")
    talento_danca = st.text_input("Uma palavra para descrever seu talento para dança")
    musica_entrada = st.text_input("Qual música tocaria sempre que você entrasse numa sala?")
    travessura = st.text_area("Qual foi a maior travessura que você já aprontou?")
    bordao = st.text_input("Qual seria seu bordão num reality show?")

    if st.button("Submit Inscription"):
        if participante_id and nome:
            formulario = {
                "nome": nome,
                "idade": idade,
                "instagram": instagram,
                "seguidores": seguidores,
                "idade_coluna": idade_coluna,
                "apelido_colegio": apelido_colegio,
                "animal_rep": animal_rep,
                "habilidade": habilidade,
                "estacao_ano": estacao_ano,
                "superpoder": superpoder,
                "talento_danca": talento_danca,
                "musica_entrada": musica_entrada,
                "travessura": travessura,
                "bordao": bordao
            }
            create_inscription(participante_id, formulario)
        else:
            st.warning("Please fill in all required fields")
    st.markdown("</div>", unsafe_allow_html=True)

# Aba de Painel Administrativo
elif auth_mode == "Admin Panel":
    st.markdown("<div class='form-container'>", unsafe_allow_html=True)
    st.header("Admin Panel")

    # Exibir todas as inscrições
    inscriptions = get_all_inscriptions()
    st.subheader("All Inscriptions")
    for inscription in inscriptions:
        st.write(inscription)

    # Outras funcionalidades administrativas podem ser adicionadas aqui
    st.markdown("</div>", unsafe_allow_html=True)
