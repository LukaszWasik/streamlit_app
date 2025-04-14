def render_line_plot(df, x_axis, y_axis, plot_id):
    import streamlit as st
    import plotly.express as px

    fig = px.line(df, x=x_axis, y=y_axis, title=f"Wykres liniowy {plot_id+1}")
    st.plotly_chart(fig, use_container_width=True)