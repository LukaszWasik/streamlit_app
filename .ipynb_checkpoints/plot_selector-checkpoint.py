import streamlit as st
from plots.line_plot import render_line_plot
from plots.bar_plot import render_bar_plot


def plot_page(df):
    st.title("📊 Generowanie wykresów")

    # Lista dostępnych DataFrame'ów
    dataframes = {k: v for k, v in st.session_state.items() if k.startswith("df_")}

    if not dataframes:
        st.warning("Wczytaj najpierw dane w zakładce 'Dane'")
        return

    selected_df_name = st.selectbox("Wybierz zbior danych", options=list(dataframes.keys()))
    df = dataframes[selected_df_name]

    if "plots" not in st.session_state:
        st.session_state.plots = []

    st.sidebar.header("⚙️ Ustawienia wykresu")
    plot_type = st.sidebar.selectbox("Typ wykresu", ["Liniowy", "Słupkowy"])
    x_axis = st.sidebar.selectbox("Kolumna X", df.columns)
    y_axis = st.sidebar.selectbox("Kolumna Y (numeryczna)", df.select_dtypes(include="number").columns)

    if st.sidebar.button("Dodaj wykres"):
        st.session_state.plots.append({
            "type": plot_type,
            "x_axis": x_axis,
            "y_axis": y_axis
        })

    for idx, plot in enumerate(st.session_state.plots):
        st.subheader(f"Wykres {idx+1}: {plot['type']}")
        if plot['type'] == "Liniowy":
            render_line_plot(df, plot['x_axis'], plot['y_axis'], plot_id=idx)
        elif plot['type'] == "Słupkowy":
            render_bar_plot(df, plot['x_axis'], plot['y_axis'], plot_id=idx)

        if st.button("Usuń wykres", key=f"remove_{idx}"):
            st.session_state.plots.pop(idx)
            st.rerun()
