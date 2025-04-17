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
        st.warning("Brak załadowanych plików. Najpierw załadowuj pliki CSV.")
        return

    # Wybór pliku
    file_name = st.selectbox("📂 Wybierz plik do analizy", options=list(st.session_state.uploaded_files.keys()))
    df = st.session_state.uploaded_files[file_name]

    # Parametry wykresu
    st.sidebar.subheader("⚙️ Parametry Wykresu")
    plot_type = st.sidebar.selectbox("Typ wykresu", ["Liniowy", "Słupkowy"])
    x_axis = st.sidebar.selectbox("🟦 Oś X", df.columns)
    y_axis = st.sidebar.selectbox("🟥 Oś Y (numeryczna)", df.select_dtypes(include=["int64", "float64"]).columns)

    # Wybór agregacji (na początku nie jest wybrana)
    aggregation_type = None
    aggregation_selected = st.sidebar.checkbox("📏 Wybierz agregację", value=False)

    if aggregation_selected:
        aggregation_type = st.sidebar.radio("📏 Agregacja danych", ["Suma", "Średnia", "Ilość"])

    # Grupowanie (color)
    color_col = None
    enable_color_grouping = st.sidebar.checkbox("🎨 Podział wg dodatkowej kolumny (np. kategorie modeli)")
    if enable_color_grouping:
        color_col = st.sidebar.selectbox("🎯 Kolumna grupująca (kolor)", [col for col in df.columns if col != x_axis])

    # Dodanie nowego wykresu
    if st.sidebar.button("➕ Dodaj Wykres"):
        try:
            # Przygotowanie danych do snapshotu
            columns_to_keep = [x_axis, y_axis]
            if color_col:
                columns_to_keep.append(color_col)
            plot_data = df[columns_to_keep].copy()

            # Grupowanie i agregowanie danych, jeśli jest wybrana agregacja
            if color_col:
                if aggregation_type == "Suma":
                    grouped_df = plot_data.groupby([x_axis, color_col], as_index=False)[y_axis].sum()
                elif aggregation_type == "Średnia":
                    grouped_df = plot_data.groupby([x_axis, color_col], as_index=False)[y_axis].mean()
                elif aggregation_type == "Ilość":
                    grouped_df = plot_data.groupby([x_axis, color_col], as_index=False)[y_axis].count()
                else:
                    grouped_df = plot_data  # Jeśli brak agregacji
            else:
                if aggregation_type == "Suma":
                    grouped_df = plot_data.groupby(x_axis, as_index=False)[y_axis].sum()
                elif aggregation_type == "Średnia":
                    grouped_df = plot_data.groupby(x_axis, as_index=False)[y_axis].mean()
                elif aggregation_type == "Ilość":
                    grouped_df = plot_data.groupby(x_axis, as_index=False)[y_axis].count()
                else:
                    grouped_df = plot_data  # Jeśli brak agregacji

            # Zapisanie wykresu
            new_plot = {
                "id": len(st.session_state.plots),
                "file_name": file_name,
                "type": plot_type,
                "x_axis": x_axis,
                "y_axis": y_axis,
                "color": color_col,
                "aggregation": aggregation_type,  # dodano agregację
                "data_snapshot": grouped_df
            }
            st.session_state.plots.append(new_plot)
            log_event(f"Dodano nowy wykres: {new_plot}")
            log_plots_state(st.session_state)
        except Exception as e:
            st.error(f"Błąd przy dodawaniu wykresu: {e}")

    # Wyświetlanie wykresów
    st.subheader("📋 Lista Wykresów")
    for plot in st.session_state.plots:
        with st.container():
            aggregation_display = plot.get('aggregation', 'Brak agregacji')  # Jeśli brak agregacji, wyświetl "Brak"
            st.write(f"**Wykres {plot['id'] + 1}:** Plik `{plot['file_name']}` – Agregacja: {aggregation_display}")
            col1, col2 = st.columns([9, 1])
            with col1:
                plot_df = plot["data_snapshot"]
                if plot["type"] == "Liniowy":
                    render_line_plot(plot_df, plot["x_axis"], plot["y_axis"], plot["color"], plot["id"])
                elif plot["type"] == "Słupkowy":
                    render_bar_plot(plot_df, plot["x_axis"], plot["y_axis"], plot["color"], plot["id"])
            with col2:
                if st.button("❌ Usuń", key=f"remove_plot_{plot['id']}"):
                    log_event(f"Usunięto wykres: {plot}")
                    st.session_state.plots = [p for p in st.session_state.plots if p["id"] != plot["id"]]
                    log_plots_state(st.session_state)
                    st.rerun()
