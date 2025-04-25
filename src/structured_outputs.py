from pydantic import BaseModel, Field


class WebsiteData(BaseModel):
    summary: str = Field(description="Summary of the company website content")
    blog_url: str | None = Field(None, description="The main blog URL of the company")
    youtube: str | None = Field(None, description="The company's YouTube profile link")
    twitter: str | None = Field(None, description="The company's Twitter profile link")
    facebook: str | None = Field(None, description="The company's Facebook profile link")
    linkedin: str | None = Field(None, description="The company's LinkedIn profile link")

class EmailResponse(BaseModel):
    subject: str = Field(description="An engaging subject line to encourage the lead to open the email.")
    email: str = Field(description="The personalized email content tailored to the lead’s profile and company information.")
