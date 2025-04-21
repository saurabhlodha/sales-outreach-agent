import PyPDF2
from src.utils import invoke_llm

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
    PITCH_DECK_ANALYSIS_PROMPT = """
    You are an expert in analyzing company pitch decks. Review the provided pitch deck content and extract key information about the company.
    
    # Task
    Extract and summarize the following information in a structured format:
    
    1. Company Name and Description
    2. Core Products/Services
    3. Target Market/Customers
    4. Unique Value Proposition
    5. Key Benefits/Features
    6. Industry/Domain
    7. Sales Approach
    
    # Output Format
    Return the analysis as a JSON string with the following structure:
    {
        "company_name": "",
        "description": "",
        "products_services": [],
        "target_market": "",
        "value_proposition": "",
        "benefits": [],
        "industry": "",
        "sales_approach": ""
    }
    """
    
    analysis = invoke_llm(
        system_prompt=PITCH_DECK_ANALYSIS_PROMPT,
        user_message=pdf_content,
        model="gemini-1.5-pro"
    )
    return analysis
