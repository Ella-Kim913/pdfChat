import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings, HuggingFacePipeline
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from htmlTemplets import css, bot_template, user_template
from langchain_huggingface.llms import HuggingFaceEndpoint

def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def get_text_chunks(raw_text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=500,
        chunk_overlap=100,
        length_function=len
    )
    chunks = text_splitter.split_text(raw_text)
    

    return chunks

def get_vectorstore(text_chunks):
    embedding_model = "sentence-transformers/all-MiniLM-L6-v2"
    embeddings = HuggingFaceEmbeddings(model_name=embedding_model)
    vectorstore = FAISS.from_texts(text_chunks, embeddings)
    
    return vectorstore

def load_llm_pipeline():
    llm_pipeline = HuggingFacePipeline.from_model_id(
        model_id="MBZUAI/LaMini-T5-738M",
        task="text2text-generation",
        pipeline_kwargs={
            "max_length": 512,  # Adjust based on model capacity
            # "max_new_tokens": 100,  # Larger token limit for generation
            "truncation": True,    # Ensure input is truncated if too long
        },
    )
    return llm_pipeline


def get_conversation_chain(vectorstore):

    llm = load_llm_pipeline()
    # Create the memory object for conversation history
    memory = ConversationBufferMemory(memory_key='chat_history',  output_key='answer', return_messages=True)

    # Create the ConversationalRetrievalChain using the wrapped LLM
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,  # Use the pipeline-wrapped model
        retriever=vectorstore.as_retriever(),
        chain_type="stuff",
        return_source_documents=True,
        memory=memory
    )

    
    return conversation_chain

def handle_user_input(user_question):
    if st.session_state.conversation:
        response = st.session_state.conversation({'question': user_question})
        st.session_state.chat_history = response['chat_history']

        for i, message in enumerate(st.session_state.chat_history):
            if i % 2 == 1:
                st.write(bot_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)
            else:
                st.write(user_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)
    else:
        st.write("Conversation chain is not initialized. Please process the PDFs first.")

def main():
    load_dotenv()
    st.set_page_config(page_title="Chat With multiple PDFs", page_icon=":books:")

    st.write(css, unsafe_allow_html=True)

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    st.header("Chat With multiple PDFs :books:")
    user_question = st.text_input("Ask a question about your documents:")

    if user_question:
        handle_user_input(user_question)

    with st.sidebar:
        st.subheader("Your documents")
        pdf_docs = st.file_uploader("Upload your PDFs", type="pdf", accept_multiple_files=True)
        if st.button("Process"):
            with st.spinner("Processing..."):
                raw_text = get_pdf_text(pdf_docs)
                text_chunks = get_text_chunks(raw_text)
                vectorstore = get_vectorstore(text_chunks)
                st.session_state.conversation = get_conversation_chain(vectorstore)


if __name__ == "__main__":
    main()
