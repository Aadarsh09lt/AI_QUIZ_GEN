# AI_QUIZ_GEN
---
#active link:


#  AI Quiz Generator (PDF → MCQ Generator)

The **AI Quiz Generator** is an NLP-powered application that automatically generates high-quality **multiple-choice questions (MCQs)** from any uploaded PDF.
Built using **Python, Streamlit, NLTK, and PyMuPDF**, this tool extracts meaningful concepts, identifies key nouns, and forms MCQs with distractors — completely offline.

---

##  Features

###  **PDF Text Extraction**

* Uses **PyMuPDF (fitz)** to extract clean text from uploaded PDFs.
* Automatically removes unwanted characters, URLs, and noisy content.

###  **Smart Question Generation**

* Generates MCQs based on **noun extraction** and **POS tagging**.
* Ensures:

  * No dates, times, or generic words as answers.
  * Clean, meaningful fill-in-the-blank questions.
  * Intelligent distractors using noun pools.

###  **NLP-Powered Processing**

* NLTK tokenizers (sent_tokenize, word_tokenize)
* POS tagging using `averaged_perceptron_tagger_eng`
* Custom blacklist filtering to avoid meaningless MCQs.

###  **Interactive Streamlit UI**

* Upload PDF → Select number of questions → Get MCQs instantly.
* Clean UI with quiz cards, score display, and reset option.

###  **Results & Evaluation**

* Shows:

  * Correct answers
  * User's selected answers
  * Final score with highlights

---

##  Tech Stack

| Component     | Library                              |
| ------------- | ------------------------------------ |
| UI Framework  | Streamlit                            |
| NLP Toolkit   | NLTK                                 |
| PDF Extractor | PyMuPDF (fitz)                       |
| Language      | Python                               |
| Styling       | Custom CSS injected inside Streamlit |

---

##  Installation & Setup

### Clone the repository

```
git clone <your-repo-link>
cd ai-quiz-generator
```

###  Install dependencies

```
pip install streamlit pymupdf nltk
```

###  Run NLTK downloads (will auto-download if missing)

```
python -m nltk.downloader punkt punkt_tab averaged_perceptron_tagger_eng
```

###  Run the application

```
streamlit run quiz_app.py
```

---

##  How It Works (Pipeline)

### **1. PDF Input**

User uploads a `.pdf` file.

### **2. Text Cleaning**

* URLs removed
* Trailing symbols removed
* Extra whitespace removed

### **3. NLP Parsing**

* Text → Sentences → Words
* POS tagging performed
* Nouns extracted and filtered

### **4. MCQ Generation**

* One key noun chosen as the answer
* The sentence is converted into a fill-in-the-blank
* Distractors chosen from global noun pool

### **5. Quiz Interface**

* User attempts each question
* Results shown instantly
* Score calculated
* Incorrect and unanswered questions highlighted

---

##  Project Structure

```
 AI-Quiz-Generator
│
├── quiz_app.py        # Main Streamlit application
├── README.md          # Project documentation
│
└── nltk_data/         # Auto-created NLTK storage (downloads here)
```

---

##  Future Improvements

*  Add option to export MCQs to PDF / Word
*  Add support for images/diagrams in PDFs
*  Improve distractor selection using word embeddings
*  Add difficulty-level selectors (easy/medium/hard)
*  Add online version hosted on Streamlit Cloud

---

##  Team Credits

**Developed by:**

* Gaurav Yadav
* Aadarsh Tripathi
* Mayank Kaushik
* * Satyam Srivastava
  *(1CSE17)*

---

## 💬 Feedback & Contributions

We welcome suggestions!
Fork the repo, submit PRs, or reach out for collaboration.

---

##  If you like this project

Don’t forget to **star the repository** and share it with others!

---

###  Enjoy generating smart, concept-based quizzes automatically!
