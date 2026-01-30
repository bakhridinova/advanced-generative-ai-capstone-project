# Toyota Assistant - RAG Customer Support System

## Images

### Landing page

![Landing page.png](screenshots/Landing%20page.png)

### Cite document and page

![Cite document and page.png](screenshots/Cite%20document%20and%20page.png)

### Company information

![Company information.png](screenshots/Company%20information.png)

### Conversation history

![Conversation history.png](screenshots/Conversation%20history.png)

### Customer support ticket 

![Answer not found.png](screenshots/Answer%20not%20found.png)

![Customer support ticket.png](screenshots/Customer%20support%20ticket.png) 

https://github.com/bakhridinova/advanced-generative-ai-capstone-project/issues/2

![Customer support ticket console.png](screenshots/Customer%20support%20ticket%20console.png)

## Setup

1. **Clone the repository**
```bash
cd rag
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure environment variables**

Create a `.env` file in the `rag` folder:
```env
OPENAI_API_KEY=your_openai_api_key_here
GITHUB_TOKEN=your_github_token_here
GITHUB_REPO=your_repo_name
GITHUB_USER=your_github_username
LLM_MODEL=gpt-4o-mini
```

4. **Add documents**

Place your PDF and TXT files in the `documents/` folder.

5. **Run the application**
```bash
streamlit run app.py
```

The app will be available at `http://localhost:8501`

## 📖 Usage

### Asking Questions
Simply type your question in the chat input. The AI will:
1. Search the knowledge base (manuals + FAQs)
2. Return relevant information with source citations
3. Example: `(Source: 2018 Toyota Hilux Owner's Manual.pdf, page 325)`

### Creating Support Tickets
If the AI can't find an answer:
1. It will ask: "Would you like to open a support ticket?"
2. Say "yes" to proceed
3. Provide: Name → Email → Summary → Description
4. Ticket created in GitHub Issues with tracking link
