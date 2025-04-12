# plots/line_plot.py

import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import logging

def render_line_plot(df, plot, plot_id=None):
    st.subheader("📈 Wykres liniowy")

    try:
        with st.expander("⚙️ Opcje wykresu", expanded=True):
            filter_data = st.checkbox("🔍 Włącz filtrowanie danych", value=plot.get("filter", False), key=f"filter_line_{plot_id}")
            group_by_col = st.selectbox("📎 Grupuj po kolumnie (opcjonalnie)", options=[None] + df.columns.tolist(),
                                         index=(df.columns.tolist().index(plot.get("group_by")) + 1) if plot.get("group_by") in df.columns else 0,
                                         key=f"group_line_{plot_id}")
            agg_func = st.selectbox("📈 Agregacja", options=["mean", "sum", "min", "max"],
                                    index=["mean", "sum", "min", "max"].index(plot.get("agg_func", "mean")),
                                    key=f"agg_line_{plot_id}")
            use_interactive = st.checkbox("✨ Użyj wykresu interaktywnego (Plotly)", value=plot.get("interactive", False), key=f"interactive_line_{plot_id}")

            # Zapisz aktualizacje
            st.session_state.plots[plot_id].update({
                "filter": filter_data,
                "group_by": group_by_col,
                "agg_func": agg_func,
                "interactive": use_interactive
            })

        filtered_df = df.copy()
        if filter_data:
            filter_col = st.selectbox("🔎 Kolumna do filtrowania", df.columns, key=f"filter_col_line_{plot_id}")
            unique_vals = df[filter_col].unique()
            selected_vals = st.multiselect("Wybierz wartości", unique_vals, default=unique_vals, key=f"filter_vals_line_{plot_id}")
            filtered_df = filtered_df[filtered_df[filter_col].isin(selected_vals)]

        if group_by_col:
            filtered_df = filtered_df.groupby([group_by_col, plot["x_axis"]])[plot["y_axis"]].agg(plot["agg_func"]).reset_index()

        if use_interactive:
            fig = px.line(filtered_df, x=plot["x_axis"], y=plot["y_axis"], color=group_by_col if group_by_col else None,
                          title=f"Wykres liniowy: {plot['y_axis']} względem {plot['x_axis']}")
            st.plotly_chart(fig)
        else:
            fig, ax = plt.subplots()
            sns.lineplot(data=filtered_df, x=plot["x_axis"], y=plot["y_axis"], hue=group_by_col, ax=ax)
            ax.set_title(f"Wykres liniowy: {plot['y_axis']} względem {plot['x_axis']}")
            st.pyplot(fig)

        logging.info(f"Wygenerowano wykres liniowy: {plot['y_axis']} względem {plot['x_axis']}")
    except Exception as e:
        st.error(f"Błąd generowania wykresu: {e}")
        logging.error(f"Błąd: {e}")
