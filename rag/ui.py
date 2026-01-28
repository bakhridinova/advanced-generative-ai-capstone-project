import os
import streamlit as st
from config import PATH_DOCUMENTS


def setup_page_layout():
    st.set_page_config(
        page_title="Toyota",
        page_icon="🛻",
        layout="centered"
    )


def show_header():
    st.markdown("# 🛻 Toyota Assistant")


def get_document_counts():
    if not os.path.isdir(PATH_DOCUMENTS):
        return 0, 0, []

    all_files = os.listdir(PATH_DOCUMENTS)
    supported_files = [f for f in all_files if f.lower().endswith(('.pdf', '.txt'))]
    pdf_total = sum(1 for f in supported_files if f.lower().endswith('.pdf'))
    txt_total = sum(1 for f in supported_files if f.lower().endswith('.txt'))
    return pdf_total, txt_total, sorted(supported_files)


def show_document_stats():
    st.markdown("### 📚 Loaded Documents")
    pdf_count, txt_count, file_list = get_document_counts()
    if pdf_count == 0 and txt_count == 0:
        st.warning("No documents folder found")
        return

    metric_col1, metric_col2 = st.columns(2)
    with metric_col1:
        st.metric("PDF Files", pdf_count)
    with metric_col2:
        st.metric("TXT Files", txt_count)
    with st.expander("📄 View Files"):
        for filename in file_list:
            st.text(f"• {filename}")


def show_company_details():
    st.markdown("### ℹ️ About")
    st.caption("**AutoSupport AI Ltd.**")
    st.caption("AI-powered customer support for Toyota vehicles")
    st.caption("📞 +1-800-123-4567")
    st.caption("📧 support@autosupport.ai")


def render_sidebar():
    with st.sidebar:
        st.header("📊 Knowledge Base")
        show_document_stats()
        st.divider()
        show_company_details()


def init_session_data():
    if "conversation_history" not in st.session_state:
        st.session_state.conversation_history = []


def show_chat_messages():
    for msg in st.session_state.conversation_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
