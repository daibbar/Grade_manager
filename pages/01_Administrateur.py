import streamlit as st
import pandas as pd
from src.services.data_manager import DataManager
from src.models.etudiant import Etudiant
from src.models.professeur import Professeur
from src.models.module import Module

st.set_page_config(page_title="Administration", page_icon="⚙️")

st.title("⚙️ Espace Administrateur")


# --- SECURITY CHECK ---
if "authenticated" not in st.session_state or st.session_state["role"] != "admin":
    st.error("⛔ Accès refusé. Vous devez être connecté en tant qu'Administrateur.")
    st.stop() # Stops execution here
# --- 1. Load Data Manager (Safe Load) ---

if "data_manager" not in st.session_state:
    st.session_state["data_manager"] = DataManager()

manager = st.session_state["data_manager"]

# --- 2. Interface Layout ---
tab_etudiants, tab_profs, tab_modules, tab_inscriptions = st.tabs(["👨‍🎓 Étudiants", "👨‍🏫 Professeurs", "📚 Modules", "🔗 Inscriptions"])
# ==========================================
# TAB 1: GESTION DES ÉTUDIANTS
# ==========================================
with tab_etudiants:
    st.header("Gestion des Étudiants")
    
    with st.expander("➕ Ajouter un étudiant", expanded=False):
        with st.form("add_student_form"):
            col1, col2 = st.columns(2)
            id_new = col1.text_input("ID Étudiant (ex: E101)")
            annee_new = col2.text_input("Année Universitaire", value="2024-2025")
            nom_new = col1.text_input("Nom")
            prenom_new = col2.text_input("Prénom")
            
            # --- NEW INPUT ---
            pwd_new = st.text_input("Mot de passe provisoire", value="1234", type="password")
            # -----------------
            
            submitted = st.form_submit_button("Enregistrer l'étudiant")
            if submitted:
                if manager.get_etudiant_by_id(id_new):
                    st.error("Cet ID existe déjà !")
                else:
                    # Pass the password to the constructor
                    new_etudiant = Etudiant(id_new, nom_new, prenom_new, annee_new, password=pwd_new)
                    
                    manager.etudiants.append(new_etudiant)
                    manager.save_etudiants()
                    st.success(f"Étudiant {nom_new} ajouté avec succès !")
                    st.rerun()

    if manager.etudiants:
        data = [e.to_dict() for e in manager.etudiants]
        df = pd.DataFrame(data)
        st.dataframe(df[["id_etudiant", "nom", "prenom", "annee_universitaire"]], use_container_width=True)
    else:
        st.info("Aucun étudiant enregistré.")

# ==========================================
# TAB 2: GESTION DES PROFESSEURS
# ==========================================
with tab_profs:
    st.header("Gestion des Professeurs")
    
    with st.expander("➕ Ajouter un professeur", expanded=False):
        with st.form("add_prof_form"):
            col1, col2 = st.columns(2)
            id_prof = col1.text_input("ID Professeur (ex: P001)")
            empty_col = col2.empty() # Spacer
            pwd_prof = col2.text_input("Mot de passe", value="1234", type="password")
            nom_prof = col1.text_input("Nom")
            prenom_prof = col2.text_input("Prénom")
            
            submitted_prof = st.form_submit_button("Enregistrer le professeur")
            if submitted_prof:
                # Check for duplicates (Simple check)
                existing = [p for p in manager.professeurs if p.id_professeur == id_prof]
                if existing:
                    st.error("Cet ID Professeur existe déjà !")
                else:
                    new_prof = Professeur(id_prof, nom_prof, prenom_prof)
                    manager.professeurs.append(new_prof)
                    manager.save_professeurs()
                    st.success(f"Professeur {nom_prof} ajouté !")
                    st.rerun()

    if manager.professeurs:
        data = [p.to_dict() for p in manager.professeurs]
        df = pd.DataFrame(data)
        # We also show how many modules they teach (calculated column)
        df["nb_modules"] = df["modules_enseignes"].apply(len)
        st.dataframe(df[["id_professeur", "nom", "prenom", "nb_modules"]], use_container_width=True)
    else:
        st.info("Aucun professeur enregistré.")

