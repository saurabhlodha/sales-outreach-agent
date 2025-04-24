import os
import json
from colorama import Fore, Style
from .tools.base.markdown_scraper_tool import scrape_website_to_markdown
from .tools.base.search_tools import get_recent_news
from .tools.base.gmail_tools import GmailTools
from .tools.google_docs_tools import GoogleDocsManager
from .tools.lead_research import research_lead_on_linkedin
from .tools.base.twitter_tools import extract_twitter_handle, get_twitter_timeline
from .tools.company_research import research_lead_company, generate_company_profile
from .tools.youtube_tools import get_youtube_stats
from .tools.rag_tool import fetch_similar_case_study
from .prompts import *
from .state import LeadData, CompanyData, Report, GraphInputState, GraphState
from .structured_outputs import WebsiteData, EmailResponse
from .utils import invoke_llm, get_report, get_current_date, save_reports_locally
from src.tools.base.pdf_tools import read_pdf_content, analyze_pitch_deck

# Enable or disable sending emails directly using GMAIL
# Should be confident about the quality of the email
SEND_EMAIL_DIRECTLY = os.environ['SEND_EMAIL_DIRECTLY', False]
# Enable or disable saving emails to Google Docs
# By defauly all reports are save locally in `reports` folder
# Set to True if you want to save reports to Google Docs
SAVE_TO_GOOGLE_DOCS = False

# Adding test email address to temporarily skips emailing VCs
TEST_EMAIL = os.environ['TEST_EMAIL']

# Model to use
AI_MODEL = os.environ['AI_MODEL']

