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
    sales_approach: str = Field("", description="The company's sales/business model")
    funding_stage: str = Field("", description="Current funding stage (e.g., Pre-Seed, Seed, Series A)")
    geography: str = Field("", description="Geographic focus or HQ location")
    tech_stack: List[str] = Field(default_factory=list, description="Technology stack or innovation areas")
    keywords: List[str] = Field(default_factory=list, description="Business keywords for matching")
    partnerships: List[str] = Field(default_factory=list, description="Notable customers and partnerships")
    differentiators: List[str] = Field(default_factory=list, description="Competitive differentiators")
    vc_fit: List[str] = Field(default_factory=list, description="Traits that would attract VC attention")
    esg_impact: str = Field("", description="Social/ESG impact if any")
    social_media_links: SocialMediaLinks = Field(default_factory=SocialMediaLinks)

class VCCompanyData(CompanyData):
    investment_focus: List[str] = Field(default_factory=list, description="Areas of investment focus")
    portfolio_companies: List[str] = Field(default_factory=list, description="Notable portfolio companies")
    investment_stages: List[str] = Field(default_factory=list, description="Preferred investment stages")
    investment_size: str = Field("", description="Typical investment size range")
    geographic_focus: List[str] = Field(default_factory=list, description="Geographic regions of interest")
    investment_thesis: str = Field("", description="Key investment thesis or criteria")
    recent_exits: List[str] = Field(default_factory=list, description="Recent successful exits")

class LeadData(BaseModel):
    id: str = Field(..., description="The unique identifier for the lead being processed")
    name: str = Field(..., description="The full name of the lead")
    address: str = Field(..., description="The address of the lead")
    email: str = Field(..., description="The email address of the lead")
    phone: str = Field(..., description="The phone number of the lead")
    profile: str = Field(..., description="The lead profile summary from LinkedIn data")
    vc_company_data: VCCompanyData = Field(..., description="The VC firm data of the lead")
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