<<<<<<< HEAD
# RAG AGENT - UPLOAD A PDF AND ASK QUESTIONS ABOUT IT 
#STACK: OPENAI API, LANGCHAIN, STREAMLIT, FAISS

import os
import tempfile

import streamlit as st
from langchain_community.document_loaders import (PyPDFLoader,Docx2txtLoader,TextLoader,CSVLoader)
import pandas as pd
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

# PAGE SETUP
st.set_page_config(page_title=" Document RAG Agent", page_icon="📄", layout="wide")
st.title("📄 Document RAG Agent")
st.caption("Upload your documents and ask questions about it, Question should be related to the content.")

# SIDEBAR 
with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("OpenAI API Key", type="password", value=os.getenv("OPENAI_API_KEY", ""))
    model_name = st.selectbox("Model", ["gpt-3.5-turbo", "gpt-4","gpt-4.1-mini", "gpt-5-mini"])

    chunk_size = st.slider("Chunk size", 500, 2000, 1000, step=100)
    chunk_overlap = st.slider("Chunk overlap", 0, 400, 150, step=50)
    top_k = st.slider("Retrieved chunks (k)", 2, 10, 4)
    if st.button("Clear chat history"):
        st.session_state.pop("messages", None)
if not api_key:
    st.info("Enter your OpenAI API key in the sidebar to begin.")
    st.stop()

os.environ["OPENAI_API_KEY"] = api_key

# -----------------------------------------------------------------------------
# PDF upload + indexing (cached in session state)
# -----------------------------------------------------------------------------
uploaded_file = st.file_uploader("Upload a document", type=["pdf", "docx", "txt", "csv", "xlsx"])
if uploaded_file is not None:
    file_type = uploaded_file.name.split(".")[-1].lower()

def build_vectorstore(file_bytes: bytes,file_type: str,size: int,overlap: int) -> FAISS:
    """Load document, split into chunks, embed, and store in FAISS."""
    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file_type}") as tmp:
        tmp.write(file_bytes)
        tmp_path = tmp.name

    try:
        if file_type == "pdf":
            docs = PyPDFLoader(tmp_path).load()
        elif file_type == "docx":
            docs = Docx2txtLoader(tmp_path).load()
        elif file_type == "txt":
            docs = TextLoader(tmp_path).load()
        elif file_type in ["csv", "xlsx"]:
            # Handle CSV and Excel files
            df = pd.read_csv(tmp_path) if file_type == "csv" else pd.read_excel(tmp_path)
            docs = [Document(page_content=str(row.values), metadata={"source": tmp_path}) for _, row in df.iterrows()]
    finally:
        os.unlink(tmp_path)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=size,
        chunk_overlap=overlap,
        separators=["\n\n", "\n",".", " ", ""]
    )
    chunks = splitter.split_documents(docs)

    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    return FAISS.from_documents(chunks, embeddings)

if uploaded_file is not None:
    # Re-index only when a new file (or new settings) arrive
    file_sig = (uploaded_file.name, uploaded_file.size, chunk_size, chunk_overlap)
    if st.session_state.get("file_sig") != file_sig:
        with st.spinner("Reading and indexing document..."):
            st.session_state.vectorstore = build_vectorstore(
                uploaded_file.getvalue(), file_type, chunk_size, chunk_overlap
            )
        st.session_state.file_sig = file_sig
        st.session_state.messages = []
        st.success(f"Indexed **{uploaded_file.name}** and ask away")

# -----------------------------------------------------------------------------
# RAG chain
# -----------------------------------------------------------------------------
RAG_PROMPT = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a helpful assistant that answers questions strictly using the "
        "provided context from a document.\n"
        "Rules:\n"
        "1. Answer ONLY from the context below.\n"
        "2. If the answer is not in the context, say: "
        "\"I couldn't find that in the document.\"\n"
        "3. Cite the page number when available.\n\n"
        "Context:\n{context}"
    ),
    ("human", "{question}"),
])

def format_docs(docs) -> str:
    return "\n\n".join(
        f"[Page {d.metadata['page'] + 1}]\n{d.page_content}"
        if "page" in d.metadata
        else f"[Document]\n{d.page_content}"
        for d in docs
    )

def get_chain(vectorstore: FAISS, model: str, k: int):
    retriever = vectorstore.as_retriever(search_kwargs={"k": k})
    llm = ChatOpenAI(model=model, temperature=0)
    return (
        {
            "context": retriever | format_docs,
            "question": RunnablePassthrough()
        }
        | RAG_PROMPT
        | llm
        | StrOutputParser()
    ), retriever

# -----------------------------------------------------------------------------
# Chat interface
# -----------------------------------------------------------------------------
if "vectorstore" in st.session_state:
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Replay history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    question = st.chat_input("Ask a question about the document...")
    if question:
        st.session_state.messages.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.markdown(question)

        chain, retriever = get_chain(
            st.session_state.vectorstore, model_name, top_k
        )

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                answer = chain.invoke(question)
                st.markdown(answer)

            # Show the retrieved chunks for transparency
            with st.expander("🔍 Sources (retrieved chunks)"):
                for doc in retriever.invoke(question):
                    if "page" in doc.metadata:
                     st.markdown(f"**Page {doc.metadata['page'] + 1}**")
                else:
                    st.markdown("**Document**")

                st.text(doc.page_content[:500])
                st.divider()

        st.session_state.messages.append({"role": "assistant", "content": answer})
else:
    st.info("👈 Upload a document to get started.")