class OutReachAutomationNodes:
    def __init__(self, loader):
        self.lead_loader = loader
        self.docs_manager = GoogleDocsManager()
        self.drive_folder_name = ""

    def get_new_leads(self, state: GraphInputState):
        print(Fore.YELLOW + "----- Fetching new leads -----\n" + Style.RESET_ALL)
        
        # Fetch new leads using the provided loader
        raw_leads = self.lead_loader.fetch_records()
        
        # Structure the leads
        leads = [
            LeadData(
                id=lead["id"],
                name=f'{lead.get("First Name", "")} {lead.get("Last Name", "")}',
                email=lead.get("Email", ""),
                phone=lead.get("Phone", ""),
                address=lead.get("Address", ""),
                vc_company_data=CompanyData(name=lead.get("Company Name", "")),
                social_media_links=SocialMediaLinks(linkedin=lead.get("Linkedin URL", "")),
                profile="" # will be constructed
            )
            for lead in raw_leads
        ]
        
        print(Fore.YELLOW + f"----- Fetched {len(leads)} leads -----\n" + Style.RESET_ALL)
        return {"leads_data": leads, "number_leads": len(leads)}
    
    @staticmethod
    def check_for_remaining_leads(state: GraphState):
        """Checks for remaining leads and updates lead_data in the state."""
        print(Fore.YELLOW + "----- Checking for remaining leads -----\n" + Style.RESET_ALL)
        
        current_lead = None
        if state["leads_data"]:
            current_lead = state["leads_data"].pop()
        return {"current_lead": current_lead}

    @staticmethod
    def check_if_there_more_leads(state: GraphState):
        # Number of leads remaining
        num_leads = state["number_leads"]
        if num_leads > 0:
            print(Fore.YELLOW + f"----- Found {num_leads} more leads -----\n" + Style.RESET_ALL)
            return "Found leads"
        else:
            print(Fore.GREEN + "----- Finished, No more leads -----\n" + Style.RESET_ALL)
            return "No more leads"

    def generate_prompt_from_pitch_deck(self, state: GraphState):
        print(Fore.YELLOW + "----- Generating prompt from pitch deck -----\n" + Style.RESET_ALL)

        # Read and analyze the pitch deck
        pdf_path = os.getenv("PITCH_DECK_PATH", "data/decks/target.pdf")
        pdf_content = read_pdf_content(pdf_path)
        if not pdf_content:
            print(Fore.RED + f"Error: Could not read pitch deck at {pdf_path}" + Style.RESET_ALL)
            return "No more leads"
            
        # Analyze pitch deck content
        company_analysis = analyze_pitch_deck(pdf_content)

        # Update company data in state
        our_company_data = CompanyData()
        our_company_data.description = company_analysis.get("description", "")
        our_company_data.products_services = company_analysis.get("products_services", [])
        our_company_data.target_market = company_analysis.get("target_market", "")
        our_company_data.value_proposition = company_analysis.get("value_proposition", "")
        our_company_data.benefits = company_analysis.get("benefits", [])
        our_company_data.industry = company_analysis.get("industry", "")
        our_company_data.sales_approach = company_analysis.get("sales_approach", "")
        our_company_data.name = company_analysis.get("company_name", "")
        
        # Store our company data in state
        state["our_company_data"] = our_company_data
        
        print(Fore.GREEN + f"Successfully analyzed pitch deck for {our_company_data.name}" + Style.RESET_ALL)
        return { "our_company_data": our_company_data }

    def fetch_linkedin_profile_data(self, state: GraphState):
        print(Fore.YELLOW + "----- Searching Lead data on LinkedIn -----\n" + Style.RESET_ALL)
        # print(state)
        lead_data = state["current_lead"]
        vc_company_data = lead_data.vc_company_data
        
        # Scrape lead linkedin profile
        (
            lead_profile, 
            company_name, 
            company_website,
            company_linkedin_url
        ) = research_lead_on_linkedin(lead_data.name, lead_data.email, lead_data.social_media_links.linkedin)
        lead_data.profile = lead_profile

        # Research company on linkedin
        company_profile = research_lead_company(company_linkedin_url)
        
        # Update company name from LinkedIn data
        vc_company_data.name = company_name
        vc_company_data.website = company_website
        vc_company_data.profile = str(company_profile)
        lead_data.vc_company_data = vc_company_data

        # Set the drive folder name
        self.drive_folder_name = f"{lead_data.name}_{vc_company_data.name}"

        return {
            "current_lead": lead_data,
            "reports": []
        }

    def analyze_lead_social_profile(self, state: GraphState):
        print(Fore.YELLOW + "----- Analyzing Twitter profile -----\n" + Style.RESET_ALL)
        lead_data = state.get("current_lead")
        vc_company_data = state["current_lead"].vc_company_data
        
        # Extract twitter handle
        twitter_handle = extract_twitter_handle(lead_data.name, vc_company_data.name)
        if not twitter_handle:
            print(f"Twitter handle not found for {lead_data.name}")
            return {
                "current_lead": lead_data,
                "vc_company_data": vc_company_data
            }

        # Scrape Twitter profile
        twitter_profile = get_twitter_timeline(twitter_handle)
        prompt = VC_TWITTER_ANALYSIS_PROMPT.format(lead_name=lead_data.name)
        twitter_insight = invoke_llm(
            system_prompt=prompt, 
            user_message=twitter_profile,
            model=AI_MODEL
        )
        vc_twitter_analysis_report = Report(
            title="VC Twitter Analysis Report",
            content=twitter_insight,
            is_markdown=True
        )

        return {
            "current_lead": lead_data,
            # vc_company_data is now stored in current_lead
            "reports": [vc_twitter_analysis_report]
        }
    
    def review_company_website(self, state: GraphState):
        print(Fore.YELLOW + "----- Scraping company website -----\n" + Style.RESET_ALL)
        lead_data = state.get("current_lead")
        vc_company_data = lead_data.vc_company_data

        company_website = vc_company_data.website
        if company_website:
            # Scrape company website
            content = scrape_website_to_markdown(company_website)
            website_info = invoke_llm(
                system_prompt=WEBSITE_ANALYSIS_PROMPT.format(main_url=company_website), 
                user_message=content,
                model=AI_MODEL,
                response_format=WebsiteData
            )

            # Extract all relevant links if they exist
            if website_info.blog_url:
                vc_company_data.social_media_links.blog = website_info.blog_url
            if website_info.facebook:
                vc_company_data.social_media_links.facebook = website_info.facebook
            if website_info.twitter:
                vc_company_data.social_media_links.twitter = website_info.twitter
            if website_info.youtube:
                vc_company_data.social_media_links.youtube = website_info.youtube
            if website_info.linkedin:
                vc_company_data.social_media_links.linkedin = website_info.linkedin

            # Update company profile with website data
            vc_company_data.profile = generate_company_profile(vc_company_data.profile, website_info.summary)
                 
        inputs = f"""
        # **Lead Profile:**

        {lead_data.profile}

        # **Company Information:**

        {vc_company_data.profile}
        """
        
        # Generate general lead search report
        general_lead_search_report = invoke_llm(
            system_prompt=LEAD_SEARCH_REPORT_PROMPT, 
            user_message=inputs,
            model=AI_MODEL
        )
        
        lead_search_report = Report(
            title="General Lead Research Report",
            content=general_lead_search_report,
            is_markdown=True
        )

        lead_data.vc_company_data = vc_company_data
        return {
            "current_lead": lead_data,
            "reports": [lead_search_report]
        }
    
    def analyze_social_media_content(self, state: GraphState):
        print(Fore.YELLOW + "----- Analyzing company social media accounts -----\n" + Style.RESET_ALL)
        
        # Load states
        vc_company_data = state["current_lead"].vc_company_data
        
        # Initialize report variables with empty content
        youtube_analysis_report = Report(
            title="Youtube Analysis Report",
            content="No YouTube channel found or analysis not available.",
            is_markdown=True
        )
        facebook_analysis_report = Report(
            title="Facebook Analysis Report",
            content="No Facebook profile found or analysis not available.",
            is_markdown=True
        )
        twitter_analysis_report = Report(
            title="Twitter Analysis Report",
            content="No Twitter profile found or analysis not available.",
            is_markdown=True
        )

        # Get social media urls
        facebook_url = vc_company_data.social_media_links.facebook
        twitter_url = vc_company_data.social_media_links.twitter
        youtube_url = vc_company_data.social_media_links.youtube
        
        # Check If company has Youtube channel
        # TODO: Remove the youtube block
        if False and youtube_url:
            youtube_data = get_youtube_stats(youtube_url)
            prompt = YOUTUBE_ANALYSIS_PROMPT.format(company_name=vc_company_data.name)
            youtube_insight = invoke_llm(
                system_prompt=prompt, 
                user_message=youtube_data,
                model=AI_MODEL
            )
            youtube_analysis_report = Report(
                title="Youtube Analysis Report",
                content=youtube_insight,
                is_markdown=True
            )
            
        # Check If company has Facebook account
        if facebook_url:
            # TODO Add Facebook analysis part
            pass
        
        # Check If company has Twitter account
        if twitter_url:
            # TODO Add Twitter analysis part
            pass
        
        return {
            # vc_company_data is now stored in current_lead
            "reports": [youtube_analysis_report]
        }

    def analyze_recent_news(self, state: GraphState):
        print(Fore.YELLOW + "----- Analyzing recent news about company -----\n" + Style.RESET_ALL)
        
        # Load states
        vc_company_data = state["current_lead"].vc_company_data
        
        # Fetch recent news using serper API
        recent_news = get_recent_news(company=vc_company_data.name)
        number_months = 6
        current_date = get_current_date()
        news_analysis_prompt = NEWS_ANALYSIS_PROMPT.format(
            company_name=vc_company_data.name, 
            number_months=number_months, 
            date=current_date
        )
        
        # Craft news analysis prompt
        news_insight = invoke_llm(
            system_prompt=news_analysis_prompt, 
            user_message=recent_news,
            model=AI_MODEL
        )
        
        news_analysis_report = Report(
            title="News Analysis Report",
            content=news_insight,
            is_markdown=True
        )
        return {"reports": [news_analysis_report]}
    
    def generate_company_profile_report(self, state: GraphState):
        print(Fore.YELLOW + "----- Generate company profile report -----\n" + Style.RESET_ALL)
        
        # Load reports
        reports = state["reports"]
        facebook_analysis_report = get_report(reports, "Facebook Analysis Report")
        twitter_analysis_report = get_report(reports, "Twitter Analysis Report")
        youtube_analysis_report = get_report(reports, "Youtube Analysis Report")
        news_analysis_report = get_report(reports, "News Analysis Report")
        vc_twitter_analysis_report = get_report(reports, "VC Twitter Analysis Report")

        inputs = f"""
        # **Company Data:**
        # **Recent News:**

        {news_analysis_report}

        # **VC Twitter Analysis:**

        {vc_twitter_analysis_report}
        """
        
        prompt = COMPANY_PROFILE_REPORT_PROMPT.format(
            company_name=state["current_lead"].vc_company_data.name,
            industry=state["current_lead"].vc_company_data.industry,
            date=get_current_date()
        )
        company_profile_report = invoke_llm(
            system_prompt=prompt, 
            user_message=inputs,
            model=AI_MODEL
        ) 
        
        company_profile_report = Report(
            title="Company Profile Report",
            content=company_profile_report,
            is_markdown=True
        )
        return {"reports": [company_profile_report]}
    
    def generate_custom_outreach_report(self, state: GraphState):
        print(Fore.YELLOW + "----- Crafting Custom outreach report based on gathered information -----\n" + Style.RESET_ALL)
        
        # Load reports
        reports = state["reports"]
        general_lead_search_report = get_report(reports, "General Lead Research Report")
        global_research_report = get_report(reports, "Global Lead Analysis Report")
        
        # TODO Create better description to fetch accurate similar case study using RAG
        # get relevant case study
        case_study_report = fetch_similar_case_study(general_lead_search_report)
        
        inputs = f"""
        **Research Report:**

        {global_research_report}

        ---

        **Case Study:**

        {case_study_report}
        """
        
        # Generate report
        custom_outreach_report = invoke_llm(
            system_prompt=GENERATE_OUTREACH_REPORT_PROMPT,
            user_message=inputs,
            model=AI_MODEL
        )
        
        # TODO Find better way to include correct links into the final report
        # Proof read generated report
        inputs = f"""
        {custom_outreach_report}

        ---

        **Correct Links:**

        ** Our website link**: {state["our_company_data"].website}
        """
        
        # Call our editor/proof-reader agent
        revised_outreach_report = invoke_llm(
            system_prompt=PROOF_READER_PROMPT,
            user_message=inputs,
            model=AI_MODEL
        )
        
        # Store report into google docs and get shareable link
        new_doc = self.docs_manager.add_document(
            content=revised_outreach_report,
            doc_title="Outreach Report",
            folder_name=self.drive_folder_name,
            make_shareable=True,
            folder_shareable=True, # Set to false if only personal or true if with a team
            markdown=True
        )  
        
        # print(f"new_doc: {new_doc}")
        return {
            "custom_outreach_report_link": new_doc["shareable_url"],
            "reports_folder_link": new_doc["folder_url"]
        }

    def generate_personalized_email(self, state: GraphState):
        """
        Generate a personalized email for the lead.

        @param state: The current state of the application.
        @return: Updated state with the generated email.
        """
        print(Fore.YELLOW + "----- Generating personalized email -----\n" + Style.RESET_ALL)
        
        # Load reports
        reports = state["reports"]
        general_lead_search_report = get_report(reports, "General Lead Research Report")
        
        vc_company_data = state["current_lead"].vc_company_data
        lead_data = f"""
        # **Company & Lead Information:**

        {general_lead_search_report}

        # Company Details:
        Company Name: {vc_company_data.name}
        Industry: {vc_company_data.industry}
        Website: {vc_company_data.website}
        Value Proposition: {vc_company_data.description}

        # Report Link:
        {state["custom_outreach_report_link"]}
        """
        our_company = state["our_company_data"]
        target_company = state["current_lead"].vc_company_data
        lead = state["current_lead"]

        email_context = {
            "first_name": lead.name.split()[0],
            "company_name": our_company.name,
            "company_description": our_company.description,
            "value_proposition": our_company.value_proposition,
            "target_market": our_company.target_market,
            "key_benefits": our_company.benefits,
            "sender_name": our_company.name
        }

        personalize_email_prompt = PERSONALIZE_EMAIL_PROMPT.format(**email_context)
        output = invoke_llm(
            system_prompt=personalize_email_prompt,
            user_message=lead_data,
            model=AI_MODEL,
            response_format=EmailResponse
        )
        
        # Get relevant fields
        subject = output.subject
        personalized_email = output.email
        
        # Get lead email
        email = state["current_lead"].email
        
        # Create draft email
        gmail = GmailTools()
        gmail.create_draft_email(
            recipient=email,
            subject=subject,
            email_content=personalized_email
        )
        
        # Send email directly
        if SEND_EMAIL_DIRECTLY:
            gmail.send_email(
                recipient=TEST_EMAIL,
                subject=f"{subject}-{email}",
                email_content=personalized_email
            )
        
        # Save email with reports for reference
        personalized_email_doc = Report(
            title="Personalized Email",
            content=personalized_email,
            is_markdown=False
        )
        return {"reports": [personalized_email_doc]}

    def generate_interview_script(self, state: GraphState):
        print(Fore.YELLOW + "----- Generating interview script -----\n" + Style.RESET_ALL)
        
        # Load reports and company data
        reports = state["reports"]
        vc_company_data = state["current_lead"].vc_company_data
        global_research_report = get_report(reports, "Global Lead Analysis Report")
        
        # Prepare data for SPIN questions
        our_company = state["our_company_data"]
        target_company = state["current_lead"].vc_company_data
        lead = state["current_lead"]
        
        spin_context = {
            "company_name": our_company.name,
            "value_proposition": our_company.value_proposition,
            "target_market": our_company.target_market,
            "benefits": our_company.benefits,
            "target_company_name": target_company.name,
            "target_company_profile": target_company.profile,
            "lead_profile": lead.profile
        }
        
        # Generate SPIN questions
        spin_questions = invoke_llm(
            system_prompt=GENERATE_SPIN_QUESTIONS_PROMPT.format(**spin_context),
            user_message=global_research_report,
            model=AI_MODEL
        )
        
        # Prepare data for interview script
        interview_context = {
            "company_name": our_company.name,
            "company_description": our_company.description,
            "value_proposition": our_company.value_proposition,
            "benefits": our_company.benefits,
            "contact_name": lead.name,
            "target_company": target_company.name
        }
        
        # Combine all inputs for interview script
        inputs = f"""
        # Research Report
        {global_research_report}

        # SPIN Questions
        {spin_questions}
        """
        
        # Generate interview script
        interview_script = invoke_llm(
            system_prompt=WRITE_INTERVIEW_SCRIPT_PROMPT,
            user_message=inputs,
            model=AI_MODEL
        )
        
        interview_script_doc = Report(
            title="Interview Script",
            content=interview_script,
            is_markdown=True
        )
        
        return {"reports": [interview_script_doc]}
    
    @staticmethod
    def await_reports_creation(state: GraphState):
        return {"reports": []}
    
    def save_reports_to_google_docs(self, state: GraphState):
        print(Fore.YELLOW + "----- Save Reports to Google Docs -----\n" + Style.RESET_ALL)
        
        # Load all reports
        reports = state["reports"]
        
        # Ensure reports are saved locally
        save_reports_locally(reports, self.drive_folder_name)

        # Save all reports to Google docs
        if SAVE_TO_GOOGLE_DOCS:
            for report in reports:
                self.docs_manager.add_document(
                    content=report.content,
                    doc_title=report.title,
                    folder_name=self.drive_folder_name,
                    markdown=report.is_markdown
                )

        return {"reports_folder_link": self.drive_folder_name}

    def update_CRM(self, state: GraphState):
        print(Fore.YELLOW + "----- Updating CRM records -----\n" + Style.RESET_ALL)
        # print(f"state: {state}")
        # save new record data, ensure correct fields are used
        new_data = {
            "Status": "ATTEMPTED_TO_CONTACT", # Set lead to attempted contact
            "Analysis Reports": state["reports_folder_link"],
            "Outreach Report": state.get("custom_outreach_report_link"),
            "Last Contacted": get_current_date()
        }
        self.lead_loader.update_record(state["current_lead"].id, new_data)
        
        # reset reports list
        state["reports"] = []
        
        return {"number_leads": state["number_leads"] - 1}
