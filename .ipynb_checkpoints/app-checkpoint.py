import streamlit as st
from components.file_loader import file_uploader
from components.data_preview import data_preview

# Ustawienia strony
st.set_page_config(page_title="Analiza Danych", layout="wide")

# Menu główne
menu_options = [
    "📁 Załaduj Plik",
    "📊 Generowanie Wykresów",
    "📋 Generowanie Raportu",
    "🤖 Nauka Maszynowa",
    "🖥️ Pisanie Kodów"
]
choice = st.sidebar.radio("Menu", menu_options)

# Globalne dane
if "uploaded_files" not in st.session_state:
    st.session_state.uploaded_files = {}

# Obsługa poszczególnych zakładek
if choice == "📁 Załaduj Plik":
    # Sekcja ładowania plików i podglądu danych
    file_uploader()
    data_preview()

elif choice == "📊 Generowanie Wykresów":
    if st.session_state.uploaded_files:
        from pages.plot_page import render_plot_page
        render_plot_page()
    else:
        st.warning("Najpierw załaduj przynajmniej jeden plik CSV.")

elif choice == "📋 Generowanie Raportu":
    if st.session_state.uploaded_files:
        from pages.report_page import render_report_page
        render_report_page()
    else:
        st.warning("Najpierw załaduj przynajmniej jeden plik CSV.")

elif choice == "🤖 Nauka Maszynowa":
    if st.session_state.uploaded_files:
        from pages.ml_page import render_ml_page
        render_ml_page()
    else:
        st.warning("Najpierw załaduj przynajmniej jeden plik CSV.")

elif choice == "🖥️ Pisanie Kodów":
    from pages.code_page import render_code_editor_page
    render_code_editor_page()
