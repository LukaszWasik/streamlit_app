import streamlit as st
from utils.report_analysis import (
    check_missing_values,
    check_duplicates,
    analyze_text_columns,
    analyze_numeric_columns,
    analyze_date_columns,
    analyze_text_length,
    analyze_correlation,
    check_unique_ids,
    analyze_binary_columns
)

def render_report_page():
    st.header("📑 Generowanie Raportu")

    if "uploaded_files" not in st.session_state or not st.session_state.uploaded_files:
        st.warning("Brak załadowanych plików. Najpierw załaduj pliki CSV.")
        return

    st.subheader("🔍 Wybierz dane do analizy")
    file_name = st.selectbox("📂 Wybierz plik", options=list(st.session_state.uploaded_files.keys()))
    df = st.session_state.uploaded_files[file_name]

    # Ustawienia opcjonalne
    with st.expander("⚙️ Ustawienia zaawansowane"):
        date_column = st.selectbox("🕒 Kolumna datowa (opcjonalnie)", options=[""] + list(df.columns), index=0)
        unique_id_columns = st.multiselect("🆔 Kolumny do sprawdzenia unikalności", options=list(df.columns))
        text_len_analyze = st.checkbox("📏 Analiza długości tekstów", value=True)
        correlation_threshold = st.slider("📈 Próg korelacji", min_value=0.0, max_value=1.0, value=0.8, step=0.05)

    # Przycisk generowania raportu
    if st.button("🧠 Generuj Raport"):
        results = []

        check_missing_values(df, results)
        check_duplicates(df, results)
        analyze_text_columns(df, results)
        analyze_numeric_columns(df, results)

        if date_column:
            analyze_date_columns(df, results, date_column)

        if text_len_analyze:
            analyze_text_length(df, results)

        analyze_correlation(df, results, threshold=correlation_threshold)

        if unique_id_columns:
            check_unique_ids(df, results, unique_id_columns)

        analyze_binary_columns(df, results)

        # Renderowanie wyników
        st.subheader("📄 Raport")
        st.markdown("\n\n".join(results))
