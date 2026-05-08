import streamlit as st
from langchain_community.document_loaders import WebBaseLoader

from chains import Chain
from portfolio import Portfolio
from utils import clean_text


def create_streamlit_app(llm, portfolio, clean_text):
    st.title("📧 Cold Mail Generator")
    url_input = st.text_input("Enter a URL:", value="https://jobs.nike.com/job/R-33460")
    submit_button = st.button("Submit")

    if submit_button:
        try:
            loader = WebBaseLoader([url_input])
            data = clean_text(loader.load().pop().page_content)
            portfolio.load_portfolio()
            jobs = llm.extract_jobs(data)
            
            for job in jobs:
                # 1. Get skills and provide a default empty list if it's None
                skills = job.get('skills', [])
                
                # 2. Ensure skills is a string and not None/Empty
                if isinstance(skills, list):
                    skills_query = ", ".join(skills)
                else:
                    skills_query = str(skills) if skills else ""

                # 3. Only query if we actually have skills to look for
                if skills_query.strip():
                    links = portfolio.query_links(skills_query)
                else:
                    links = [] # Fallback if no skills were found
                
                email = llm.write_mail(job, links)
                st.code(email, language='markdown')
                
        except Exception as e:
            st.error(f"An Error Occurred: {e}")


if __name__ == "__main__":
    chain = Chain()
    portfolio = Portfolio()
    st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="📧")
    create_streamlit_app(chain, portfolio, clean_text)

