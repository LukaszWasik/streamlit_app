import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from pandas.api.types import is_datetime64_any_dtype

def check_missing_values(df, results):
    results.append("### Braki danych ###")
    missing_data = df.isnull().sum()
    missing_info = missing_data[missing_data > 0]
    if missing_info.empty:
        results.append("Brak brakujących danych.")
    else:
        for col, count in missing_info.items():
            percentage = (count / len(df)) * 100
            results.append(f"- {col}: {count} brakujących wartości ({percentage:.2f}%)")

def check_duplicates(df, results):
    results.append("\n### Sprawdzanie duplikatów ###")

    duplicates_count = df.duplicated().sum()
    results.append(f"Znaleziono {duplicates_count} duplikatów." if duplicates_count > 0 else "Brak duplikatów.")

def analyze_text_columns(df, results):
    results.append("### Kolumny tekstowe ###")
    text_columns = df.select_dtypes(include=['object']).columns
    if len(text_columns) > 0:
        for col in text_columns:
            unique_values = df[col].dropna().unique()
            unique_count = len(unique_values)
            if unique_count <= 10:
                results.append(f"- {col}: {list(unique_values)}")
            else:
                results.append(f"- {col}: {unique_count} unikalnych kategorii")
    else:
        results.append("Brak kolumn tekstowych.")

def analyze_numeric_columns(df, results):
    results.append("\n### Kolumny liczbowe ###")
    numeric_columns = df.select_dtypes(include=['number']).columns
    if len(numeric_columns) > 0:
        stats = df[numeric_columns].describe()
        for col in numeric_columns:

            # Obliczanie IQR
            unique_values = df[col].dropna().unique()
            unique_count = len(unique_values)
            # Obliczanie statystyk
            mean = df[col].mean()
            median = df[col].median()
            std_dev = df[col].std()
            quartiles = df[col].quantile([0.25, 0.5, 0.75]).to_dict()
            Q1 = quartiles[0.25]
            Q3 = quartiles[0.75]
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR

            # Zidentyfikowanie wartości odstających
            outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]

            if unique_count == 2:
                counts = df[col].value_counts().to_dict()
                results.append(f"- {col} (binary): {counts}")
            else:
                results.append(f"- {col}: min={df[col].min()}, max={df[col].max()}")
                results.append(f"  - Średnia: {mean:.2f}, Odchylenie standardowe: {std_dev:.2f}")
                results.append(f"  - Kwartyle: Q1={quartiles[0.25]:.2f}, Mediana={quartiles[0.5]:.2f}, Q3={quartiles[0.75]:.2f}")

                # Wypisanie wartości odstających tylko wtedy, gdy jest ich więcej niż 0
                if len(outliers) > 0:
                    results.append(f"  - Wartości odstające: {len(outliers)}")
                    results.append(f"    - Przykładowe wartości odstające: {outliers[col].head(5).tolist()}")
    else:
        results.append("Brak kolumn liczbowych.")

def analyze_date_columns(df, results, date_column, check_levels=['months', 'days', 'hours', 'minutes', 'seconds']):
    df[date_column] = pd.to_datetime(df[date_column], errors='coerce')
    print("Typ kolumny:", df[date_column].dtype)
    print("Czy kolumna istnieje?", date_column in df.columns)
    results.append(f"\n### Analiza kolumny datowej: {date_column} ###")    
    if date_column not in df.columns or not np.issubdtype(df[date_column].dtype, np.datetime64):
        results.append(f"- {date_column}: Nie podano kolumny lub podana kolumna nie istanieje (może nie poprawny typ danych)")
        return
    min_date = df[date_column].min()
    max_date = df[date_column].max()
    if pd.isnull(min_date) or pd.isnull(max_date):
        results.append(f"- {date_column}: Brak prawidłowych wartości datowych.")
        return
    results.append(f"- Zakres dat: od {min_date} do {max_date}")
    for level in check_levels:
        freq = {'months': 'M', 'days': 'D', 'hours': 'H', 'minutes': 'T', 'seconds': 'S'}.get(level)
        if freq:
            full_range = pd.date_range(start=min_date, end=max_date, freq=freq)
            existing_values = df[date_column].dropna().dt.to_period(freq)
            missing_values = sorted(set(full_range.to_period(freq)) - set(existing_values))
            results.append(f"  - Braki dla {level}: {len(missing_values)}")
            # Dodanie przykładowych brakujących wartości (max 5)
            if missing_values:
                example_missing = ', '.join(str(v) for v in missing_values[:5])
                results.append(f"    - Przykłady brakujących wartości: {example_missing}")
                
