## Your AI Teaching Assistant

This app helps teachers generate lesson plans, worksheets, and answer questions from uploaded PDFs using local AI models via Ollama. It runs entirely offline once models are downloaded.

- Generate lesson plans and worksheets from a topic or PDF
- Ask questions based on uploaded documents (RAG-style Q&A)
- Save and download Q&A sessions
- Fully local and private — no internet required after setup

---

## Requirements
- Python 3.9+
- Ollama installed and running
- The following models pulled via Ollama:
  ```bash
  ollama pull phi3
  ollama pull nomic-embed-text
  ```

## Installation
- Clone the repo
  ```bash
  git clone https://github.com/your-username/ai-teaching-assistant.git
  cd ai-teaching-assistant
  ```
- Create and activate a virtual environment:
  ```bash
  python -m venv edumind-env
  source edumind-env/bin/activate  # On Windows: edumind-env\Scripts\activate
  ```
- Install dependencies:
  ```bash
   pip install -r requirements.txt
  ```
- Run the app:
   ```bash
    streamlit run edumind_app.py
  ```
 
## People
Shreya Nagunuri  
snagunur@qti.qualcomm.com  
Anya Chernova  
achernov@qti.qualcomm.com  
