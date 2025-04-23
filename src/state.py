from pydantic import BaseModel, Field
from typing import List, Annotated
from typing_extensions import TypedDict
from operator import add
    
class SocialMediaLinks(BaseModel):
    blog: str = ""
    facebook: str = ""
    twitter: str = ""
    youtube: str = ""
    linkedin: str = ""
    
class Report(BaseModel):
    title: str = ""
    content: str = ""
    is_markdown: bool = False

# Define the base data needed about the lead
class LeadData(BaseModel):
    id: str = Field(..., description="The unique identifier for the lead being processed")
    name: str = Field(..., description="The full name of the lead")
    address: str = Field(..., description="The address of the lead")
    email: str = Field(..., description="The email address of the lead")
    phone: str = Field(..., description="The phone number of the lead")
    profile: str = Field(..., description="The lead profile summary from LinkedIn data")
    vc_company_data: CompanyData = Field(..., description="The company data of the lead")

class CompanyData(BaseModel):
    name: str = Field("", description="The name of the company")
    website: str = Field("", description="The company's website URL")
    profile: str = Field("", description="The company's profile or summary")
    description: str = Field("", description="Detailed description of the company")
    products_services: List[str] = Field(default_factory=list, description="List of products and services offered")
    target_market: str = Field("", description="Description of the target market")
    value_proposition: str = Field("", description="The company's value proposition")
    benefits: List[str] = Field(default_factory=list, description="List of key benefits offered")
    industry: str = Field("", description="The industry the company operates in")
    sales_approach: str = Field("", description="The company's sales approach")
    social_media_links: SocialMediaLinks = Field(default_factory=SocialMediaLinks)

class GraphInputState(TypedDict):
    leads_ids: List[str]

class GraphState(TypedDict):
    leads_ids: List[str]
    leads_data: List[dict]
    current_lead: LeadData
    lead_score: str = ""
    our_company_data: CompanyData  # Data about our company from pitch deck
    reports: Annotated[list[Report], add]
    reports_folder_link: str
    custom_outreach_report_link: str
    personalized_email: str
    interview_script: str
    number_leads: int