def analyze_text_length(df, results, text_length_columns="all"):
    results.append("\n### Wykrywanie nietypowych długości tekstowych ###")
    
    # Jeśli "text_length_columns" to "all", analizujemy wszystkie kolumny tekstowe
    if text_length_columns == "all":
        text_columns = df.select_dtypes(include=['object']).columns
    else:
        text_columns = [col for col in text_length_columns if col in df.columns and df[col].dtype == 'object']
    
    if len(text_columns) > 0:
        for col in text_columns:
            unusual_texts = df[col].dropna().apply(lambda x: isinstance(x, str) and (len(x) < 3 or len(x) > 50))
            unusual_count = unusual_texts.sum()
            if unusual_count > 0:
                results.append(f"- {col}: znaleziono {unusual_count} nietypowe wartości tekstowe.")
    else:
        results.append("Brak kolumn tekstowych do analizy.")


def analyze_correlation(df, results, threshold=0.8):
    results.append(f"\n### Analiza korelacji dla progu {threshold} ###")
    df_encoded = df.copy()
    for col in df.select_dtypes(include=['object']).columns:
        df_encoded[col] = LabelEncoder().fit_transform(df_encoded[col].astype(str))
    
    correlation_matrix = df_encoded.corr()
    upper_triangle = np.triu(np.ones(correlation_matrix.shape), k=1).astype(bool)
    correlated_pairs = correlation_matrix.where(upper_triangle & (abs(correlation_matrix) >= threshold)).stack()
    
    if not correlated_pairs.empty:
        for (col1, col2), correlation in correlated_pairs.items():
            results.append(f"- {col1} i {col2}: korelacja = {correlation:.2f}")
    else:
        results.append(f"Brak silnych korelacji (>= {threshold}).")

def check_unique_ids(df, results, unique_columns):
    results.append("\n### Sprawdzenie unikalności identyfikatorów ###")
    if unique_columns == "all":
        columns_to_check = df.columns
    elif isinstance(unique_columns, list):
        columns_to_check = unique_columns
    else:
        columns_to_check = []
    
    for col in columns_to_check:
        if col in df.columns:
            unique_count = df[col].nunique()
            total_count = len(df)
            if unique_count == total_count:
                results.append(f"- {col}: Wszystkie wartości są unikalne.")
            else:
                results.append(f"- {col}: {total_count - unique_count} duplikujących się wartości.")

def analyze_binary_columns(df, results):
    results.append("\n### Analiza równowagi w danych binarnych  ###")
    binary_columns = [col for col in df.select_dtypes(include=['number']).columns if len(df[col].dropna().unique()) == 2]
    if len(binary_columns) > 0:
        for col in binary_columns:
            counts = df[col].value_counts()
            imbalance = abs(counts.iloc[0] - counts.iloc[1]) / len(df) * 100
            results.append(f"- {col}: niezbalansowanie danych: {imbalance:.2f}% (0: {counts.iloc[0]}, 1: {counts.iloc[1]})")
    else:
        results.append("Brak kolumn binarnych w danych.")

def analyze_dataframe(df, unique_columns="all",text_length_columns="all",date_column=None,check_levels=None,threshold=0.8):
    results = []
    check_missing_values(df, results)
    check_duplicates(df, results)
    analyze_text_columns(df, results)
    analyze_numeric_columns(df, results)
    analyze_date_columns(df,results, date_column, check_levels)
    analyze_text_length(df, results)
    analyze_correlation(df, results,threshold)
    check_unique_ids(df, results, unique_columns)
    analyze_binary_columns(df, results)
    return "\n".join(results)
    
def save_report(txt_filename, html_filename, report_content):
    with open(txt_filename, "w", encoding="utf-8") as txt_file:
        txt_file.write(report_content)
    
    html_content = (
        "<html>"
        "<head><title>Raport Analizy Danych</title></head>"
        "<body><pre>" + report_content + "</pre></body>"
        "</html>"
    )
    
    with open(html_filename, "w", encoding="utf-8") as html_file:
        html_file.write(html_content)