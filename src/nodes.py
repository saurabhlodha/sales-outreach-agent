import os
import json
from colorama import Fore, Style
from .tools.base.markdown_scraper_tool import scrape_website_to_markdown
from .tools.base.search_tools import get_recent_news
from .tools.base.gmail_tools import GmailTools
from .tools.google_docs_tools import GoogleDocsManager
from .tools.lead_research import research_lead_on_linkedin
from .tools.base.twitter_tools import extract_twitter_handle, get_twitter_timeline
from .tools.company_research import analyze_vc_firm, generate_company_profile
from .tools.youtube_tools import get_youtube_stats
from .tools.rag_tool import fetch_similar_case_study
from .prompts import *
from .state import LeadData, CompanyData, VCCompanyData, Report, GraphInputState, GraphState, SocialMediaLinks
from .structured_outputs import WebsiteData, EmailResponse
from .utils import invoke_llm, get_current_date, save_reports_locally
from src.tools.base.pdf_tools import read_pdf_content, analyze_pitch_deck
from src.tools.reports_manager import ReportManager

# Enable or disable sending emails directly using GMAIL
# Should be confident about the quality of the email
SEND_EMAIL_DIRECTLY = False
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
        self.report_manager = ReportManager()
        self.our_company_data = None
        self.current_lead = None
        self.vc_company_data = None

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
                vc_company_data=VCCompanyData(name=lead.get("Company Name", "")),
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

    def gather_lead_company_data(self, state: GraphState):
        print(Fore.YELLOW + "----- Analyzing our pitch deck -----\n" + Style.RESET_ALL)

        # Read and analyze our pitch deck
        pdf_path = os.getenv("PITCH_DECK_PATH", "data/decks/target.pdf")
        pdf_content = read_pdf_content(pdf_path)
        if not pdf_content:
            print(Fore.RED + f"Error: Could not read pitch deck at {pdf_path}" + Style.RESET_ALL)
            return "No more leads"
            
        # Analyze our pitch deck content
        company_analysis = analyze_pitch_deck(pdf_content)

        # Update our company data
        self.our_company_data = CompanyData()
        self.our_company_data.description = company_analysis.get("description", "")
        self.our_company_data.products_services = company_analysis.get("products_services", [])
        self.our_company_data.target_market = company_analysis.get("target_market", "")
        self.our_company_data.value_proposition = company_analysis.get("value_proposition", "")
        self.our_company_data.benefits = company_analysis.get("benefits", [])
        self.our_company_data.industry = company_analysis.get("industry", "")
        self.our_company_data.sales_approach = company_analysis.get("sales_approach", "")
        self.our_company_data.name = company_analysis.get("company_name", "")
        self.our_company_data.funding_stage = company_analysis.get("funding_stage", "")
        self.our_company_data.geography = company_analysis.get("geography", "")
        self.our_company_data.tech_stack = company_analysis.get("tech_stack", [])
        self.our_company_data.keywords = company_analysis.get("keywords", [])
        self.our_company_data.partnerships = company_analysis.get("partnerships", [])
        self.our_company_data.differentiators = company_analysis.get("differentiators", [])
        self.our_company_data.vc_fit = company_analysis.get("vc_fit", [])
        self.our_company_data.esg_impact = company_analysis.get("esg_impact", "")
        
        print(Fore.GREEN + f"Successfully analyzed pitch deck for {self.our_company_data.name}" + Style.RESET_ALL)
        
        # Update state and class variables
        state["our_company_data"] = self.our_company_data
        self.current_lead = state["current_lead"]
        self.vc_company_data = self.current_lead.vc_company_data
        
        return { 
            "our_company_data": self.our_company_data,
            "current_lead": self.current_lead
        }

    def fetch_linkedin_profile_data(self, state: GraphState):
        print(Fore.YELLOW + "----- Searching Lead data on LinkedIn -----\n" + Style.RESET_ALL)
        # print(state)
        lead_data = state["current_lead"]
        
        # Scrape lead linkedin profile
        (
            lead_profile, 
            company_name, 
            company_website,
            company_linkedin_url
        ) = research_lead_on_linkedin(lead_data.name, lead_data.email, lead_data.social_media_links.linkedin)
        lead_data.profile = lead_profile

        print(Fore.YELLOW + "----- Analyzing VC firm from web presence -----\n" + Style.RESET_ALL)
        
        # Analyze VC firm from their web presence
        vc_analysis = analyze_vc_firm(company_linkedin_url, company_website)
        
        # Update VC company data
        vc_company_data = lead_data.vc_company_data
        vc_company_data.name = vc_analysis.get("company_name", company_name)
        vc_company_data.website = company_website
        vc_company_data.description = vc_analysis.get("description", "")
        vc_company_data.investment_focus = vc_analysis.get("investment_focus", [])
        vc_company_data.portfolio_companies = vc_analysis.get("portfolio_companies", [])
        vc_company_data.investment_stages = vc_analysis.get("investment_stages", [])
        vc_company_data.investment_size = vc_analysis.get("investment_size", "")
        vc_company_data.geographic_focus = vc_analysis.get("geographic_focus", [])
        vc_company_data.investment_thesis = vc_analysis.get("investment_thesis", "")
        vc_company_data.recent_exits = vc_analysis.get("recent_exits", [])
        vc_company_data.industry = vc_analysis.get("industry", "")
        vc_company_data.tech_stack = vc_analysis.get("tech_stack", [])
        vc_company_data.value_add = vc_analysis.get("value_add", [])
        vc_company_data.esg_impact = vc_analysis.get("esg_impact", "")
        vc_company_data.key_partners = vc_analysis.get("key_partners", [])
        vc_company_data.investment_process = vc_analysis.get("investment_process", "")
        
        print(Fore.GREEN + f"Successfully analyzed VC firm {vc_company_data.name} from web presence" + Style.RESET_ALL)
        lead_data.vc_company_data = vc_company_data

        # Set the drive folder name
        self.drive_folder_name = f"{lead_data.name}_{vc_company_data.name}"

        return {
            "current_lead": lead_data,
            "reports": []
        }

    def analyze_lead_social_profile(self, state: GraphState):
        print(Fore.YELLOW + "----- Analyzing social profiles -----\n" + Style.RESET_ALL)
        
        # Extract twitter handle
        twitter_handle = extract_twitter_handle(self.current_lead.name, self.vc_company_data.name)
        
        reports = []
        
        # Analyze Twitter if handle found
        if twitter_handle:
            print(Fore.YELLOW + "Analyzing Twitter profile..." + Style.RESET_ALL)
            twitter_profile = get_twitter_timeline(twitter_handle)
            prompt = VC_TWITTER_ANALYSIS_PROMPT.format(lead_name=self.current_lead.name)
            twitter_insight = invoke_llm(
                system_prompt=prompt, 
                user_message=twitter_profile,
                model=AI_MODEL
            )
            self.report_manager.add_report(Report(
                title="VC Twitter Analysis Report",
                content=twitter_insight,
                is_markdown=True
            ))
        else:
            print(f"Twitter handle not found for {self.current_lead.name}")

        # Analyze other social media if available
        if self.vc_company_data.social_media_links.linkedin:
            print(Fore.YELLOW + "Analyzing LinkedIn presence..." + Style.RESET_ALL)
            # LinkedIn analysis is already done in fetch_linkedin_profile_data
            pass

        return {"current_lead": self.current_lead}
    
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
        
        # Get social media urls
        social_links = self.vc_company_data.social_media_links
        
        # Check If company has Youtube channel
        if social_links.youtube:
            print(Fore.YELLOW + "Analyzing YouTube channel..." + Style.RESET_ALL)
            youtube_data = get_youtube_stats(social_links.youtube)
            prompt = YOUTUBE_ANALYSIS_PROMPT.format(company_name=self.vc_company_data.name)
            youtube_insight = invoke_llm(
                system_prompt=prompt, 
                user_message=youtube_data,
                model=AI_MODEL
            )
            self.report_manager.add_report(Report(
                title="Youtube Analysis Report",
                content=youtube_insight,
                is_markdown=True
            ))
            
        # Check If company has Facebook account
        if social_links.facebook:
            print(Fore.YELLOW + "Facebook analysis not yet implemented" + Style.RESET_ALL)
            # TODO: Add Facebook analysis
            pass
        
        # Note: Twitter analysis is handled in analyze_lead_social_profile
        
        return {}

    def analyze_recent_news(self, state: GraphState):
        print(Fore.YELLOW + "----- Analyzing recent news about company -----\n" + Style.RESET_ALL)
        
        # Fetch recent news using serper API
        recent_news = get_recent_news(company=self.vc_company_data.name)
        number_months = 6
        current_date = get_current_date()
        news_analysis_prompt = NEWS_ANALYSIS_PROMPT.format(
            company_name=self.vc_company_data.name, 
            number_months=number_months, 
            date=current_date
        )
        
        # Analyze recent news
        news_insight = invoke_llm(
            system_prompt=news_analysis_prompt, 
            user_message=recent_news,
            model=AI_MODEL
        )
        
        # Add report to manager
        self.report_manager.add_report(Report(
            title="News Analysis Report",
            content=news_insight,
            is_markdown=True
        ))
        return {}
    
    def generate_company_profile_report(self, state: GraphState):
        print(Fore.YELLOW + "----- Generate company profile report -----\n" + Style.RESET_ALL)
        
        # Get reports from manager
        news_analysis_report = self.report_manager.get_report("News Analysis Report")
        vc_twitter_analysis_report = self.report_manager.get_report("VC Twitter Analysis Report")

        inputs = f"""
        # **Company Data:**
        # **Recent News:**

        {news_analysis_report}

        # **VC Twitter Analysis:**

        {vc_twitter_analysis_report}
        """
        
        prompt = COMPANY_PROFILE_REPORT_PROMPT.format(
            company_name=self.vc_company_data.name,
            industry=self.vc_company_data.industry,
            date=get_current_date()
        )
        company_profile = invoke_llm(
            system_prompt=prompt, 
            user_message=inputs,
            model=AI_MODEL
        ) 
        
        self.report_manager.add_report(Report(
            title="Company Profile Report",
            content=company_profile,
            is_markdown=True
        ))
        return {}
    
    def generate_custom_outreach_report(self, state: GraphState):
        print(Fore.YELLOW + "----- Crafting Custom outreach report based on gathered information -----\n" + Style.RESET_ALL)
        
        # Get reports from manager
        general_lead_search_report = self.report_manager.get_report("General Lead Research Report")
        global_research_report = self.report_manager.get_report("Global Lead Analysis Report")
        
        # Get relevant case study
        case_study_report = fetch_similar_case_study(general_lead_search_report)
        
        inputs = f"""
        **Research Report:**

        {global_research_report}

        ---

        **Case Study:**

        {case_study_report}
        """
        
        # Generate initial report
        custom_outreach_report = invoke_llm(
            system_prompt=GENERATE_OUTREACH_REPORT_PROMPT,
            user_message=inputs,
            model=AI_MODEL
        )
        
        # Proof read and add correct links
        inputs = f"""
        {custom_outreach_report}

        ---

        **Correct Links:**

        ** Our website link**: {self.our_company_data.website}
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
            folder_shareable=True,
            markdown=True
        )  
        
        # Add report to manager for reference
        self.report_manager.add_report(Report(
            title="Custom Outreach Report",
            content=revised_outreach_report,
            is_markdown=True
        ))
        
        return {
            "custom_outreach_report_link": new_doc["shareable_url"],
            "reports_folder_link": new_doc["folder_url"]
        }

    def generate_personalized_email(self, state: GraphState):
        """
        Generate a personalized email for the lead.
        """
        print(Fore.YELLOW + "----- Generating personalized email -----\n" + Style.RESET_ALL)
        
        # Get report from manager
        general_lead_search_report = self.report_manager.get_report("General Lead Research Report")
        
        lead_data = f"""
        # **Company & Lead Information:**

        {general_lead_search_report}

        # Company Details:
        Company Name: {self.vc_company_data.name}
        Industry: {self.vc_company_data.industry}
        Website: {self.vc_company_data.website}
        Value Proposition: {self.vc_company_data.description}

        # Report Link:
        {state["custom_outreach_report_link"]}
        """

        email_context = {
            "first_name": self.current_lead.name.split()[0],
            "company_name": self.our_company_data.name,
            "company_description": self.our_company_data.description,
            "value_proposition": self.our_company_data.value_proposition,
            "target_market": self.our_company_data.target_market,
            "key_benefits": self.our_company_data.benefits,
            "sender_name": self.our_company_data.name
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
        
        # Create draft email
        gmail = GmailTools()
        gmail.create_draft_email(
            recipient=self.current_lead.email,
            subject=subject,
            email_content=personalized_email
        )
        
        # Send email directly if enabled
        if SEND_EMAIL_DIRECTLY:
            gmail.send_email(
                recipient=TEST_EMAIL,
                subject=f"{subject}-{self.current_lead.email}",
                email_content=personalized_email
            )
        
        # Save email to report manager
        self.report_manager.add_report(Report(
            title="Personalized Email",
            content=personalized_email,
            is_markdown=False
        ))
        return {}

    def generate_interview_script(self, state: GraphState):
        print(Fore.YELLOW + "----- Generating interview script -----\n" + Style.RESET_ALL)
        
        # Load reports and company data
        global_research_report = self.report_manager.get_report("Global Lead Analysis Report")
        
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
        
        # Get all reports from the report manager
        reports = self.report_manager.get_all_reports()
        
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

        # Clear reports after saving
        self.report_manager.clear_reports()
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