=======
# RAG AGENT - UPLOAD A PDF AND ASK QUESTIONS ABOUT IT 
#STACK: OPENAI API, LANGCHAIN, STREAMLIT, FAISS

import os
import tempfile

import streamlit as st
from langchain_community.document_loaders import (PyPDFLoader,Docx2txtLoader,TextLoader,CSVLoader)
import pandas as pd
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

# PAGE SETUP
st.set_page_config(page_title=" Document RAG Agent", page_icon="📄", layout="wide")
st.title("📄 Document RAG Agent")
st.caption("Upload your documents and ask questions about it, Question should be related to the content.")

# SIDEBAR 
with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("OpenAI API Key", type="password", value=os.getenv("OPENAI_API_KEY", ""))
    model_name = st.selectbox("Model", ["gpt-3.5-turbo", "gpt-4","gpt-4.1-mini", "gpt-5-mini"])

    chunk_size = st.slider("Chunk size", 500, 2000, 1000, step=100)
    chunk_overlap = st.slider("Chunk overlap", 0, 400, 150, step=50)
    top_k = st.slider("Retrieved chunks (k)", 2, 10, 4)
    if st.button("Clear chat history"):
        st.session_state.pop("messages", None)
if not api_key:
    st.info("Enter your OpenAI API key in the sidebar to begin.")
    st.stop()

os.environ["OPENAI_API_KEY"] = api_key

# -----------------------------------------------------------------------------
# PDF upload + indexing (cached in session state)
# -----------------------------------------------------------------------------
uploaded_file = st.file_uploader("Upload a document", type=["pdf", "docx", "txt", "csv", "xlsx"])
if uploaded_file is not None:
    file_type = uploaded_file.name.split(".")[-1].lower()

def build_vectorstore(file_bytes: bytes,file_type: str,size: int,overlap: int) -> FAISS:
    """Load document, split into chunks, embed, and store in FAISS."""
    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file_type}") as tmp:
        tmp.write(file_bytes)
        tmp_path = tmp.name

    try:
        if file_type == "pdf":
            docs = PyPDFLoader(tmp_path).load()
        elif file_type == "docx":
            docs = Docx2txtLoader(tmp_path).load()
        elif file_type == "txt":
            docs = TextLoader(tmp_path).load()
        elif file_type in ["csv", "xlsx"]:
            # Handle CSV and Excel files
            df = pd.read_csv(tmp_path) if file_type == "csv" else pd.read_excel(tmp_path)
            docs = [Document(page_content=str(row.values), metadata={"source": tmp_path}) for _, row in df.iterrows()]
    finally:
        os.unlink(tmp_path)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=size,
        chunk_overlap=overlap,
        separators=["\n\n", "\n",".", " ", ""]
    )
    chunks = splitter.split_documents(docs)

    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    return FAISS.from_documents(chunks, embeddings)

if uploaded_file is not None:
    # Re-index only when a new file (or new settings) arrive
    file_sig = (uploaded_file.name, uploaded_file.size, chunk_size, chunk_overlap)
    if st.session_state.get("file_sig") != file_sig:
        with st.spinner("Reading and indexing document..."):
            st.session_state.vectorstore = build_vectorstore(
                uploaded_file.getvalue(), file_type, chunk_size, chunk_overlap
            )
        st.session_state.file_sig = file_sig
        st.session_state.messages = []
        st.success(f"Indexed **{uploaded_file.name}** and ask away")

# -----------------------------------------------------------------------------
# RAG chain
# -----------------------------------------------------------------------------
RAG_PROMPT = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a helpful assistant that answers questions strictly using the "
        "provided context from a document.\n"
        "Rules:\n"
        "1. Answer ONLY from the context below.\n"
        "2. If the answer is not in the context, say: "
        "\"I couldn't find that in the document.\"\n"
        "3. Cite the page number when available.\n\n"
        "Context:\n{context}"
    ),
    ("human", "{question}"),
])

def format_docs(docs) -> str:
    return "\n\n".join(
        f"[Page {d.metadata['page'] + 1}]\n{d.page_content}"
        if "page" in d.metadata
        else f"[Document]\n{d.page_content}"
        for d in docs
    )

def get_chain(vectorstore: FAISS, model: str, k: int):
    retriever = vectorstore.as_retriever(search_kwargs={"k": k})
    llm = ChatOpenAI(model=model, temperature=0)
    return (
        {
            "context": retriever | format_docs,
            "question": RunnablePassthrough()
        }
        | RAG_PROMPT
        | llm
        | StrOutputParser()
    ), retriever

# -----------------------------------------------------------------------------
# Chat interface
# -----------------------------------------------------------------------------
if "vectorstore" in st.session_state:
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Replay history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    question = st.chat_input("Ask a question about the document...")
    if question:
        st.session_state.messages.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.markdown(question)

        chain, retriever = get_chain(
            st.session_state.vectorstore, model_name, top_k
        )

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                answer = chain.invoke(question)
                st.markdown(answer)

            # Show the retrieved chunks for transparency
            with st.expander("🔍 Sources (retrieved chunks)"):
                for doc in retriever.invoke(question):
                    if "page" in doc.metadata:
                     st.markdown(f"**Page {doc.metadata['page'] + 1}**")
                else:
                    st.markdown("**Document**")

                st.text(doc.page_content[:500])
                st.divider()

        st.session_state.messages.append({"role": "assistant", "content": answer})
else:
    st.info("👈 Upload a document to get started.")
>>>>>>> 7e554598c5ee128ccbdcdec0aa7b5a2e95a35bdc
