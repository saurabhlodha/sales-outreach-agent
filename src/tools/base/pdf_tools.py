import json
import PyPDF2
from src.utils import invoke_llm
from .prompts import PITCH_DECK_ANALYSIS_PROMPT

def read_pdf_content(pdf_path):
    """Read content from a PDF file."""
    content = ""
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                content += page.extract_text() + "\n"
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return None
    return content

def analyze_pitch_deck(pdf_content):
    """Analyze pitch deck content to understand the company's offering."""
    try:
        analysis_str = invoke_llm(
            system_prompt=PITCH_DECK_ANALYSIS_PROMPT,
            user_message=pdf_content,
            model="gemini-1.5-pro"
        )
        # Parse the response as JSON
        analysis = json.loads(analysis_str)
        return analysis
    except json.JSONDecodeError as e:
        print(f"Error parsing LLM response as JSON: {e}")
        return {
            "company_name": "",
            "description": "",
            "products_services": [],
            "target_market": "",
            "value_proposition": "",
            "benefits": [],
            "industry": "",
            "sales_approach": ""
        }
