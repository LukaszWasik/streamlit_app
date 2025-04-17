def render_bar_plot(df, x_axis, y_axis, color, plot_id):
    import streamlit as st
    import plotly.express as px

    fig = px.bar(
        df,
        x=x_axis,
        y=y_axis,
        color=color if color else None,
        barmode="group",
        title=f"Wykres słupkowy {plot_id+1}"
    )
    st.plotly_chart(fig, use_container_width=True)
