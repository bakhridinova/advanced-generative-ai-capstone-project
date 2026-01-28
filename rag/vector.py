import os
import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document

from config import (
    API_KEY_OPENAI,
    PATH_VECTOR_DB,
    PATH_DOCUMENTS,
    TEXT_CHUNK_SIZE,
    TEXT_CHUNK_OVERLAP
)


class DocumentProcessor:
    def __init__(self):
        self.embedding_model = OpenAIEmbeddings(openai_api_key=API_KEY_OPENAI)
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=TEXT_CHUNK_SIZE,
            chunk_overlap=TEXT_CHUNK_OVERLAP
        )

    def locate_pdf_files(self):
        if not os.path.isdir(PATH_DOCUMENTS):
            return []
        return [f for f in os.listdir(PATH_DOCUMENTS) if f.lower().endswith('.pdf')]

    def locate_text_files(self):
        if not os.path.isdir(PATH_DOCUMENTS):
            return []
        return [f for f in os.listdir(PATH_DOCUMENTS) if f.lower().endswith('.txt')]

    def extract_pdf_content(self, pdf_filename):
        file_path = os.path.join(PATH_DOCUMENTS, pdf_filename)
        loader = PyPDFLoader(file_path)
        return loader.load()

    def extract_text_content(self, text_filename):
        file_path = os.path.join(PATH_DOCUMENTS, text_filename)
        try:
            with open(file_path, 'r', encoding='utf-8') as fh:
                content = fh.read()
            return [Document(page_content=content, metadata={"source": file_path})]
        except Exception as err:
            st.warning(f"Failed to read {text_filename}: {err}")
            return []

    def gather_all_documents(self):
        documents = []

        pdf_list = self.locate_pdf_files()
        for pdf in pdf_list:
            documents.extend(self.extract_pdf_content(pdf))

        text_list = self.locate_text_files()
        for txt in text_list:
            documents.extend(self.extract_text_content(txt))

        return documents

    def create_text_chunks(self, documents):
        return self.text_splitter.split_documents(documents)

    def build_database(self, chunks):
        return Chroma.from_documents(
            documents=chunks,
            embedding=self.embedding_model,
            persist_directory=PATH_VECTOR_DB
        )


class VectorStoreManager:
    def __init__(self):
        self.processor = DocumentProcessor()

    def database_exists(self):
        return os.path.isdir(PATH_VECTOR_DB) and os.listdir(PATH_VECTOR_DB)

    def load_persisted_database(self):
        if self.database_exists():
            return Chroma(
                persist_directory=PATH_VECTOR_DB,
                embedding_function=self.processor.embedding_model
            )
        return None

    def count_available_documents(self):
        pdf_count = len(self.processor.locate_pdf_files())
        txt_count = len(self.processor.locate_text_files())
        return pdf_count + txt_count

    def create_fresh_database(self):
        total_docs = self.count_available_documents()

        if total_docs == 0:
            return None

        with st.spinner(f"Indexing {total_docs} document(s)... Please wait."):
            all_docs = self.processor.gather_all_documents()

        chunks = self.processor.create_text_chunks(all_docs)
        return self.processor.build_database(chunks)

    def get_or_create_database(self):
        existing = self.load_persisted_database()
        if existing:
            return existing
        return self.create_fresh_database()


@st.cache_resource(show_spinner=False)
def setup_vector_store():
    manager = VectorStoreManager()
    return manager.get_or_create_database()

