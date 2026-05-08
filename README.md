# 📧 AI-Powered Cold Email Generator

An automated tool that leverages **Generative AI** and **Vector Databases** to transform job postings into highly personalized cold emails. By scraping job descriptions and matching them with a relevant project portfolio, this tool ensures every pitch is backed by context-specific evidence.

---

## 🚀 Features
- **Automated Web Scraping:** Extracts raw content from any job board URL.
- **LLM-Based Extraction:** Uses **Llama-3 (Groq)** to parse unstructured text into structured JSON (Role, Skills, Experience).
- **Semantic Portfolio Matching:** Utilizes **ChromaDB** and **RAG (Retrieval-Augmented Generation)** to find the best portfolio links for specific job requirements.
- **Dynamic Email Synthesis:** Generates professional, persuasive cold emails tailored to the identified tech stack.
- **Streamlit Interface:** A clean, user-friendly dashboard for quick email generation.

---

## 🛠️ Tech Stack
- **Orchestration:** LangChain
- **LLM:** Groq (Llama-3.3-70b-versatile)
- **Vector Database:** ChromaDB
- **Frontend:** Streamlit
- **Data Handling:** Pandas, BeautifulSoup

---

## 🏗️ Architecture Flow



1. **Input:** User provides a job portal URL.
2. **Scrape:** `WebBaseLoader` pulls the raw HTML and cleans the text.
3. **Parse:** The LLM extracts a list of required technical skills.
4. **Query:** Those skills are converted into vectors to search a local portfolio database.
5. **Generate:** The LLM writes the final email using the job context and the retrieved links.

---

## 🔧 Installation & Setup

1. **Clone the Repository:**
2. **Install Dependencies:**
    pip install -r requirements.txt
