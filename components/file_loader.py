import streamlit as st
import pandas as pd
from utils.utils import load_csv

def file_uploader():
    """
    Komponent do ładowania plików CSV z możliwością ich podglądu i usuwania.
    """
    st.header("📁 Załaduj Pliki CSV")

    if "uploaded_files" not in st.session_state:
        st.session_state.uploaded_files = {}
    
    # Dodaj możliwość załadowania wielu plików
    uploaded_files = st.file_uploader("Wybierz pliki CSV", type=["csv"], accept_multiple_files=True)

    if uploaded_files:
        for file in uploaded_files:
            if file.name not in st.session_state.uploaded_files:
                df = load_csv(file)
                if df is not None:
                    # Przechowujemy dane w st.session_state, aby były dostępne w edytorze kodu
                    st.session_state.uploaded_files[file.name] = df
                    st.session_state.df = df  # Zapisujemy ostatnio załadowane dane do df
                    st.success(f"Plik {file.name} poprawnie załadowany!")
                else:
                    st.error(f"Nie udało się załadować pliku {file.name}.")

    # Wyświetl listę załadowanych plików
    if st.session_state.uploaded_files:
        st.subheader("📜 Załadowane Pliki")
        for file_name in list(st.session_state.uploaded_files.keys()):
            with st.expander(f"📂 {file_name}"):
                df = st.session_state.uploaded_files[file_name]
                st.write(df.head())  # Podgląd pierwszych 5 wierszy
                if st.button(f"❌ Usuń {file_name}", key=f"remove_{file_name}"):
                    del st.session_state.uploaded_files[file_name]
                    st.success(f"Plik {file_name} został usunięty.")
                    st.experimental_rerun()

    else:
        st.info("Nie załadowano żadnych plików.")
