# Cold Email Generation Tool
This Python-based tool automates the generation of cold emails using Langchain, llama-3.1-70b-versatile, Chroma DB, and Streamlit.

## Architecture

The tool consists of the following components:
- **Streamlit**: User interface for job URL input.
- **Langchain**: Web scraping and email generation pipeline.
- **Llama 3.1**: NLP model for job data extraction.
- **Chroma DB**: Database for storing technical skills and links.



## Architecture Overview:
```bash
User Interface (Streamlit):

Purpose: Allows the user to input a job URL and submit the request.
Flow: User inputs a URL → Sends the request to Langchain for processing.
Langchain Pipeline:

WebBaseLoader: Scrapes the job URL content.
Custom Chains: Processes the scraped data using the Llama 3.1 70B model and creates JSON outputs (e.g., role, skills, qualifications).
Llama 3.1 70B Model:

Purpose: NLP model that extracts and processes job description data.
Flow: Receives the scraped content → Generates structured job posting data in JSON format.
Chroma DB:

Persistent Storage: Stores tech stack data from a CSV file, providing relevant links based on the job's technical skills.
Query System: Queries the stored tech stack data using the extracted skills from the job posting.
Cold Email Generator:

Langchain Chain: Uses job data and tech stack links to generate a cold email via a prompt template.
Flow: Receives the structured job description and link list → Generates a personalized cold email.
Data Flow:

From User to Streamlit: User inputs a job URL in the Streamlit UI.
Streamlit to Langchain Pipeline: URL is processed, and data is scraped and passed to Llama 3.1.
From Llama 3.1 to Chroma DB: The processed technical skills are used to query relevant links from Chroma DB.
Langchain to Cold Email Generator: Job description and tech stack links are used to generate the cold email.
Final Output: Cold email is displayed back to the user via Streamlit.
```


## Installation

1. Clone the repository:
```bash
  git clone https://github.com/sreejithrv86/cold_email_generation_tool.git
```
2) Install the required packages using below pip comment
```bash
  pip install -r requirements.txt
```
3) Create a new account in https://console.groq.com/login and inside API Keys section 
  create a new API KEY and update it in .env file after base64 encoding against the given environment variable[GROQ_API_KEY].

## Usage

1) Run the Streamlit app:
```bash
streamlit run app/main.py
```
2) Enter a job URL and submit to generate a cold email

## Features
- Web scraping of job postings.
- Automatic extraction of job-related data.
- Cold email generation based on extracted job data.
- Integration with Chroma DB for personalized skills recommendations.

## Contributing
Contributions are welcome! Please submit a pull request or open an issue to discuss potential changes.
