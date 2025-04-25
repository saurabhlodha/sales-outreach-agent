import os
from src.utils import invoke_llm
from .base.linkedin_tools import scrape_linkedin
from .base.markdown_scraper_tool import scrape_website_to_markdown
from src.prompts import ANALYZE_VC_FIRM_WEB

# Model to use
AI_MODEL = os.environ['AI_MODEL']

CREATE_COMPANY_PROFILE = """
### Role  
You are an Expert Company profile generator with a particular expertise for generating a company profile from their scraped LinkedIn & website pages. 

### Objective  
Your goal is to look through the scraped LinkedIn company profile & website and create a 300-word company profile summarizing its operations, value proposition, target audience, products/services, location, company size, year founded and any other relevant information that might be useful to use when meeting the inbound lead that works for this company .

### Context  
This profile provides context for engaging with a prospect who works at the company.  

### Instructions  
- If no data is available from LinkedIn *and* the website, output only: *"No company info available."*  
- Use the available data from one or both sources; do not assume or invent information.  
- Always include:  
  - Company description  
  - Value proposition  
  - Target audience  
  - Products/services  
  - Location, size, and year founded  
- Keep the tone neutral and factual; avoid hype or subjective language.  
- Limit the profile to 300 words.  
"""

def analyze_vc_firm(linkedin_url, website_url):
    """Analyze a VC firm by scraping and analyzing their LinkedIn profile and website."""
    # Scrape LinkedIn profile
    linkedin_content = scrape_linkedin(linkedin_url, True)
    linkedin_data = linkedin_content.get("data", {}) if linkedin_content else {}
    
    # Scrape website
    website_content = ""
    if website_url:
        website_content = scrape_website_to_markdown(website_url)
    
    # Combine content for analysis
    combined_content = f"LinkedIn Profile:\n{str(linkedin_data)}\n\nWebsite Content:\n{website_content}"
    
    # Analyze the combined content
    analysis_str = invoke_llm(
        system_prompt=ANALYZE_VC_FIRM_WEB,
        user_message=combined_content,
        model=AI_MODEL
    )
    
    try:
        # Parse the response as JSON
        import json
        analysis = json.loads(analysis_str)
        
        # Fill in basic info from LinkedIn if missing
        if not analysis.get("company_name") and linkedin_data.get("company_name"):
            analysis["company_name"] = linkedin_data["company_name"]
        if not analysis.get("description") and linkedin_data.get("description"):
            analysis["description"] = linkedin_data["description"]
        
        return analysis
    except json.JSONDecodeError:
        return {
            "company_name": linkedin_data.get("company_name", ""),
            "description": linkedin_data.get("description", ""),
            "investment_focus": [],
            "portfolio_companies": [],
            "investment_stages": [],
            "investment_size": "",
            "geographic_focus": [],
            "investment_thesis": "",
            "recent_exits": [],
            "industry": linkedin_data.get("industry", ""),
            "tech_stack": [],
            "value_add": [],
            "esg_impact": "",
            "key_partners": [],
            "investment_process": ""
        }

def generate_company_profile(company_linkedin_info, scraped_website):
    # Get company profile summary
    inputs = (
        f"# Scraped Website:\n {scraped_website}\n\n"
        f"# Company LinkedIn Information:\n{company_linkedin_info}"
    )
    profile_summary = invoke_llm(
        system_prompt=CREATE_COMPANY_PROFILE, 
        user_message=inputs,
        model=AI_MODEL
    )
    return profile_summary