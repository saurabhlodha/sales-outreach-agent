import os
import requests
from src.utils import invoke_llm
from .search_tools import google_search
from colorama import Fore, Style

# Model to use
AI_MODEL = os.environ['AI_MODEL']

def extract_twitter_handle(lead_data_name, company_name):
    EXTRACT_TWITTER_URL_PROMPT = """
    **Role:**  
    You are an expert in extracting Twitter/X handles from Google search results.

    **Objective:**  
    Extract the Twitter/X handle from the search results URLs. A handle is the username that appears after "x.com/" or "twitter.com/" in the URL (e.g., from "x.com/elonmusk" extract "elonmusk").

    **Instructions:**  
    1. Look for URLs containing either "x.com/" or "twitter.com/"
    2. Extract ONLY the handle part (what comes after the slash)
    3. Remove any trailing slashes, question marks, or additional path segments
    4. Output ONLY the handle without @ symbol (e.g., "elonmusk", "narendramodi", "realDonaldTrump")
    5. If no valid handle found, output an empty string 
    6. Return only one handle name that is best matching to the lead name 
    """
    # Querring by company name does not always yield the correct results.
    # Removing company name for now
    query = f"Twitter {lead_data_name}"
    search_results = google_search(query)

    result = invoke_llm(
        system_prompt=EXTRACT_TWITTER_URL_PROMPT, 
        user_message=str(search_results),
        model=AI_MODEL
    )
    print(Fore.BLUE + f"Lead Twitter Handle Extracted: {result}" + Style.RESET_ALL)
    return result

def get_twitter_timeline(twitter_handle, is_company=False):
    """
    Scrapes Twitter profile data based on the provided Twitter URL.
    
    @param Twitter_url: The Twitter URL to scrape.
    @param is_company: Boolean indicating whether to scrape a company profile or a person profile.
    @return: The scraped Twitter profile data.
    """
    print(Fore.BLUE + f"Lead Twitter Handle: {twitter_handle}" + Style.RESET_ALL)
    url = "https://twitter-api45.p.rapidapi.com/timeline.php"

    querystring = {"screenname": twitter_handle}
    headers = {
      "x-rapidapi-key": os.getenv("RAPIDAPI_KEY"),
      "x-rapidapi-host": "twitter-api45.p.rapidapi.com"
    }

    try:
        response = requests.get(url, headers=headers, params=querystring)
        response.raise_for_status()
        
        try:
            data = response.json()
            if not data:
                print(f"No data returned for Twitter handle: {twitter_handle}")
                return ""
                
            twitter_data = f"""
            Twitter timeline: {data}
            """
            return twitter_data
            
        except requests.exceptions.JSONDecodeError as e:
            print(f"Failed to parse Twitter API response: {e}")
            print(f"Response content: {response.text}")
            return ""
            
    except requests.exceptions.RequestException as e:
        print(f"Request failed with error: {e}")
        if hasattr(e.response, 'status_code'):
            print(f"Status code: {e.response.status_code}")
        return ""
