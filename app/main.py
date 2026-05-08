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
            
            if jobs:
                # To ensure we only generate a single email for the primary job found
                main_job = jobs[0] 
                
                # Extract skills and convert list to string for ChromaDB query
                skills = main_job.get('skills', [])
                if isinstance(skills, list):
                    skills_query = ", ".join(skills)
                else:
                    skills_query = skills

                # Query the portfolio for the most relevant links
                links = portfolio.query_links(skills_query)
                
                # Generate the email (Pass your own info here if desired)
                email = llm.write_mail(main_job, links)
                
                st.subheader("Generated Cold Email")
                st.code(email, language='markdown')
            else:
                st.warning("No job postings could be extracted from the provided URL.")
                
        except Exception as e:
            st.error(f"An Error Occurred: {e}")


if __name__ == "__main__":
    chain = Chain()
    portfolio = Portfolio()
    st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="📧")
    create_streamlit_app(chain, portfolio, clean_text)

