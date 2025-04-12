# plot_selector.py

import streamlit as st
from plots.line_plot import render_line_plot
from plots.bar_plot import render_bar_plot

def plot_selector(df):
    """
    Funkcja do wyboru wykresu oraz generowania wykresu na podstawie wybranych opcji.
    Wspiera dodawanie i usuwanie wykresów.
    """
    if "plots" not in st.session_state:
        st.session_state.plots = []

    numeric_columns = df.select_dtypes(include=["float64", "int64"]).columns.tolist()
    all_columns = df.columns.tolist()

    plot_type = st.selectbox("Wybierz typ wykresu", options=["Liniowy", "Słupkowy"], key="plot_type")
    x_axis = st.selectbox("🟦 Wybierz kolumnę dla osi X", options=all_columns, key="x_axis")
    y_axis = st.selectbox("🟥 Wybierz kolumnę dla osi Y (numeryczna)", options=numeric_columns, key="y_axis")

    if st.button("Generuj wykres"):
        new_plot = {
            "type": plot_type,
            "x_axis": x_axis,
            "y_axis": y_axis,
            "filter": False,
            "group_by": None,
            "agg_func": "mean",
            "interactive": False
        }
        st.session_state.plots.append(new_plot)

    for idx, plot in enumerate(st.session_state.plots):
        col1, col2 = st.columns([9, 1])
        with col1:
            if plot["type"] == "Liniowy":
                render_line_plot(df, plot, plot_id=idx)
            elif plot["type"] == "Słupkowy":
                render_bar_plot(df, plot, plot_id=idx)

        with col2:
            if st.button(f"❌", key=f"remove_{idx}"):
                st.session_state.plots.pop(idx)
                st.rerun()
                break
