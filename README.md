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


MIT License

Copyright (c) [year] [fullname]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
