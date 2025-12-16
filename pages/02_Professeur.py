import streamlit as st
import pandas as pd
from src.services.data_manager import DataManager
from src.models.note import Note

import streamlit as st
import pandas as pd
from src.services.data_manager import DataManager
from src.models.note import Note

st.set_page_config(page_title="Espace Professeur", page_icon="👨‍🏫")

# --- SECURITY CHECK ---
if "authenticated" not in st.session_state or st.session_state["role"] != "professeur":
    st.error("⛔ Accès refusé. Réservé aux professeurs.")
    st.stop()

st.title(f"👨‍🏫 Espace Professeur ({st.session_state['user_id']})")

# 1. Load Data
if "data_manager" not in st.session_state:
    st.session_state["data_manager"] = DataManager()
manager = st.session_state["data_manager"]

# 2. GET CURRENT PROF AUTOMATICALLY
current_prof_id = st.session_state["user_id"]
current_prof = next((p for p in manager.professeurs if p.id_professeur == current_prof_id), None)

if not current_prof:
    st.error("Erreur de profil. Contactez l'admin.")
    st.stop()

st.sidebar.button("Se déconnecter", on_click=lambda: st.session_state.update({"authenticated": False}) or st.rerun())

st.divider()

# ... (The rest of your code remains the same, starting from "# 3. Select a Module...")

# 3. Select a Module managed by this professor
if not current_prof.modules_enseignes:
    st.info("Vous n'avez aucun module assigné.")
else:
    # Create a map of Code -> Intitule for display
    my_modules_codes = current_prof.modules_enseignes
    # We need to find the Module objects to get their names
    my_modules_objs = [manager.get_module_by_code(code) for code in my_modules_codes]
    # Filter out None in case a module was deleted but still in prof's list
    my_modules_objs = [m for m in my_modules_objs if m is not None]
    
    module_map = {f"{m.intitule} ({m.code_module})": m for m in my_modules_objs}
    
    selected_module_label = st.selectbox("Sélectionnez un module :", options=list(module_map.keys()))
    selected_module = module_map[selected_module_label]
    
    # 4. Interface for the selected module
    st.subheader(f"Gestion : {selected_module.intitule}")
    
    tab_saisie, tab_consultation = st.tabs(["✍️ Saisir des notes", "📊 Consulter les résultats"])
    
    # --- TAB SAISIE ---
    with tab_saisie:
        if not selected_module.etudiants_inscrits:
            st.warning("Aucun étudiant inscrit à ce module.")
        else:
            with st.form("grading_form"):
                col1, col2, col3 = st.columns(3)
                
                # Dropdown of students enrolled in THIS module
                student_objs = [manager.get_etudiant_by_id(uid) for uid in selected_module.etudiants_inscrits]
                student_map = {f"{s.nom} {s.prenom}": s for s in student_objs if s}
                
                sel_student_label = col1.selectbox("Étudiant", options=list(student_map.keys()))
                sel_student = student_map[sel_student_label]
                
                note_val = col2.number_input("Note (/20)", min_value=0.0, max_value=20.0, step=0.25)
                type_note = col3.selectbox("Type", ["Contrôle", "Examen", "TP", "Projet"])
                
                submitted_note = st.form_submit_button("Enregistrer la note")
                
                if submitted_note:
                    new_note = Note(selected_module.code_module, note_val, type_note)
                    try:
                        sel_student.ajouter_note(new_note)
                        manager.save_etudiants() # Notes are stored inside Students
                        st.success(f"Note de {note_val} ajoutée pour {sel_student.nom}")
                    except Exception as e:
                        st.error(f"Erreur : {e}")

    # --- TAB CONSULTATION ---
    with tab_consultation:
        # We need to aggregate notes for all students in this module
        report_data = []
        for uid in selected_module.etudiants_inscrits:
            stu = manager.get_etudiant_by_id(uid)
            if stu:
                # Filter notes for THIS module
                mod_notes = [n.valeur for n in stu.notes if n.code_module == selected_module.code_module]
                moyenne = sum(mod_notes)/len(mod_notes) if mod_notes else 0
                report_data.append({
                    "Étudiant": f"{stu.nom} {stu.prenom}",
                    "Notes": str(mod_notes), # Simple string repr for now
                    "Moyenne Module": round(moyenne, 2)
                })
        
        if report_data:
            df_report = pd.DataFrame(report_data)
            st.dataframe(df_report, use_container_width=True)
        else:
            st.info("Aucune donnée à afficher.")