# ==========================================
# TAB 3: GESTION DES MODULES
# ==========================================
with tab_modules:
    st.header("Gestion des Modules")
    
    # Requirement: A module must have a professor.
    if not manager.professeurs:
        st.warning("⚠️ Vous devez d'abord créer des professeurs avant de créer des modules.")
    else:
        with st.expander("➕ Créer un module", expanded=False):
            with st.form("add_module_form"):
                col1, col2 = st.columns(2)
                code_mod = col1.text_input("Code Module (ex: M101)")
                annee_mod = col2.text_input("Année", value="2024-2025")
                intitule = st.text_input("Intitulé du module")
                
                # Dynamic Selectbox for Professor
                # We create a mapping: "Name (ID)" -> ID
                prof_options = {f"{p.nom} {p.prenom} ({p.id_professeur})": p.id_professeur for p in manager.professeurs}
                selected_label = st.selectbox("Professeur responsable", options=list(prof_options.keys()))
                selected_prof_id = prof_options[selected_label]
                
                submitted_mod = st.form_submit_button("Créer le module")
                
                if submitted_mod:
                    if manager.get_module_by_code(code_mod):
                        st.error("Ce code module existe déjà !")
                    else:
                        # 1. Create Module
                        new_module = Module(code_mod, intitule, annee_mod, selected_prof_id)
                        manager.modules.append(new_module)
                        manager.save_modules()
                        
                        # 2. Assign Module to Professor (Update Relationship)
                        prof = next(p for p in manager.professeurs if p.id_professeur == selected_prof_id)
                        prof.assigner_module(code_mod)
                        manager.save_professeurs()
                        
                        st.success(f"Module {intitule} créé et assigné à {prof.nom} !")
                        st.rerun()

    if manager.modules:
        data = [m.to_dict() for m in manager.modules]
        df = pd.DataFrame(data)
        df["nb_etudiants"] = df["etudiants_inscrits"].apply(len)
        st.dataframe(df[["code_module", "intitule", "annee_universitaire", "id_professeur", "nb_etudiants"]], use_container_width=True)
    else:
        st.info("Aucun module enregistré.")


# ==========================================
# TAB 4: INSCRIPTIONS (LINKING)
# ==========================================
with tab_inscriptions:
    st.header("Inscriptions aux Modules")
    
    if not manager.etudiants or not manager.modules:
        st.warning("Il faut des étudiants et des modules pour faire une inscription.")
    else:
        with st.form("enroll_form"):
            col1, col2 = st.columns(2)
            
            # Select Student
            student_opts = {f"{e.nom} {e.prenom} ({e.id_etudiant})": e.id_etudiant for e in manager.etudiants}
            sel_student_label = col1.selectbox("Étudiant", options=list(student_opts.keys()))
            sel_student_id = student_opts[sel_student_label]
            
            # Select Module
            module_opts = {f"{m.intitule} ({m.code_module})": m.code_module for m in manager.modules}
            sel_module_label = col2.selectbox("Module", options=list(module_opts.keys()))
            sel_module_code = module_opts[sel_module_label]
            
            submitted_enroll = st.form_submit_button("Inscrire l'étudiant")
            
            if submitted_enroll:
                # 1. Get Objects
                student = manager.get_etudiant_by_id(sel_student_id)
                module = manager.get_module_by_code(sel_module_code)
                
                # 2. Check if already enrolled
                if sel_module_code in student.modules_inscrits:
                    st.error("Cet étudiant est déjà inscrit à ce module.")
                else:
                    # 3. Perform Bi-directional Update
                    student.s_inscrire_module(sel_module_code)
                    module.ajouter_etudiant(sel_student_id)
                    
                    # 4. Save Both
                    manager.save_etudiants()
                    manager.save_modules()
                    st.success(f"{student.nom} inscrit en {module.intitule} !")