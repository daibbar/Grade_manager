import streamlit as st
import pandas as pd
from src.services.data_manager import DataManager

st.set_page_config(page_title="Espace Étudiant", page_icon="🎓")

# --- SECURITY CHECK ---
if "authenticated" not in st.session_state or st.session_state["role"] != "etudiant":
    st.error("⛔ Accès refusé. Réservé aux étudiants.")
    st.stop()

st.title("🎓 Espace Étudiant")

# 1. Load Data
if "data_manager" not in st.session_state:
    st.session_state["data_manager"] = DataManager()
manager = st.session_state["data_manager"]

# 2. GET CURRENT STUDENT AUTOMATICALLY
current_student_id = st.session_state["user_id"]
student = manager.get_etudiant_by_id(current_student_id)

if not student:
    st.error("Erreur : Profil étudiant introuvable.")
    st.stop()

st.sidebar.button("Se déconnecter", on_click=lambda: st.session_state.update({"authenticated": False}) or st.rerun())

st.divider()

# --- 3. Dashboard Header ---
# ... (The rest of your code remains the same)

# --- 3. Dashboard Header ---
col1, col2, col3 = st.columns(3)
col1.info(f"**Nom:** {student.nom}")
col2.info(f"**Prénom:** {student.prenom}")
col3.info(f"**Année:** {student.annee_universitaire}")

# --- 4. Generate the Bulletin (Logic Heavy) ---
if not student.modules_inscrits:
    st.warning("Vous n'êtes inscrit à aucun module.")
else:
    bulletin_data = []
    total_moyenne = 0
    count_modules = 0

    for code_mod in student.modules_inscrits:
        # Get Module Info
        mod = manager.get_module_by_code(code_mod)
        if not mod:
            continue # Skip if data is corrupted
            
        # Get Prof Name
        prof_name = "Inconnu"
        if mod.id_professeur:
            prof = next((p for p in manager.professeurs if p.id_professeur == mod.id_professeur), None)
            if prof:
                prof_name = f"{prof.nom} {prof.prenom}"

        # Get Notes for THIS module
        # We filter the big list of notes stored in the student object
        my_notes = [n for n in student.notes if n.code_module == code_mod]
        
        # Calculate Average for this module
        if my_notes:
            vals = [n.valeur for n in my_notes]
            moyenne_mod = sum(vals) / len(vals)
            notes_str = ", ".join([f"{n.valeur} ({n.type_note})" for n in my_notes])
        else:
            moyenne_mod = 0.0
            notes_str = "Aucune note"

        # Add to global stats
        if my_notes:
            total_moyenne += moyenne_mod
            count_modules += 1

        bulletin_data.append({
            "Module": mod.intitule,
            "Code": code_mod,
            "Professeur": prof_name,
            "Détail des notes": notes_str,
            "Moyenne": round(moyenne_mod, 2)
        })
# --- 5. Display General Average ---
    # Calculate global average
    moyenne_generale = total_moyenne / count_modules if count_modules > 0 else 0.0
    
    # Logic: Green if passed, Red if failed
    score_color = "#00cc66" if moyenne_generale >= 10 else "#ff3333"
    
    # CSS Fix: Force text color to dark grey (#31333F) to contrast with the light grey background
    st.markdown(f"""
    <div style="text-align: center; padding: 20px; background-color: #f0f2f6; border-radius: 10px; margin-bottom: 20px; color: #31333F;">
        <h3 style="margin: 0; color: #31333F;">Moyenne Générale</h3>
        <h1 style="margin: 0; font-size: 3em; color: {score_color};">{moyenne_generale:.2f} / 20</h1>
    </div>
    """, unsafe_allow_html=True)

    # --- 6. Display Detailed Table ---
    st.subheader("Détail des résultats")
    if bulletin_data:
        df = pd.DataFrame(bulletin_data)
        
        # Highlight logic (Optional fancy pandas styling)
        def highlight_fail(val):
            color = 'red' if val < 10 else 'green'
            return f'color: {color}'

        # Display interactive table
        st.dataframe(
            df.style.map(highlight_fail, subset=['Moyenne']),
            use_container_width=True
        )