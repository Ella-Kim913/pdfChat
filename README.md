# Local LLM Chatbot with PDF

## Webpage
You can interact with the live version of the app here: [https://ella-kim913-pdfchat-app-k32rgb.streamlit.app/](https://ella-kim913-pdfchat-app-k32rgb.streamlit.app/)

## Overview
This project provides a chatbot service powered by an open-source LLM (Large Language Model) from Hugging Face, using the LangChain framework and Streamlit UI. The chatbot allows users to upload multiple PDFs and ask questions about their content. The system will generate relevant answers based on the information extracted from the PDFs.

### Main Stack

- **Embedding Model**: [all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2)
- **LLM Model**: [LaMini-T5-738M](https://huggingface.co/MBZUAI/LaMini-T5-738M)
- **Vector Store**: FAISS
- **Backend**: Python, Hugging Face Transformers, LangChain
- **Frontend**: Streamlit

## Features

- Upload multiple PDFs and ask questions about their content.
- Embedding and retrieval using FAISS for efficient document searching.
- LLM-powered chatbot that generates answers based on the content of the uploaded PDFs.

### Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/username/repository.git
    cd repository
    ```

2. **Create and activate a virtual environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required packages**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Set up environment variables**:
    - Create a `.env` file in the project root and add any necessary environment variables (e.g., API keys for Hugging Face).

    Example `.env` file:
    ```plaintext
    HUGGINGFACEHUB_API_TOKEN=your_huggingface_api_key
    ```

5. **Run the Streamlit application**:
    ```bash
    streamlit run app.py
    ```
