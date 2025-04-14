import streamlit as st

def data_preview():
    """
    Komponent do podglądu załadowanych danych.
    Umożliwia wybór pliku, regulację liczby wyświetlanych wierszy oraz filtrowanie kolumn.
    """
    st.header("👁️ Podgląd Danych")

    if "uploaded_files" not in st.session_state or not st.session_state.uploaded_files:
        st.warning("Brak załadowanych plików. Najpierw załaduj pliki CSV.")
        return

    # Wybór pliku do podglądu
    file_name = st.selectbox("📂 Wybierz plik do podglądu", options=list(st.session_state.uploaded_files.keys()))
    df = st.session_state.uploaded_files[file_name]

    # Suwak do regulacji liczby wierszy
    num_rows = st.slider("📊 Liczba wierszy do wyświetlenia", min_value=5, max_value=len(df), value=10, step=5)

    # Opcjonalne filtrowanie kolumn
    with st.expander("⚙️ Opcje filtrowania kolumn"):
        selected_columns = st.multiselect("Wybierz kolumny do wyświetlenia", options=df.columns.tolist(), default=df.columns.tolist())
        filtered_df = df[selected_columns] if selected_columns else df

    # Wyświetlanie danych
    st.subheader(f"Podgląd danych z pliku: {file_name}")
    st.dataframe(filtered_df.head(num_rows))
