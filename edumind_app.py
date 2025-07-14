import streamlit as st
import fitz 
import requests
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_community.llms import Ollama
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain.chains import RetrievalQA
import tempfile
import os

def generate_with_ollama(prompt, model="phi3"):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": model, "prompt": prompt, "stream": False}
    )
    return response.json()["response"]

def load_prompt(filename):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return f"Error: {filename} not found."

lessonplan_template = load_prompt("prompt_lessonplan.txt")
worksheet_template = load_prompt("prompt_worksheet.txt")

st.title("Your AI Teaching Assistant")

st.markdown("""
Welcome to your helpful assistant that can make your life easier! 🎓  
This platform helps teachers generate engaging teaching materials using AI.

You can:
- **Enter a topic** to generate summaries and quiz questions.
- **Upload a PDF** (e.g., lesson plans, notes) to extract content and generate teaching aids.
- **Ask questions** from a passage using a fast local model.

Use the sidebar to navigate between:
- **Generate Teaching Material**
- **Ask a Question**
""")

st.sidebar.header("Navigation")
page = st.sidebar.radio("Go to", ["Generate Teaching Material", "Ask a Question"])

if page == "Generate Teaching Material":
    st.header("Generate Teaching Material")

    st.subheader("Option A: Start from Scratch")
    topic = st.text_input("Enter a topic (e.g., 'Adding Fractions'):")
    grade_level = st.text_input("Enter the grade level (e.g., '3rd Grade'):")

    lesson_type = st.radio("Select output type:", ["Lesson Plan", "Worksheet"])

    if st.button("Generate Content"):
        if topic.strip() and grade_level.strip():
            if lesson_type == "Lesson Plan":
                prompt = lessonplan_template.replace("<INSERT_TOPIC_HERE>", topic).replace("<INSERT_GRADE_LEVEL_HERE>", grade_level)
            else:
                prompt = worksheet_template.replace("<INSERT_TOPIC_HERE>", topic).replace("<INSERT_GRADE_LEVEL_HERE>", grade_level)

            with st.spinner("Generating content..."):
                response = generate_with_ollama(prompt)
                st.subheader("Generated Content")
                st.write(response)
        else:
            st.warning("Please enter both a topic and a grade level.")

    st.markdown("---")
    st.subheader("Option B: Upload Existing Material")

    uploaded_pdf = st.file_uploader("Upload a PDF file", type=["pdf"])
    if uploaded_pdf is not None:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(uploaded_pdf.read())
            tmp_path = tmp_file.name

        # Load and split PDF
        loader = PyMuPDFLoader(tmp_path)
        pages = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        chunks = text_splitter.split_documents(pages)
        full_text = "\n\n".join([chunk.page_content for chunk in chunks])

        st.subheader("Extracted Text")
        st.text_area("Review or edit the extracted content:", value=full_text, height=300)

        lesson_type_pdf = st.radio("Select output type for PDF:", ["Lesson Plan", "Worksheet"], key="pdf_radio")

        if st.button("Generate Content from PDF"):
            if full_text.strip():
                with st.spinner("Generating content..."):
                    llm = Ollama(model="phi3")

                    if lesson_type_pdf == "Lesson Plan":
                        prompt = f"Create a detailed lesson plan based on the following material:\n\n{full_text}"
                    else:
                        prompt = f"Generate 10 practice problems for students based on the following material:\n\n{full_text}"

                    response = llm.invoke(prompt)
                    st.subheader("Generated Output")
                    st.write(response)
            else:
                st.warning("Please enter or upload some content.")

        os.remove(tmp_path)
elif page == "Ask a Question":
    st.header("Ask a Question from a PDF")

    # Initialize session state for Q&A history
    if "qa_history" not in st.session_state:
        st.session_state.qa_history = []

    uploaded_pdf = st.file_uploader("Upload a PDF to ask questions from", type=["pdf"], key="qa_pdf")

    if uploaded_pdf is not None:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(uploaded_pdf.read())
            tmp_path = tmp_file.name

        # Load and split the PDF
        loader = PyMuPDFLoader(tmp_path)
        pages = loader.load()

        # Embed and store in vector DB
        embeddings = OllamaEmbeddings(model="nomic-embed-text")
        vectorstore = Chroma.from_documents(pages, embedding=embeddings)

        retriever = vectorstore.as_retriever()
        llm = Ollama(model="phi3")

        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            retriever=retriever,
            return_source_documents=True
        )

        question = st.text_input("Ask a question based on the uploaded PDF:")

        if question:
            with st.spinner("Thinking..."):
                result = qa_chain({"query": question})
                answer = result["result"]

                st.subheader("Answer")
                st.write(answer)

                # Save Q&A to session state
                st.session_state.qa_history.append((question, answer))

                with st.expander("Source Chunks"):
                    for doc in result["source_documents"]:
                        st.markdown(doc.page_content)

        # Display Q&A history and download option
        if st.session_state.qa_history:
            st.subheader("Q&A History")
            for i, (q, a) in enumerate(st.session_state.qa_history, 1):
                st.markdown(f"**Q{i}:** {q}")
                st.markdown(f"**A{i}:** {a}")

            qa_text = "\n\n".join([f"Q{i+1}: {q}\nA{i+1}: {a}" for i, (q, a) in enumerate(st.session_state.qa_history)])
            st.download_button(
                label="Download Q&A as .txt",
                data=qa_text,
                file_name="qa_session.txt",
                mime="text/plain"
            )

        os.remove(tmp_path)
