import streamlit as st
import pandas as pd
import os
from io import BytesIO

def set_theme():
    """Toggle between light and dark mode."""
    theme = st.radio("🔍 Select Theme:", ["🌞 Light", "🌙 Dark"], horizontal=True)
    if theme == "🌞 Light":
        st.markdown(
            """
            <style>
                body { background-color: #ffffff; color: #000000; }
                .block-container { background-color: #f5f5f5; padding: 2rem; border-radius: 10px; margin-top: 50px; }
                .stButton>button, .stDownloadButton>button { background-color: #0078D7; color: white; border-radius: 5px; padding: 10px; transition: 0.3s; }
                .stButton>button:hover, .stDownloadButton>button:hover { background-color: #005a9e; }
                h1, h2, h3, h4, h5, h6, p, label, .stRadio, .stCheckbox, .stDataFrame, .stTable { color: #000000 !important; }
            </style>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            """
            <style>
                body { background-color: #121212; color: #ffffff; }
                .block-container { background-color: #1e1e1e; padding: 2rem; border-radius: 10px; margin-top: 50px; }
                .stButton>button, .stDownloadButton>button { background-color: #0078D7; color: white; border-radius: 5px; padding: 10px; transition: 0.3s; }
                .stButton>button:hover, .stDownloadButton>button:hover { background-color: #005a9e; }
                h1, h2, h3, h4, h5, h6, p, label, .stRadio, .stCheckbox, .stDataFrame, .stTable { color: #ffffff !important; }
            </style>
            """,
            unsafe_allow_html=True
        )

st.set_page_config(page_title="🔍🧹 Data Sweeper", layout="wide")
st.title("🔍🧹 Advanced Data Sweeper")
st.write("🧹 Convert CSV & Excel files effortlessly with data cleaning and visualization.")

set_theme()

uploaded_files = st.file_uploader("📂 Upload CSV or Excel files:", type=["csv", "xlsx"], accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        file_extension = os.path.splitext(file.name)[-1].lower()
        df = pd.read_csv(file) if file_extension == ".csv" else pd.read_excel(file)
        st.write(f"**📄 File:** {file.name} ({file.size / 1024:.2f} KB)")
        st.dataframe(df.head())
        
        st.subheader("🛠️ Data Cleaning Options")
        if st.checkbox(f"🧼 Clean Data - {file.name}"):
            if st.button(f"🚫 Remove Duplicates - {file.name}"):
                df.drop_duplicates(inplace=True)
                st.write("✔️ Duplicates Removed!")
            if st.button(f"🩹 Fill Missing Values - {file.name}"):
                df.fillna(df.mean(), inplace=True)
                st.write("✔️ Missing Values Filled!")
        
        st.subheader("📊 Data Visualization")
        if st.checkbox(f"📉 Show Chart - {file.name}"):
            st.bar_chart(df.select_dtypes(include='number').iloc[:, :2])
        
        st.subheader("🔄 Convert File")
        conversion_type = st.radio("🔃 Convert To:", ["📄 CSV", "📂 Excel"], key=file.name)
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
