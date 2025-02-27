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

# import streamlit as st
# import pandas as pd
# import os
# from io import BytesIO

# # Configure the Streamlit app's appearance and layout
# # 'page_title' sets the browser tab title
# # 'layout="wide"' allows more horizontal space, improving the display for tables and graphs
# st.set_page_config(page_title="Data Sweeper", layout="wide")

# # Custom CSS for styling the app with dark mode aesthetics
# # This enhances the UI by setting background colors, button styles, and text formatting
# st.markdown(
#     """
#     <style>
#         .main {
#             background-color: #121212;  /* Overall dark background for the main page */
#         }
#         .block-container {
#             padding: 3rem 2rem;  /* Padding around main container for spacing */
#             border-radius: 12px;  /* Rounds the corners of the container */
#             background-color: #1e1e1e;  /* Slightly lighter shade for contrast */
#             box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);  /* Adds subtle shadow for depth */
#         }
#         h1, h2, h3, h4, h5, h6 {
#             color: #66c2ff;  /* Light blue color for headings to stand out */
#         }
#         .stButton>button {
#             border: none;
#             border-radius: 8px;  /* Rounds button edges */
#             background-color: #0078D7;  /* Primary blue for buttons */
#             color: white;  /* White text for contrast */
#             padding: 0.75rem 1.5rem;  /* Enlarges button for better interaction */
#             font-size: 1rem;  /* Readable button text */
#             box-shadow: 0 4px 10px rgba(0, 0, 0, 0.4);  /* Shadow for button depth */
#         }
#         .stButton>button:hover {
#             background-color: #005a9e;  /* Darker blue on hover for visual feedback */
#             cursor: pointer;
#         }
#         .stDataFrame, .stTable {
#             border-radius: 10px;  /* Smooth edges for data tables and frames */
#             overflow: hidden;  /* Prevents data from overflowing the container */
#         }
#         .css-1aumxhk, .css-18e3th9 {
#             text-align: left;
#             color: white;  /* Ensures all standard text is white for readability */
#         }
#         .stRadio>label {
#             font-weight: bold;
#             color: white;
#         }
#         .stCheckbox>label {
#             color: white;
#         }
#         .stDownloadButton>button {
#             background-color: #28a745;  /* Green color for download buttons */
#             color: white;
#         }
#         .stDownloadButton>button:hover {
#             background-color: #218838;  /* Darker green on hover for download buttons */
#         }
#     </style>
#     """,
#     unsafe_allow_html=True  # 'unsafe_allow_html' permits raw HTML/CSS embedding in the Streamlit app
# )

# # Display the main app title and introductory text
# st.title("Advanced Data Sweeper")  # Large, eye-catching title
# st.write("Transform your files between CSV and Excel formats with built-in data cleaning and visualization.")

# # File uploader widget that accepts CSV and Excel files
# # 'accept_multiple_files=True' allows batch uploading multiple files at once
# uploaded_files = st.file_uploader("Upload your files (CSV or Excel):", type=["csv", "xlsx"], accept_multiple_files=True)

# # Processing logic for uploaded files (if any files are uploaded)
# if uploaded_files:
#     for file in uploaded_files:
#         # Extract the file extension to determine if it's CSV or Excel
#         file_extension = os.path.splitext(file.name)[-1].lower()
        
#         # Read the uploaded file into a pandas DataFrame based on its extension
#         if file_extension == ".csv":
#             df = pd.read_csv(file)  # Read CSV files
#         elif file_extension == ".xlsx":
#             df = pd.read_excel(file)  # Read Excel files
#         else:
#             # Show an error message if the file type is unsupported
#             st.error(f"Unsupported file type: {file_extension}")
#             continue
        
#         # Display uploaded file information (name and size)
#         st.write(f"**📄 File Name:** {file.name}")
#         st.write(f"**📏 File Size:** {file.size / 1024:.2f} KB")  # File size in KB

#         # Preview the first 5 rows of the uploaded file
#         st.write("🔍 Preview of the Uploaded File:")
#         st.dataframe(df.head())  # Display a scrollable preview of the data
        
#         # Section for data cleaning options
#         st.subheader("🛠️ Data Cleaning Options")
#         if st.checkbox(f"Clean Data for {file.name}"):
#             col1, col2 = st.columns(2)  # Split cleaning options into two columns
#             with col1:
#                 # Button to remove duplicate rows from the DataFrame
#                 if st.button(f"Remove Duplicates from {file.name}"):
#                     df.drop_duplicates(inplace=True)
#                     st.write("Duplicates Removed!")
#             with col2:
#                 # Button to fill missing numeric values with column means
#                 if st.button(f"Fill Missing Values for {file.name}"):
#                     numeric_cols = df.select_dtypes(include=['number']).columns
#                     df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
#                     st.write("Missing Values in Numeric Columns Filled with Column Means!")

#         # Section to choose specific columns to convert
#         st.subheader("🎯 Select Columns to Convert")
#         columns = st.multiselect(f"Choose Columns for {file.name}", df.columns, default=df.columns)
#         df = df[columns]  # Filters the DataFrame to the selected columns
        
#         # Visualization section for uploaded data
#         st.subheader("📊 Data Visualization")
#         if st.checkbox(f"Show Visualization for {file.name}"):
#             st.bar_chart(df.select_dtypes(include='number').iloc[:, :2])  # Plot the first two numeric columns as a bar chart
        
#         # Section to choose file conversion type (CSV or Excel)
#         st.subheader("🔄 Conversion Options")
#         conversion_type = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=file.name)
#         if st.button(f"Convert {file.name}"):
#             buffer = BytesIO()  # Creates in-memory buffer for file output
#             if conversion_type == "CSV":
#                 df.to_csv(buffer, index=False)  # Save DataFrame as CSV in buffer
#                 file_name = file.name.replace(file_extension, ".csv")
#                 mime_type = "text/csv"
#             elif conversion_type == "Excel":
#                 df.to_excel(buffer, index=False, engine='openpyxl')  # Save as Excel using openpyxl
#                 file_name = file.name.replace(file_extension, ".xlsx")
#                 mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
#             buffer.seek(0)
            
#             # Download button for the converted file
#             st.download_button(
#                 label=f"⬇️ Download {file.name} as {conversion_type}",
#                 data=buffer,
#                 file_name=file_name,
#                 mime=mime_type
#             )

# st.success("🎉 All files processed successfully!")  # Display success message when all files are processed
