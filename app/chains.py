from dotenv import load_dotenv
from langchain_core.exceptions import OutputParserException
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_groq import ChatGroq
import os
from logging_config import logger

# Load environment variables
load_dotenv()
key = os.getenv('GROQ_API_KEY')
model = os.getenv('MODEL')
user_name = os.getenv('USERNAME')


class Chain:
    def __init__(self):
        # initialize llm model in the in Groq
        self.llm = ChatGroq(
            model_name=model,
            temperature=0,
            groq_api_key=key
        )

    def extract_job_posting(self, page_data):
        # Define the prompt template to extract data from the webpage content
        prompt_extract = PromptTemplate.from_template(
            """
            ### SCRAPED TEXT FROM WEBSITE:
            {page_data}
            ### INSTRUCTION:
            The scraped text is from the career's page of a website.
            Your job is to extract the job posting and return them in JSON format containing the following keys:
            'role', 'experience', 'qualifications', 'technical skills', 'behavioural skills', 'description'.
            Only return the valid JSON.
            ### VALID JSON (NO PREAMBLE):
            """
        )
        chain_extract = prompt_extract | self.llm
        res = chain_extract.invoke(input={"page_data": page_data})
        try:
            json_parser = JsonOutputParser()
            json_res = json_parser.parse(res.content)
            logger.info("extracted the contents and created JSON.")
        except OutputParserException:
            logger.error("Context too big. Unable to parse jobs.")
            raise OutputParserException("Context too big. Unable to parse jobs.")
        return json_res

    def generate_email(self, json_res, refined_links):
        # Write cold email with a prompt template
        prompt_email = PromptTemplate.from_template(
            """
            ### JOB DESCRIPTION:
            {job_description}
    
            ### INSTRUCTION:
            You are {by_user}, a business development executive at AIQuest. AIQuest is an AI & Software Consulting company dedicated to facilitating
            the seamless integration of business processes through automated tools. 
            Your job is to write a cold email to the client regarding the job mentioned above describing the capability of AIQuest 
            in fulfilling their needs.
            Also add the most relevant ones from the following links to showcase AIQuest's portfolio: {link_list}
            Remember you are {by_user}, BDE at AIQuest. 
            Do not provide a preamble.
            ### EMAIL (NO PREAMBLE):
            """
        )
        chain_email = prompt_email | self.llm
        res_email = chain_email.invoke({"job_description": str(json_res['description']), "link_list": refined_links, "by_user": user_name})
        logger.info("returnn email content is generated.")
        return res_email.content


if __name__ == "__main__":
    print(os.getenv("GROQ_API_KEY"))
