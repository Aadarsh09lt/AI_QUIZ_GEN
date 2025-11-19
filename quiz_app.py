import streamlit as st
import fitz  # PyMuPDF
import nltk
import os
import random
import shutil
import zipfile
import re  # Cleaning text

# ---------------------- COSMIC THEME CSS -------------------------
cosmic_css = """
<style>

html, body {
    background: radial-gradient(circle at top, #0a0f2c, #000000) fixed !important;
    color: #E0E7FF !important;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #080818, #020012) !important;
    border-right: 2px solid #6d28d9 !important;
    box-shadow: 0px 0px 15px #6d28d9;
}

/* Main container */
.block-container {
    background: rgba(20, 10, 40, 0.25) !important;
    border: 1px solid #6d28d9;
    border-radius: 15px;
    padding: 25px;
    box-shadow: 0px 0px 20px rgba(120, 70, 255, 0.4);
}

/* Titles */
h1 {
    color: #c084fc !important;
    text-shadow: 0 0 15px #a855f7;
}
h2, h3, h4 {
    color: #d8b4fe !important;
    text-shadow: 0 0 10px #9333ea;
}

/* Radio buttons */
.stRadio > div {
    background: rgba(60, 40, 90, 0.3) !important;
    padding: 12px 15px;
    border-radius: 10px;
    border: 1px solid #7c3aed;
    box-shadow: 0 0 12px rgba(150, 100, 255, 0.4);
    color: white !important;
}

/* Buttons */
button[kind="primary"] {
    background: linear-gradient(90deg, #7c3aed, #9333ea) !important;
    border: none !important;
    color: white !important;
    border-radius: 10px !important;
    box-shadow: 0 0 20px #9333ea;
}
button[kind="primary"]:hover {
    transform: scale(1.05);
    box-shadow: 0 0 30px #a855f7;
}

/* Sidebar button */
section[data-testid="stSidebar"] button {
    background: linear-gradient(90deg, #9333ea, #c026d3) !important;
    color: white !important;
    border-radius: 10px !important;
    box-shadow: 0px 0px 10px #c026d3;
}

/* HR Line */
hr {
    border: 0;
    height: 1px;
    background: linear-gradient(90deg, #9333ea, #ec4899);
}

/* Footer */
footer, .stCaption {
    color: #e9d5ff !important;
}
</style>
"""
st.markdown(cosmic_css, unsafe_allow_html=True)
# -----------------------------------------------------------------


# --- 1. Setup NLTK Resources ---
nltk_data_dir = os.path.join(os.path.expanduser("~"), "nltk_data")
if not os.path.exists(nltk_data_dir):
    os.makedirs(nltk_data_dir)
nltk.data.path.append(nltk_data_dir)

required_packages = ["punkt", "punkt_tab", "averaged_perceptron_tagger_eng"]

for pkg in required_packages:
    try:
        if "averaged_perceptron_tagger" in pkg:
            nltk.data.find(f"taggers/{pkg}")
        else:
            nltk.data.find(f"tokenizers/{pkg}")
    except (LookupError, zipfile.BadZipFile):
        print(f"Downloading {pkg}...")
        try: 
             shutil.rmtree(os.path.join(nltk_data_dir, "taggers", pkg), ignore_errors=True)
        except: pass
        nltk.download(pkg, download_dir=nltk_data_dir)

from nltk.tokenize import sent_tokenize, word_tokenize

# --- 2. Helper Functions ---

DATE_BLACKLIST = {
    "january","february","march","april","may","june",
    "july","august","september","october","november","december",
    "monday","tuesday","wednesday","thursday","friday","saturday","sunday",
    "year","years","month","months","day","days","today","tomorrow",
    "hour","hours","minute","minutes","second","seconds","time","date",
    "https","http","www","com","page","chapter","section"
}

def preprocess_text(text):
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'\S+\.com\S*', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text

def extract_text_from_pdf(file):
    text = ""
    with fitz.open(stream=file.read(), filetype="pdf") as pdf:
        for page in pdf:
            text += page.get_text("text") + "\n"
    return preprocess_text(text)

