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

from fpdf import FPDF
import tempfile
import os

def save_report_as_pdf(results):
    pdf = FPDF()
    pdf.add_page()

    # Dodanie czcionki wspierającej UTF-8 (np. DejaVuSans)
    font_path = os.path.join(os.path.dirname(__file__), "..","fonts", "DejaVuSans.ttf")  # Upewnij się, że masz ten plik w folderze "fonts/"
    font_path = os.path.abspath(font_path)
    pdf.add_font("DejaVu", "", font_path, uni=True)
    pdf.set_font("DejaVu", size=12)

    for line in results:
        pdf.multi_cell(0, 10, line)

    tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    pdf.output(tmp_file.name)
    return tmp_file.name

def render_report_page():
    st.header("📑 Generowanie Raportu")

    if "uploaded_files" not in st.session_state or not st.session_state.uploaded_files:
        st.warning("Brak załadowanych plików. Najpierw załaduj pliki CSV.")
        return

    st.subheader("🔍 Wybierz dane do analizy")
    file_name = st.selectbox("📂 Wybierz plik", options=list(st.session_state.uploaded_files.keys()))
    df = st.session_state.uploaded_files[file_name]

    # 🧩 Wybór analiz
    st.subheader("🧩 Wybierz, które analizy mają zostać wykonane:")
    do_missing = st.checkbox("🕳️ Sprawdzenie brakujących wartości", value=True)
    do_duplicates = st.checkbox("🧬 Sprawdzenie duplikatów", value=True)
    do_text = st.checkbox("🔤 Analiza kolumn tekstowych", value=True)
    do_numeric = st.checkbox("🔢 Analiza kolumn numerycznych", value=True)
    do_dates = st.checkbox("🕒 Analiza kolumn datowych", value=True)
    do_text_len = st.checkbox("📏 Analiza długości tekstów", value=True)
    do_corr = st.checkbox("📈 Analiza korelacji", value=True)
    do_unique_ids = st.checkbox("🆔 Sprawdzenie unikalności kolumn", value=True)
    do_binary = st.checkbox("🔘 Analiza kolumn binarnych", value=True)

    # Ustawienia opcjonalne
    with st.expander("⚙️ Ustawienia zaawansowane"):
        date_columns = st.multiselect("🕒 Kolumny datowe (jeśli wybrano analizę dat)", options=list(df.columns))
        unique_id_columns = st.multiselect("🆔 Kolumny do sprawdzenia unikalności", options=list(df.columns))
        correlation_threshold = st.slider("📈 Próg korelacji", min_value=0.0, max_value=1.0, value=0.8, step=0.05)

    # Konfiguracja poziomów dla kolumn datowych
    date_columns_config = {}
    if do_dates and date_columns:
        st.subheader("⚙️ Konfiguracja kolumn datowych")
        for col in date_columns:
            with st.expander(f"🕒 Ustawienia dla: {col}"):
                selected_levels = st.multiselect(
                    f"Poziomy do sprawdzenia dla {col}",
                    options=['months', 'days', 'hours', 'minutes', 'seconds'],
                    default=['months', 'days']
                )
                date_columns_config[col] = selected_levels

    # Przycisk generowania raportu
    if st.button("🧠 Generuj Raport"):
        results = []

        if do_missing:
            check_missing_values(df, results)
        if do_duplicates:
            check_duplicates(df, results)
        if do_text:
            analyze_text_columns(df, results)
        if do_numeric:
            analyze_numeric_columns(df, results)
        if do_dates:
            for col, levels in date_columns_config.items():
                analyze_date_columns(df, results, col, check_levels=levels)
        if do_text_len:
            analyze_text_length(df, results)
        if do_corr:
            analyze_correlation(df, results, threshold=correlation_threshold)
        if do_unique_ids and unique_id_columns:
            check_unique_ids(df, results, unique_id_columns)
        if do_binary:
            analyze_binary_columns(df, results)
        
        # Renderowanie wyników
        st.subheader("📄 Raport")
        if results:
            st.markdown("\n\n".join(results))
            
            # Eksport do PDF
            pdf_path = save_report_as_pdf(results)
            with open(pdf_path, "rb") as f:
                st.download_button("⬇️ Pobierz jako PDF", f.read(), file_name="raport.pdf")

            # Usuwanie tymczasowego pliku PDF
            os.remove(pdf_path)
            
        else:
            st.info("Nie wybrano żadnych analiz do wykonania.")
