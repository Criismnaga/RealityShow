import streamlit as st  # type: ignore
import requests  # type: ignore
import pandas as pd  # type: ignore

BASE_URL = "http://api:8000"

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Carrega o CSS personalizado
local_css("./frontend/styles.css")

# Carrega a fonte personalizada Raleway:
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Raleway:wght@300;400;600&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

# Funções da API
def register_user(username, password, nome, email, seguidores, instagram):
    url = f"{BASE_URL}/register"
    payload = {
        "username": username,
        "password": password,
        "nome": nome,
        "email": email,
        "instagram": instagram,
        "seguidores": seguidores
        
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

def create_inscription(participante_id, idade, apelido, animal, habilidades, estacao, musica):
    url = f"{BASE_URL}/inscricao"  # Substitua pelo URL correto do endpoint para criar inscrição
    payload = {
        "participante_id": participante_id,
        "idade": idade,
        "apelido_colegio": apelido,
        "animal_representa": animal,
        "habilidade": habilidades,
        "estacao_ano": estacao,
        "musica_preferida": musica
    }
    try:
        response = requests.post(url, json=payload)
        
        # Verifique se a resposta é JSON e se o status é bem-sucedido
        if response.status_code == 200:
            st.success("Inscription submitted successfully!")
        else:
            try:
                # Tente obter detalhes do erro, se disponível em JSON
                error_detail = response.json().get('detail', 'Unknown error')
            except ValueError:
                # Caso o JSON não seja válido, exiba o texto cru da resposta
                error_detail = response.text or 'Unknown error'
            
            st.error(f"Error: {error_detail}")

    except requests.exceptions.RequestException as e:
        st.error(f"Connection error: {e}")

def get_participant_id(username):
    response = requests.get(f"{BASE_URL}/participante/{username}")
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Participante não encontrado.")
        return None
    
def get_participant_info(participante_id):
    response = requests.get(f"{BASE_URL}/inscricao/{participante_id}")
    
    if response.status_code == 200:
        return response.json()  # Retorna os dados do participante como um dicionário
    else:
        st.error("Participante não encontrado.")
        return None
    
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
    

def put_approve_inscription(inscricao_id):
    url = f"{BASE_URL}/inscricao/{inscricao_id}"
    response = requests.put(url, json={"status": "Aprovado"})
    if response.status_code == 200:
        st.success("Inscription approved successfully!")
    else:
        st.error(f"Error: {response.json().get('detail', 'Unknown error')}")

def put_reject_inscription(inscricao_id):
    url = f"{BASE_URL}/inscricao/{inscricao_id}"
    response = requests.put(url, json={"status": "Rejeitado"})
    if response.status_code == 200:
        st.success("Inscription rejected successfully!")
    else:
        st.error(f"Error: {response.json().get('detail', 'Unknown error')}")

def delete_inscricao(inscricao_id):
    url =  url = f"{BASE_URL}/inscricao/{inscricao_id}"  # Substitua pelo URL correto da API
    response = requests.delete(url)
    
    if response.status_code == 200:
        st.success("Inscrição deletada com sucesso!")
        # Limpa o estado da sessão para deslogar o usuário
        st.session_state.clear()
        st.session_state["auth_mode"] = "Login"  # Define o modo de autenticação para "Login"
        st.experimental_rerun()  # Redireciona para a página de login
    else:
        st.error(f"Erro ao deletar inscrição: {response.json().get('detail', 'Erro desconhecido')}")

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
st.title("Se inscreva para o Spinoff do BBB!")

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
    new_instagram = st.text_input("Instagram")
    new_seguidores = st.number_input("Seguidores",  min_value=0, step=1)

    if st.button("Register"):
        if all([new_username, new_password, new_name, new_email, new_instagram, isinstance(new_seguidores, int)]):
            register_user(new_username, new_password, new_name, new_email, new_seguidores, new_instagram)
        else:
            st.error("Por favor, preencha todos os campos corretamente.")
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
elif  auth_mode == "Inscriptions":
    st.markdown("<div class='form-container'>", unsafe_allow_html=True)
    st.header("User Inscriptions")
    
    if "participant_id" not in st.session_state or "participant_name" not in st.session_state:
        username = st.session_state.get("username")
        if username:
            participant = get_participant_id(username)
            if participant:
                st.session_state["participant_id"] = participant.get("participante_id", "ID não encontrado")
                st.session_state["participant_name"] = participant.get("nome", "Nome não encontrado")
    
    participante_id = st.session_state.get("participant_id", "ID não encontrado")
    nome = st.session_state.get("participant_name", "Nome não encontrado")
    
    st.write(f"**Participant ID**: {participante_id}")
    st.write(f"**Participant Name**: {nome}")
    
    if st.button("Logout"):
        st.session_state.clear()
        st.session_state["auth_mode"] = "Login"
        st.experimental_rerun()
    
    # Botão para deletar inscrição
    if st.button("Deletar Inscrição"):
        if participante_id != "ID não encontrado":
            delete_inscricao(participante_id)
        else:
            st.warning("Nenhuma inscrição encontrada para deletar.")

    # Busca as informações existentes do participante
    participant_info = get_participant_info(participante_id)

    # Ajuste os campos para corresponder às chaves do JSON retornado
    idade = st.number_input("Idade", min_value=0, step=1, value=participant_info.get("idade", 0) if participant_info else 0)
    apelido = st.text_input("Apelido do Colégio", participant_info.get("apelido_colegio", "") if participant_info else "")
    animal = st.text_area("Qual animal mais te representa e por quê?", participant_info.get("animal_representa", "") if participant_info else "")
    habilidades = st.text_input("Habilidades", participant_info.get("habilidade", "") if participant_info else "")
    estacao = st.text_input("Estação do Ano", participant_info.get("estacao_ano", "") if participant_info else "")
    musica = st.text_input("Música Preferida", participant_info.get("musica_preferida", "") if participant_info else "")

    if st.button("Submit Inscription"):
        if participante_id and nome:
            create_inscription(participante_id, idade, apelido, animal, habilidades, estacao, musica)
            st.success("Inscription submitted successfully!")
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
    inscription_df = pd.DataFrame(inscriptions)
    st.dataframe(inscription_df, hide_index=True)


    # Exibir apenas as inscrições aprovadas
    approved_inscriptions = get_approved_inscriptions()
    st.subheader("Approved Inscriptions")
    approved_df = pd.DataFrame(approved_inscriptions)
    st.dataframe(approved_df, hide_index=True)

    # Aprovar ou rejeitar inscrição
    st.subheader("Approve or Reject Inscription")
    st.write("Select an inscription ID and click the button to approve or reject it.")

    inscricao_id = st.number_input("Inscription ID", min_value=0, step=1)

    if st.button("Approve Inscription"):
        put_approve_inscription(inscricao_id)
        st.rerun()
    if st.button("Reject Inscription"):
        put_reject_inscription(inscricao_id)
        st.rerun()

    # Outras funcionalidades administrativas podem ser adicionadas aqui
    st.markdown("</div>", unsafe_allow_html=True)
