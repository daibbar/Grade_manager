import streamlit as st
from src.services.data_manager import DataManager

st.set_page_config(page_title="Login - Gestion Notes", page_icon="🔒")

# 1. Initialize Session State
if "data_manager" not in st.session_state:
    st.session_state["data_manager"] = DataManager()
    
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
    st.session_state["role"] = None
    st.session_state["user_id"] = None

manager = st.session_state["data_manager"]

# 2. Define Logout Function (to be used in sidebar)
def logout():
    st.session_state["authenticated"] = False
    st.session_state["role"] = None
    st.session_state["user_id"] = None
    st.rerun()

# 3. If Logged In, Show Welcome Message
if st.session_state["authenticated"]:
    st.sidebar.button("Se déconnecter", on_click=logout)
    st.title(f"Bienvenue, {st.session_state['user_id']}")
    st.success(f"Vous êtes connecté en tant que : {st.session_state['role'].upper()}")
    st.info("👈 Utilisez le menu à gauche pour accéder à votre espace.")
    st.stop() # Stop here, let the user click the sidebar pages

# 4. Login Form
st.title("🔒 Connexion")

with st.form("login_form"):
    role = st.selectbox("Type de compte", ["Administrateur", "Professeur", "Étudiant"])
    username = st.text_input("Identifiant (ID)")
    password = st.text_input("Mot de passe", type="password")
    
    submitted = st.form_submit_button("Se connecter")
    
    if submitted:
        # A. AUTH ADMIN
        if role == "Administrateur":
            if username == "admin" and password == "admin":
                st.session_state["authenticated"] = True
                st.session_state["role"] = "admin"
                st.session_state["user_id"] = "Admin"
                st.success("Connexion réussie !")
                st.rerun()
            else:
                st.error("Identifiant ou mot de passe incorrect.")

        # B. AUTH PROFESSEUR
        elif role == "Professeur":
            # Find prof by ID
            prof = next((p for p in manager.professeurs if p.id_professeur == username), None)
            if prof and password == "1234": # Hardcoded password for demo
                st.session_state["authenticated"] = True
                st.session_state["role"] = "professeur"
                st.session_state["user_id"] = prof.id_professeur
                st.success(f"Bienvenue Professeur {prof.nom}")
                st.rerun()
            else:
                st.error("ID inconnu ou mot de passe incorrect (Essayez '1234').")

        # C. AUTH ETUDIANT
        elif role == "Étudiant":
            etud = manager.get_etudiant_by_id(username)
            if etud and password == "1234":
                st.session_state["authenticated"] = True
                st.session_state["role"] = "etudiant"
                st.session_state["user_id"] = etud.id_etudiant
                st.success(f"Bienvenue {etud.nom}")
                st.rerun()
            else:
                st.error("ID inconnu ou mot de passe incorrect (Essayez '1234').")