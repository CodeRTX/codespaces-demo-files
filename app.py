import streamlit as st
import os
import pdfplumber

local_llm = "llama3"
tavily_api_key = os.environ['TAVILY_API_KEY'] = 'API_KEY'
st.title("Multi-PDF ChatBot using LLAMA3 & Adaptive RAG")
user_input = st.text_input("Question:", placeholder="Ask about your PDF", key='input')

with st.sidebar:
    uploaded_files = st.file_uploader("Upload your file", type=['pdf'], accept_multiple_files=True)
    process = st.button("Process")

if process:
    if not uploaded_files:
        st.warning("Please upload at least one PDF file.")
        st.stop()

    # Ensure the temp directory exists
    temp_dir = 'temp/'
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    # Process each uploaded file
    for uploaded_file in uploaded_files:
        temp_file_path = os.path.join(temp_dir, uploaded_file.name)

        # Save the file to disk
        with open(temp_file_path, "wb") as file:
            file.write(uploaded_file.getbuffer())  # Use getbuffer() for Streamlit's UploadedFile

        # Load the PDF using pdfplumber
        try:
            with pdfplumber.open(temp_file_path) as pdf:
                data = []
                for page in pdf.pages:
                    text = page.extract_text()
                    data.append(text)
                st.write(f"Data loaded for {uploaded_file.name}")
                st.write("\n".join(data))
        except Exception as e:
            st.error(f"Failed to load {uploaded_file.name}: {str(e)}")
