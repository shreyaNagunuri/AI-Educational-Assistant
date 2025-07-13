import streamlit as st
import fitz  # PyMuPDF
import requests
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM, AutoModelForSeq2SeqLM
from huggingface_hub import configure_http_backend

# Fix the arrow symbol in the function definition
def backend_factory() -> requests.Session:
    session = requests.Session()
    session.verify = False 
    return session

configure_http_backend(backend_factory=backend_factory)

deepseek_tokenizer = AutoTokenizer.from_pretrained("google-t5/t5-large")
deepseek_model = AutoModelForSeq2SeqLM.from_pretrained("google-t5/t5-large")


# ✅ Create a unified pipeline for instruction-based generation
deepseek_pipeline = pipeline(
    "text2text-generation",
    model=deepseek_model,
    tokenizer=deepseek_tokenizer,
    device=-1
)

# Utility function to load prompt templates
def load_prompt(filename):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return f"Error: {filename} not found."

# Load prompt templates
lessonplan_template = load_prompt("prompt_lessonplan.txt")
worksheet_template = load_prompt("prompt_worksheet.txt")

st.title("Your AI Teaching Assistant")

st.markdown("""
Welcome to your helpful assistant that can make your life easier! 🎓  
This platform helps teachers generate engaging teaching materials using AI.

You can:
- ✍️ **Enter a topic** to generate summaries and quiz questions.
- 📂 **Upload a PDF** (e.g., lesson plans, notes) to extract content and generate teaching aids.

Use the sidebar to navigate between:
- **Generate Teaching Material**: Create summaries and quizzes from text or PDFs.
- **Evaluate Student Answers**: Analyze student responses and generate follow-up questions.
""")

st.sidebar.header("Navigation")
page = st.sidebar.radio("Go to", ["Generate Teaching Material", "Evaluate Student Answers"])

if page == "Generate Teaching Material":
    st.header("🧠 Generate Teaching Material")

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
                response = deepseek_pipeline(prompt)[0]['generated_text']
                st.subheader("📄 Generated Content")
                st.write(response)
        else:
            st.warning("Please enter both a topic and a grade level.")

    st.markdown("---")
    st.subheader("Option B: Upload Existing Material")

    uploaded_pdf = st.file_uploader("Upload a PDF file", type=["pdf"])
    extracted_text = ""

    if uploaded_pdf is not None:
        with fitz.open(stream=uploaded_pdf.read(), filetype="pdf") as doc:
            for page in doc:
                extracted_text += page.get_text()

        st.subheader("📄 Extracted Text")
        pdf_text = st.text_area("Review or edit the extracted content:", value=extracted_text, height=300)

        lesson_type_pdf = st.radio("Select output type for PDF:", ["Lesson Plan", "Worksheet"], key="pdf_radio")

        if st.button("Generate Content from PDF"):
            if pdf_text.strip():
                with st.spinner("Generating content..."):
                    if lesson_type_pdf == "Lesson Plan":
                        prompt = f"Instruction: Summarize the following content and generate quiz questions suitable for students.\n\nContent:\n{pdf_text}"
                    else:
                        prompt = f"Instruction: Generate 10 practice problems suitable for students based on the following material:\n\n{pdf_text}"

                    response = deepseek_pipeline(prompt)[0]['generated_text']
                    st.subheader("📄 Generated Output")
                    st.write(response)
            else:
                st.warning("Please enter or upload some content.")

elif page == "Evaluate Student Answers":
    st.header("📊 Evaluate Student Answers")
    uploaded_file = st.file_uploader("Upload a text file with student answers", type=["txt"])

    if uploaded_file is not None:
        student_text = uploaded_file.read().decode("utf-8")
        st.text_area("Student Answers", student_text, height=200)

        if st.button("Analyze and Generate Follow-up Questions"):
            with st.spinner("Analyzing answers..."):
                sentences = student_text.split(".")
                incorrect = [s.strip() for s in sentences if len(s.strip()) > 10 and "not" in s.lower()]

                if incorrect:
                    st.subheader("❌ Detected Issues")
                    for i, s in enumerate(incorrect, 1):
                        st.write(f"{i}. {s}")

                    st.subheader("🔁 Follow-up Questions")
                    for i, s in enumerate(incorrect, 1):
                        prompt = f"Instruction: Based on the following incorrect student answer, generate a follow-up question to guide them:\n\n{s}"
                        followup = deepseek_pipeline(prompt)[0]['generated_text']
                        st.write(f"{i}. {followup}")
                else:
                    st.success("No major issues detected in the student answers.")