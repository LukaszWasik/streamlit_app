import streamlit as st
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

def render_ml_page():
    """
    Zakładka do trenowania modelu ML na podstawie załadowanych danych.
    Na razie placeholder do przyszłej funkcjonalności.
    """
    st.header("🤖 Trenowanie Modelu ML")

    if "uploaded_files" not in st.session_state or not st.session_state.uploaded_files:
        st.warning("Brak załadowanych plików. Najpierw załaduj pliki CSV.")
        return

    # Wybór pliku
    st.sidebar.subheader("📂 Wybierz plik do analizy")
    file_name = st.sidebar.selectbox("Wybierz plik", options=list(st.session_state.uploaded_files.keys()))
    df = st.session_state.uploaded_files[file_name]

    # Wybór algorytmu ML
    st.sidebar.subheader("🔧 Wybór algorytmu")
    model_type = st.sidebar.selectbox("Wybierz algorytm ML", ["Regresja Liniowa"], index=0)

    if model_type == "Regresja Liniowa":
        # Wybór zmiennej docelowej
        st.sidebar.subheader("⚙️ Parametry Regresji Liniowej")
        target_column = st.sidebar.selectbox("Wybierz zmienną docelową (target)", df.columns)

        # Wybór zmiennych objaśniających
        numeric_columns = df.select_dtypes(include=["int64", "float64"]).columns.tolist()

        # Sprawdzenie, czy zmienna docelowa jest wśród zmiennych numerycznych i jeśli tak, usuwamy ją z listy
        if target_column in numeric_columns:
            numeric_columns.remove(target_column)

        features_columns = st.sidebar.multiselect("Wybierz zmienne objaśniające (features)", numeric_columns)

        if st.sidebar.button("Trenuj model"):
            if len(features_columns) > 0:
                # Przygotowanie danych
                X = df[features_columns]
                y = df[target_column]
                
                # Podział danych na treningowe i testowe
                X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

                # Trenowanie modelu
                model = LinearRegression()
                model.fit(X_train, y_train)

                # Predykcja na danych testowych
                y_pred = model.predict(X_test)

                # Ocena modelu
                mse = mean_squared_error(y_test, y_pred)
                st.subheader(f"Średni błąd kwadratowy (MSE): {mse:.2f}")
            else:
                st.warning("Wybierz zmienne objaśniające (features) przed treningiem modelu.")
    
    # Podgląd danych
    st.subheader("🔎 Podgląd danych")
    st.dataframe(df.head())

    st.info("Trenowanie modelu jest na razie dostępne tylko dla regresji liniowej. Możliwość dodawania innych algorytmów zostanie dodana w przyszłości.")
