https://document-rag-agent-bzruyb8z39c6jafv5c8cec.streamlit.app/
# 📄 Multi-Document RAG Agent

A Streamlit-based RAG (Retrieval-Augmented Generation) application
that allows users to upload documents and ask questions about their content.

## 🚀 Project Overview

The application reads an uploaded document, processes its content,
and allows the user to interact with the document through a chat interface.

Instead of asking the LLM to answer from general knowledge,
the application retrieves relevant information from the uploaded document.

## 📁 Supported File Types

The application currently supports:

- PDF (.pdf)
- Word (.docx)
- Text (.txt)
- CSV (.csv)
- Excel (.xlsx)

## 🛠️ Technologies Used

- Python
- Streamlit
- LangChain
- OpenAI API
- FAISS
- Pandas
- PyPDF
- Docx2txt
- OpenPyXL

## 🧠 How It Works

1. The user enters an OpenAI API key.
2. The user uploads a supported document.
3. The application detects the file type.
4. The appropriate document loader reads the file.
5. The extracted text is divided into smaller chunks.
6. OpenAI Embeddings convert the chunks into vectors.
7. FAISS stores these vectors in a vector database.
8. The user asks a question about the uploaded document.
9. FAISS retrieves the most relevant document chunks.
10. The retrieved information is passed to the LLM as context.
11. The LLM generates an answer based on that context.
12. The application displays the answer in the chat interface.

## 🔍 RAG Architecture

Document → Loader → Text Chunks → Embeddings → FAISS

Question → Retriever → Relevant Chunks → LLM → Answer

## ✨ Features

- Multiple document format support
- Document-based question answering
- Semantic search using embeddings
- FAISS vector storage
- Adjustable chunk size and overlap
- Adjustable number of retrieved chunks
- Chat history using Streamlit session state
- Source chunks displayed for transparency
- OpenAI model selection

## 🎯 Purpose

This project demonstrates how Retrieval-Augmented Generation
can be used to build an AI assistant that answers questions
using information retrieved from user-provided documents.