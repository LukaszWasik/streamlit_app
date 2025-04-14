import streamlit as st
from plots.line_plot import render_line_plot
from plots.bar_plot import render_bar_plot
from utils.logger import setup_logger, log_plots_state, log_event

# Inicjalizacja loggera
setup_logger()

def render_plot_page():
    """
    Zakładka do generowania wykresów na podstawie załadowanych danych.
    """
    st.header("📊 Generowanie Wykresów")

    # Inicjalizacja przechowywania wykresów
    if "plots" not in st.session_state:
        st.session_state.plots = []

    # Logowanie stanu na starcie
    log_plots_state(st.session_state)

    # Sprawdzenie dostępności plików
    if "uploaded_files" not in st.session_state or not st.session_state.uploaded_files:
        st.warning("Brak załadowanych plików. Najpierw załaduj pliki CSV.")
        return

    # Wybór pliku do generowania nowego wykresu
    file_name = st.selectbox("📂 Wybierz plik do analizy", options=list(st.session_state.uploaded_files.keys()))
    df = st.session_state.uploaded_files[file_name]

    # Wybór parametrów nowego wykresu
    st.sidebar.subheader("⚙️ Parametry Wykresu")
    plot_type = st.sidebar.selectbox("Typ wykresu", ["Liniowy", "Słupkowy"])
    x_axis = st.sidebar.selectbox("🟦 Oś X", df.columns)
    y_axis = st.sidebar.selectbox("🟥 Oś Y (numeryczna)", df.select_dtypes(include=["int64", "float64"]).columns)

    # Dodanie nowego wykresu
    if st.sidebar.button("➕ Dodaj Wykres"):
        new_plot = {
            "id": len(st.session_state.plots),
            "file_name": file_name,
            "type": plot_type,
            "x_axis": x_axis,
            "y_axis": y_axis,
            "data_snapshot": df[[x_axis, y_axis]].copy()  # Zapisujemy konkretne dane dla wykresu
        }
        st.session_state.plots.append(new_plot)
        log_event(f"Dodano nowy wykres: {new_plot}")
        log_plots_state(st.session_state)

    # Wyświetlanie zapisanych wykresów
    st.subheader("📋 Lista Wykresów")
    for plot in st.session_state.plots:
        with st.container():
            st.write(f"**Wykres {plot['id'] + 1}:** Plik `{plot['file_name']}`")
            col1, col2 = st.columns([9, 1])
            with col1:
                # Renderowanie wykresu na podstawie zapisanych danych
                plot_df = plot["data_snapshot"]
                if plot["type"] == "Liniowy":
                    render_line_plot(plot_df, plot["x_axis"], plot["y_axis"], plot_id=plot["id"])
                elif plot["type"] == "Słupkowy":
                    render_bar_plot(plot_df, plot["x_axis"], plot["y_axis"], plot_id=plot["id"])
            with col2:
                if st.button("❌ Usuń", key=f"remove_plot_{plot['id']}"):
                    log_event(f"Usunięto wykres: {plot}")
                    st.session_state.plots = [
                        p for p in st.session_state.plots if p["id"] != plot["id"]
                    ]
                    log_plots_state(st.session_state)
                    st.rerun()
