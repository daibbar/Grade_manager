import os
import shutil
from src.models.etudiant import Etudiant
from src.models.professeur import Professeur
from src.models.module import Module
from src.models.note import Note
from src.services.data_manager import DataManager

# Config: Use a temporary folder for testing so we don't mess up real data
TEST_DIR = "test_data"

def clean_start():
    """Removes the test directory if it exists to start fresh."""
    if os.path.exists(TEST_DIR):
        shutil.rmtree(TEST_DIR)
    print(f"🧹 Cleaned up {TEST_DIR} directory.")

def run_test():
    clean_start()
    
    print("\n--- 1. INITIALIZATION ---")
    # Instantiate DataManager with the test directory
    manager = DataManager(data_dir=TEST_DIR)
    print("✅ DataManager initialized.")

    print("\n--- 2. CREATING OBJECTS ---")
    # Create a Professor
    prof = Professeur("P001", "Turing", "Alan")
    manager.professeurs.append(prof)
    print(f"Created Prof: {prof.nom}")

    # Create a Module
    module_py = Module("M101", "Python Avancé", "2024-2025", prof.id_professeur)
    manager.modules.append(module_py)
    
    # Link Prof to Module (Bi-directional update logic)
    prof.assigner_module(module_py.code_module)
    print(f"Created Module: {module_py.intitule} (Assigned to {prof.nom})")

    # Create a Student
    student = Etudiant("E1337", "Anderson", "Neo", "2024-2025")
    manager.etudiants.append(student)
    print(f"Created Student: {student.nom}")

    print("\n--- 3. LOGIC & RELATIONS ---")
    # Register Student to Module
    student.s_inscrire_module(module_py.code_module)
    module_py.ajouter_etudiant(student.id_etudiant)
    print(f"✅ Student {student.nom} registered to {module_py.code_module}")

    # Add Notes
    try:
        note1 = Note(module_py.code_module, 14.5, "TP")
        note2 = Note(module_py.code_module, 16.0, "Exam")
        student.ajouter_note(note1)
        student.ajouter_note(note2)
        print("✅ Added 2 notes (14.5 and 16.0)")
    except Exception as e:
        print(f"❌ Error adding notes: {e}")

    # Test Average Calculation
    avg = student.calculer_moyenne()
    expected_avg = 15.25
    if avg == expected_avg:
        print(f"✅ Average calculation correct: {avg}")
    else:
        print(f"❌ Average calculation FAILED. Got {avg}, expected {expected_avg}")

    print("\n--- 4. PERSISTENCE (SAVING) ---")
    manager.save_professeurs()
    manager.save_modules()
    manager.save_etudiants()
    print("💾 Data saved to JSON files.")

    print("\n--- 5. RELOADING (SIMULATING APP RESTART) ---")
    # Create a NEW manager instance to verify it loads from disk
    new_manager = DataManager(data_dir=TEST_DIR)
    
    # Verify Student Data
    loaded_student = new_manager.get_etudiant_by_id("E1337")
    if loaded_student:
        print(f"✅ Reloaded Student: {loaded_student.nom}")
        if len(loaded_student.notes) == 2:
            print(f"✅ Notes preserved: {len(loaded_student.notes)} notes found.")
        else:
            print(f"❌ Data Loss: Notes missing! Found {len(loaded_student.notes)}")
            
        # Check if modules enrolled match
        if "M101" in loaded_student.modules_inscrits:
             print(f"✅ Module enrollment preserved.")
        else:
             print(f"❌ Data Loss: Student not enrolled in M101.")
    else:
        print("❌ Data Loss: Student E1337 not found in loaded data.")

    # Verify Module Data
    loaded_module = new_manager.get_module_by_code("M101")
    if loaded_module and loaded_module.id_professeur == "P001":
        print(f"✅ Module association preserved (Prof ID: {loaded_module.id_professeur})")
    else:
        print("❌ Data Loss: Module or Prof association missing.")

if __name__ == "__main__":
    run_test()