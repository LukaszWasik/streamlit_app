# app.py

import streamlit as st
from logger import setup_logger
from utils import load_csv
import os
from plot_selector import plot_selector  # Importowanie funkcji do wyboru i generowania wykresów

# Inicjalizacja logowania
log_file = setup_logger()

# Wczytanie pliku CSV
uploaded_file = st.file_uploader("Wczytaj plik CSV", type=["csv"])

if uploaded_file is not None:
    # Wczytanie danych do dataframe
    df = load_csv(uploaded_file)
    
    if df is not None:
        st.success("Plik poprawnie wczytany!")

        # Podgląd danych
        st.subheader("Podgląd danych")
        st.dataframe(df.head())

        # Wywołanie funkcji do wyboru wykresu i generowania wykresu
        plot_selector(df)
else:
    st.info("Wczytaj plik CSV, aby rozpocząć analizę.")
