import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from dotenv import load_dotenv

load_dotenv()

class Chain:
    def __init__(self):
        self.llm = ChatGroq(temperature=0, model_name="llama-3.3-70b-versatile")

    def extract_jobs(self, cleaned_text):
        prompt_extract = PromptTemplate.from_template(
            """
            ### SCRAPED TEXT FROM WEBSITE:
            {page_data}
            ### INSTRUCTION:
            The scraped text is from the career's page of a website.
            Your job is to extract the job postings and return them in JSON format containing the following keys: `role`, `experience`, `skills` and `description`.
            Only return the valid JSON.
            ### VALID JSON (NO PREAMBLE):
            """
        )
        chain_extract = prompt_extract | self.llm
        res = chain_extract.invoke(input={"page_data": cleaned_text})
        try:
            json_parser = JsonOutputParser()
            res = json_parser.parse(res.content)
        except OutputParserException:
            raise OutputParserException("Context too big. Unable to parse jobs.")
        return res if isinstance(res, list) else [res]

    def write_mail(self, job, links, sender_name="[Your Name]", company_name="[Your Company]", company_info="our software consulting firm"):
        prompt_email = PromptTemplate.from_template(
            """
            ### JOB DESCRIPTION:
            {job_description}

            ### INSTRUCTION:
            You are {sender_name}, a Business Development Executive at {company_name}. 
            {company_name} is {company_info}. 
            
            Your task is to write a professional cold email to the hiring manager regarding the job described above. 
            The email should:
            1. Describe how your company's expertise aligns perfectly with their needs.
            2. Highlight specific technical capabilities that match the job requirements.
            3. Include the following relevant portfolio links to demonstrate previous success in similar stacks: {link_list}
            
            Keep the tone professional, concise, and persuasive.
            Do not provide a preamble or subject line.
            ### EMAIL (NO PREAMBLE):
            """
        )
        chain_email = prompt_email | self.llm
        res = chain_email.invoke({
            "job_description": str(job), 
            "link_list": links,
            "sender_name": sender_name,
            "company_name": company_name,
            "company_info": company_info
        })
        return res.content

if __name__ == "__main__":
    print(os.getenv("GROQ_API_KEY"))