import streamlit as st
from dotenv import load_dotenv
import os
from chains import Chain
from portfolio import Portfolio
from util import clean_text, refine_link
from langchain_community.document_loaders import WebBaseLoader
from logging_config import logger
# Load environment variables
load_dotenv()
url = os.getenv('URL')
tskills= os.getenv('TECH_SKILLS')
lang= os.getenv('LANGUAGE')
def create_streamlit_app(llm, portfolio, clean_text, refine_link):
    # Initialize Streamlit app
    st.title("📧 Cold Mail Generator")
    # Input field for URL
    url_input = st.text_input("Enter a URL:", value=url)
    # Submit button
    submit_button = st.button("Submit")

    if submit_button:
        # Load content from website
        loader = WebBaseLoader([url_input])
        page_data = clean_text(loader.load().pop().page_content)

        # Load techstack links and initialize ChromaDB
        portfolio.populate_chroma_collection()

        # Extract job posting details in JSON format
        json_res = llm.extract_job_posting(page_data)

        # Query ChromaDB with the technical skills
        result = portfolio.query_chroma_collection(json_res[tskills])

        # Refine the results based on the technical skills
        refined_links = refine_link(result, json_res[tskills])

        # Generate cold email based on the job description and portfolio links
        res_email = llm.generate_email(json_res, refined_links)

        # Display the email in Streamlit
        st.code(res_email, language=lang)



if __name__ == "__main__":
    logger.info("initialize the chain and portfolio class")
    chain = Chain()
    portfolio = Portfolio()
    logger.info("set page config for streamlit")
    st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="📧")
    logger.info("call create streamlit method")
    create_streamlit_app(chain, portfolio, clean_text, refine_link)
