import os
from langchain.tools import tool
from ticket import create_support_ticket


class ToolFactory:
    def __init__(self, vector_store):
        self.vector_store = vector_store
        self.retrieval_limit = 4

    def format_source_citation(self, doc):
        filename = os.path.basename(doc.metadata.get('source', 'unknown'))
        page_num = doc.metadata.get('page')

        citation_header = f"Source: {filename}"
        if page_num is not None:
            citation_header += f" (page {page_num})"

        return f"{citation_header}\n{doc.page_content.strip()}"

    def retrieve_documents(self, query):
        retriever = self.vector_store.as_retriever(
            search_kwargs={"k": self.retrieval_limit}
        )
        return retriever.invoke(query)

    def validate_ticket_data(self, name, email, summary, description):
        fields = [name.strip(), email.strip(), summary.strip(), description.strip()]
        return all(fields)

    def create_search_tool(self):
        @tool
        def search_knowledge_base(search_query: str) -> str:
            """
            Searches through vehicle documentation and FAQ database for relevant information.
            This tool should be used for any inquiry about vehicle features, troubleshooting,
            maintenance procedures, specifications, company policies, or contact information.

            Args:
                search_query: User's question or search term

            Returns:
                Formatted search results with source attribution
            """
            documents = self.retrieve_documents(search_query)

            if not documents:
                return "No relevant information was found in the knowledge base."

            citations = [self.format_source_citation(doc) for doc in documents]
            return "\n\n".join(citations)

        return search_knowledge_base

    def create_ticket_tool(self):
        @tool
        def submit_support_ticket(summary: str, description: str, user_name: str, user_email: str) -> str:
            """
            Creates a support ticket in the issue tracking system.

            IMPORTANT CONSTRAINTS:
            - Only invoke this tool when ALL FOUR parameters have been explicitly provided by the user
            - user_name: Customer's full name (must be real, not placeholder)
            - user_email: Customer's email address (must be valid format)
            - summary: Brief title describing the issue
            - description: Detailed explanation of the problem

            DO NOT call this tool with:
            - Missing information
            - Placeholder values (e.g., "John Doe", "user@example.com")
            - Made-up or assumed data

            If any information is missing, ask the user for it explicitly.
            """
            if not self.validate_ticket_data(user_name, user_email, summary, description):
                return "Ticket creation failed: All fields (name, email, summary, description) are required."

            return create_support_ticket(
                summary=summary.strip(),
                name=user_name.strip(),
                email=user_email.strip(),
                description=description.strip()
            )

        return submit_support_ticket

    def get_all_tools(self):
        return [
            self.create_search_tool(),
            self.create_ticket_tool()
        ]


def build_agent_tools(vector_store):
    factory = ToolFactory(vector_store)
    return factory.get_all_tools()
