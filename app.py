
import streamlit as st
import pandas as pd
import os
from io import BytesIO


def set_theme():
    """Toggle between light and dark mode."""
    theme = st.radio("🔍 Select Theme:", ["🌞 Light", "🌙 Dark"], horizontal=True)
    theme_styles = {
        "🌞 Light": {"background": "#ffffff", "container": "#f5f5f5", "text": "black"},
        "🌙 Dark": {"background": "#121212", "container": "#1e1e1e", "text": "white"}
    }
    selected = theme_styles[theme]
    st.markdown(
        f"""
        <style>
            .stApp {{ background-color: {selected['background']}; color: {selected['text']}; }}
            .block-container {{ background-color: {selected['container']}; padding: 2rem; border-radius: 10px; margin-top: 50px; }}
            .stButton>button, .stDownloadButton>button {{ background-color: #0078D7; color: white; border-radius: 5px; padding: 10px; transition: 0.3s; }}
            .stButton>button:hover, .stDownloadButton>button:hover {{ background-color: #005a9e; }}
            div[data-testid="stMarkdownContainer"] label, div[data-testid="stCheckbox"] label {{ color: {selected['text']} !important; }}
        </style>
        """,
        unsafe_allow_html=True
    )

st.set_page_config(page_title="📑🧹 Data Sweeper", layout="wide")
st.title("📑🧹 Advanced Data Sweeper")
st.write("🧹 Convert CSV & Excel files effortlessly with data cleaning and visualization.")

set_theme()

uploaded_files = st.file_uploader("📂 Upload CSV or Excel files:", type=["csv", "xlsx"], accept_multiple_files=True)

if uploaded_files:
    for index, file in enumerate(uploaded_files):
        file_extension = os.path.splitext(file.name)[-1].lower()
        
        try:
            df = pd.read_csv(file) if file_extension == ".csv" else pd.read_excel(file)
        except Exception as e:
            st.error(f"❌ Error reading file {file.name}: {e}")
            continue

        st.write(f"**📄 File:** {file.name} ({file.size / 1024:.2f} KB)")
        st.dataframe(df.head())

        # 🛠️ Data Cleaning Options
        st.subheader("🛠️ Data Cleaning Options")
        if st.checkbox(f"🧼 Clean Data - {file.name}"):
            if st.button(f"🚫 Remove Duplicates - {file.name}"):
                df.drop_duplicates(inplace=True)
                st.success("✔️ Duplicates Removed!")

            if st.button(f"🩹 Fill Missing Values - {file.name}"):
                df.fillna(df.select_dtypes(include='number').mean(), inplace=True)
                st.success("✔️ Missing Values Filled!")
        
        # 🎯 Select Columns to Convert
        st.subheader("🎯 Select Columns to Convert")
        columns = st.multiselect(f"Choose Columns for {file.name}", df.columns, default=df.columns)
        df = df[columns]
        
        # 📊 Data Visualization
        st.subheader("📊 Data Visualization")
        if st.checkbox(f"📉 Show Chart - {file.name}"):
            numeric_cols = df.select_dtypes(include='number').columns
            if len(numeric_cols) >= 2:
                st.bar_chart(df[numeric_cols].iloc[:, :2])
            else:
                st.warning("⚠️ Not enough numeric columns for chart visualization.")

        # 🔄 Convert File
        st.subheader("🔄 Convert File")
        conversion_type = st.radio("🔃 Convert To:", ["📄 CSV", "📂 Excel"], key=f"convert_{file.name}_{index}")
        
        if st.button(f"🔄 Convert {file.name}"):
            buffer = BytesIO()
            if conversion_type == "📄 CSV":
                df.to_csv(buffer, index=False)
                mime_type, ext = "text/csv", ".csv"
            else:
                df.to_excel(buffer, index=False, engine='openpyxl')
                mime_type, ext = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", ".xlsx"

            buffer.seek(0)
            st.download_button("⬇️ Download", data=buffer, file_name=file.name.replace(file_extension, ext), mime=mime_type)

st.success("🎉 Processing Complete!")

# Footer message
st.markdown("---")
st.markdown("<p style='text-align: center;'>This code was created by Rabnawaz Dogar</p>", unsafe_allow_html=True)

