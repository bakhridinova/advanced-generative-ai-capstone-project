import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage

from config import API_KEY_OPENAI, TOKEN_GITHUB, REPOSITORY_GITHUB
from vector import setup_vector_store
from tools import build_agent_tools
from agent import create_agent_executor
from ui import setup_page_layout, show_header, render_sidebar, init_session_data, show_chat_messages


class ApplicationController:
    def __init__(self):
        self.validate_configuration()
        self.setup_interface()
        self.knowledge_base = None
        self.agent_executor = None

    def validate_configuration(self):
        required = [API_KEY_OPENAI, TOKEN_GITHUB, REPOSITORY_GITHUB]
        if not all(required):
            st.error("Missing required configuration. Please check your .env file.")
            st.stop()

    def setup_interface(self):
        setup_page_layout()
        show_header()
        render_sidebar()

    def initialize_system(self):
        self.knowledge_base = setup_vector_store()
        if self.knowledge_base is None:
            st.warning("No documents found in **documents/** folder. Please add PDF or TXT files and refresh.")
            st.stop()

        agent_tools = build_agent_tools(self.knowledge_base)
        self.agent_executor = create_agent_executor(agent_tools)

    def prepare_conversation_context(self):
        messages = []
        for entry in st.session_state.conversation_history:
            if entry["role"] == "user":
                messages.append(HumanMessage(content=entry["content"]))
            else:
                messages.append(AIMessage(content=entry["content"]))
        return messages

    def generate_response(self, query):
        context = self.prepare_conversation_context()

        with st.spinner("Processing your request..."):
            try:
                result = self.agent_executor.invoke({
                    "input": query,
                    "chat_history": context
                })
                return result["output"]
            except Exception as error:
                return f"⚠️ An error occurred while processing your request.\n\nDetails: {error}"

    def handle_user_input(self):
        query = st.chat_input("How can I assist you with your Toyota today?")

        if query:
            st.session_state.conversation_history.append({"role": "user", "content": query})

            with st.chat_message("user"):
                st.markdown(query)

            response = self.generate_response(query)

            with st.chat_message("assistant"):
                st.markdown(response)

            st.session_state.conversation_history.append({"role": "assistant", "content": response})

    def run(self):
        init_session_data()
        self.initialize_system()
        show_chat_messages()
        self.handle_user_input()


def main():
    controller = ApplicationController()
    controller.run()


if __name__ == "__main__":
    main()

