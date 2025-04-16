import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from streamlit_ace import st_ace
import io
import contextlib

def register_custom_dataframe(df, name="custom_df_1"):
    """Zarejestruj nowy DataFrame w aplikacji."""
    st.session_state.uploaded_files[name] = df
    st.success(f"Dodano nowy DataFrame jako '{name}'!")

def render_code_editor_page():
    st.markdown("""
### 🖥️ Edytor kodu Python
<small style='color:gray'>
ℹ️ Możesz utworzyć zmienną <code>new_df</code> i przypisać do niej dane. 
Jeśli chcesz dodać je do aplikacji, użyj funkcji <code>register_custom_dataframe(new_df,name="new_df_name")</code>.
</small>
""", unsafe_allow_html=True)
    st.write("Wprowadź kod Python w edytorze poniżej. Możesz korzystać z załadowanych danych (zmienna `df`) oraz bibliotek takich jak pandas, matplotlib, czy seaborn.")

    # Sidebar: lista załadowanych plików
    st.sidebar.header("📁 Załadowane pliki")
    if st.session_state.uploaded_files:
        selected_file = st.sidebar.selectbox(
            "Wybierz plik do analizy",
            options=list(st.session_state.uploaded_files.keys()),
            help="Wybierz plik, aby uzyskać dostęp do jego danych w zmiennej `df`.",
        )
        st.sidebar.write("Podgląd pierwszych 5 wierszy:")
        st.sidebar.dataframe(st.session_state.uploaded_files[selected_file].head())
    else:
        selected_file = None
        st.sidebar.info("Brak załadowanych plików.")

    # Domyślny kod, który będzie wyświetlany na początku
    default_code = """def draw_tree(levels):
    \"""
    Rysuje drzewo z '#' z podaną liczbą poziomów.

    :param levels: Liczba poziomów drzewa.
    \"""
    for i in range(1, levels + 1):
        spaces = " " * (levels - i)
        hashes = "#" * (2 * i - 1)
        print(spaces + hashes + spaces)

    # Pień drzewa
    trunk_width = levels // 3 if levels > 3 else 1
    trunk_height = max(1, levels // 3)
    trunk_space = " " * (levels - trunk_width // 2 - 1)
    
    for _ in range(trunk_height):
        print(trunk_space + "#" * trunk_width)

# Przykład użycia
draw_tree(10)
"""

    # Wczytywanie kodu z session_state, aby kod nie znikał po przeładowaniu
    if "code_editor_content" not in st.session_state:
        st.session_state.code_editor_content = default_code

    # Edytor kodu z Ace
    user_code = st_ace(
        value=st.session_state.code_editor_content,
        placeholder="# Wprowadź swój kod Python tutaj\n",
        language="python",
        theme="github",
        key="code_editor",
        height=400,
    )

    # Zapisz aktualny stan kodu w session_state
    if user_code is not None:
        st.session_state.code_editor_content = user_code

    # Przyciski akcji
    col1, col2 = st.columns(2)
    with col1:
        run_code = st.button("▶️ Uruchom kod")
    with col2:
        clear_code = st.button("🗑️ Wyczyść kod")

    if clear_code:
        st.session_state.code_editor_content = default_code  # Wyczyść do domyślnego kodu
        st.experimental_rerun()

    # Kontekst wykonania kodu
    execution_context = {
        "st": st,
        "pd": pd,
        "plt": plt,
        "df": st.session_state.uploaded_files[selected_file] if selected_file else pd.DataFrame(),
        "register_custom_dataframe": register_custom_dataframe
    }

    # Uruchamianie kodu użytkownika
    if run_code and user_code.strip():
        st.write("### 🖥️ Wyniki wykonania kodu")
        with io.StringIO() as buf, contextlib.redirect_stdout(buf):
            try:
                exec(user_code, execution_context)
                st.text("Kod wykonano pomyślnie.")
            except Exception as e:
                st.error(f"Błąd wykonania kodu: {e}")
            output = buf.getvalue()
        if "new_df" in execution_context and isinstance(execution_context["new_df"], pd.DataFrame):
            new_df = execution_context["new_df"]
            
            # Znajdź unikalną nazwę dla nowego df
            counter = 1
            while f"custom_df_{counter}" in st.session_state.uploaded_files:
                counter += 1
            new_name = f"custom_df_{counter}"

            
            st.session_state.uploaded_files[new_name] = new_df
            
            st.dataframe(new_df.head())
        if output.strip():
            st.code(output)
