import streamlit as st
from langchain.document_loaders import CSVLoader, UnstructuredExcelLoader
import tempfile
from utils import get_model_response

def main():
    st.title("Ask your Query")
    
    # Allow users to upload various file types
    uploaded_file = st.sidebar.file_uploader(
        "Choose a file (CSV, Excel)", 
        type=['csv', 'xlsx', 'xls'],  # Supporting CSV and Excel files
        label_visibility="visible"
    )
    
    if uploaded_file is not None:
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(uploaded_file.getvalue())
            temp_file_path = temp_file.name
            
            # Determine file type and use appropriate loader
            if uploaded_file.type == 'text/csv':
                file_loader = CSVLoader(file_path=temp_file_path, encoding='utf-8', csv_args={'delimiter': ','})
            elif uploaded_file.type in ['application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'application/vnd.ms-excel']:
                file_loader = UnstructuredExcelLoader(file_path=temp_file_path)
            else:
                st.error("Unsupported file type.")
                return
            
            try:
                data = file_loader.load()
            except Exception as e:
                st.error(f"Error loading file: {e}")
                return
            
            user_input = st.text_input("Your Message:")
            if user_input:
                with st.spinner("Processing your query..."):
                    try:
                        response = get_model_response(data, user_input)
                        st.write(response)
                    except Exception as e:
                        st.error(f"Error getting response: {e}")

if __name__ == "__main__":
    main()
