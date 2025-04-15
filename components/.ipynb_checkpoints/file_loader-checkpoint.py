import streamlit as st
import pandas as pd
from utils.utils import load_csv
import os
def file_uploader():
    """
    Komponent do ładowania plików CSV z możliwością ich podglądu i usuwania.
    """
    st.header("📁 Załaduj Pliki CSV")
    # 📂 Pliki z folderu Datasets
    datasets_dir = "Datasets"
    available_datasets = [
        f for f in os.listdir(datasets_dir)
        if f.endswith(".csv") and os.path.isfile(os.path.join(datasets_dir, f))
    ]
    
    if available_datasets:
        st.subheader("📊 Wybierz gotowy zbiór danych")
        selected_dataset = st.selectbox("Zbiór danych:", available_datasets)
        if st.button("📥 Załaduj wybrany zbiór"):
            dataset_path = os.path.join(datasets_dir, selected_dataset)
            with open(dataset_path, "rb") as f:
                df = load_csv(f)
            if df is not None:
                st.session_state.uploaded_files[selected_dataset] = df
                st.session_state.df = df
                st.success(f"Zbiór {selected_dataset} został załadowany.")
            else:
                st.error("Nie udało się załadować zbioru danych.")

    if "uploaded_files" not in st.session_state:
        st.session_state.uploaded_files = {}

    # 🔄 Umożliwiamy załadowanie wielu plików
    uploaded_files = st.file_uploader("Wybierz pliki CSV", type=["csv"], accept_multiple_files=True, key="uploader")

    # 📥 Obsługa nowo załadowanych plików
    if uploaded_files:
        for file in uploaded_files:
            if file.name not in st.session_state.uploaded_files:
                df = load_csv(file)
                if df is not None:
                    st.session_state.uploaded_files[file.name] = df
                    st.session_state.df = df  # ostatnio załadowany plik
                    st.success(f"Plik {file.name} poprawnie załadowany!")
                else:
                    st.error(f"Nie udało się załadować pliku {file.name}.")

    # 🗂️ Zawsze pokazuj listę załadowanych plików (niezależnie od tego czy coś właśnie załadowano)
    if st.session_state.uploaded_files:
        st.subheader("📜 Załadowane Pliki")
        for file_name in list(st.session_state.uploaded_files.keys()):
            with st.expander(f"📂 {file_name}"):
                df = st.session_state.uploaded_files[file_name]
                st.write(df.head())  # Podgląd pierwszych 5 wierszy
                if st.button(f"❌ Usuń {file_name}", key=f"remove_{file_name}"):
                    del st.session_state.uploaded_files[file_name]
                    st.success(f"Plik {file_name} został usunięty.")
                    st.rerun()  # ⬅️ bardzo ważne: odświeża stronę
    else:
        st.info("Nie załadowano żadnych plików.")