def get_nouns(text):
    words = word_tokenize(text)
    tags = nltk.pos_tag(words)

    nouns = []
    for word, tag in tags:
        if tag in ('NN','NNS','NNP','NNPS') and word.isalpha() and len(word) > 3:
            if word.lower() not in DATE_BLACKLIST:
                nouns.append(word)

    return list(set(nouns))

def generate_mcqs(text, num_questions=5):
    sentences = sent_tokenize(text)
    sentences = [s.strip() for s in sentences if len(s.split()) > 6]

    if not sentences:
        return []

    noun_pool = get_nouns(text)
    if len(noun_pool) < 10:
        return []

    selected_sentences = random.sample(sentences, min(num_questions, len(sentences)))
    questions = []

    for s in selected_sentences:
        s_words = word_tokenize(s)
        s_tags = nltk.pos_tag(s_words)

        valid_keywords = [
            w for w, t in s_tags
            if t in ('NN','NNS','NNP','NNPS')
            and w.isalpha()
            and len(w) > 3
            and w.lower() not in DATE_BLACKLIST
        ]

        if not valid_keywords:
            continue

        answer = random.choice(valid_keywords)
        question_text = s.replace(answer, "______", 1)

        distractors = []
        attempts = 0
        while len(distractors) < 3 and attempts < 50:
            choice = random.choice(noun_pool)
            if choice != answer and choice not in distractors:
                distractors.append(choice)
            attempts += 1

        if len(distractors) < 3:
            continue

        options = distractors + [answer]
        random.shuffle(options)
        questions.append((question_text, options, answer))

    return questions

# --- 3. UI ---

st.set_page_config(page_title="AI Quiz Generator", layout="wide")
st.title("AI Quiz Generator")
st.markdown("Upload a PDF to generate **concept-based** multiple-choice questions.")

with st.sidebar:
    st.header("Configuration")
    uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])
    num_q = st.slider("Number of Questions", 1, 15, 5)

    if st.button("Reset App"):
        st.session_state.clear()
        st.rerun()

if "quiz_data" not in st.session_state:
    st.session_state["quiz_data"] = []
if "user_answers" not in st.session_state:
    st.session_state["user_answers"] = {}
if "score_visible" not in st.session_state:
    st.session_state["score_visible"] = False

if uploaded_file is not None:
    if not st.session_state["quiz_data"]:
        if st.button("Generate Quiz"):
            with st.spinner("Processing PDF..."):
                text = extract_text_from_pdf(uploaded_file)
                generated_quiz = generate_mcqs(text, num_q)

                if generated_quiz:
                    st.session_state["quiz_data"] = generated_quiz
                    st.session_state["score_visible"] = False
                    st.rerun()
                else:
                    st.error("Could not generate questions. Text might be too short.")

if st.session_state["quiz_data"]:
    st.subheader("Quiz")

    with st.form(key='quiz_form'):
        for i, (q, options, ans) in enumerate(st.session_state["quiz_data"]):
            st.markdown(f"**{i+1}. {q}**")

            st.radio(
                label="Select answer:",
                options=options,
                key=f"question_{i}",
                label_visibility="collapsed",
                index=None
            )
            st.markdown("---")

        submit_button = st.form_submit_button("Submit Quiz")

    if submit_button:
        st.session_state["score_visible"] = True
        score = 0
        total = len(st.session_state["quiz_data"])

        st.divider()
        st.header("Results")

        for i, (q, options, ans) in enumerate(st.session_state["quiz_data"]):
            user_choice = st.session_state.get(f"question_{i}")

            if user_choice == ans:
                score += 1
                st.success(f"Q{i+1}: Correct! ({ans})")
            else:
                if user_choice is None:
                    st.warning(f"Q{i+1}: You didn't answer this one. Correct answer: {ans}")
                else:
                    st.error(f"Q{i+1}: Incorrect. You chose '{user_choice}', but answer was '{ans}'.")

        st.info(f"**Final Score: {score} / {total}**")

# Footer
st.markdown("---")
st.caption("Project by: Gaurav Yadav, Mayank Kaushik, Aadarsh Tripathi, Satyam Srivastava [1CSE17]")
