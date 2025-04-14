import streamlit as st
import pandas as pd
def data_page():
    st.title("📁 Wczytaj dane")
    st.markdown("Możesz wczytać jeden lub wiele plików CSV.")

    uploaded_files = st.file_uploader("Wybierz pliki CSV", type=["csv"], accept_multiple_files=True)

    if uploaded_files:
        for i, uploaded_file in enumerate(uploaded_files):
            df = pd.read_csv(uploaded_file)
            st.subheader(f"Podgląd danych: {uploaded_file.name}")
            st.dataframe(df.head(10))

            # Przechowaj dane w session_state
            st.session_state[f"df_{i}"] = df
