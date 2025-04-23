WEBSITE_ANALYSIS_PROMPT = """
Analyze the provided webpage content from {main_url} and extract key information.

# Tasks

## 1. Company Overview
Provide a concise summary (max 300 words) of:
* Core business and value proposition
* Target market and customer segments
* Key products/services
* Technology and innovation focus

## 2. Important Links
Extract and validate links for:
* Social media profiles (Twitter, LinkedIn, Facebook, YouTube)
* Blog or news section
* Product documentation
* Contact information

# Output Format
Return a JSON object with the following structure (replace empty/missing values with null):
{{
    "summary": "string",
    "twitter": "string (URL)",
    "linkedin": "string (URL)",
    "facebook": "string (URL)",
    "youtube": "string (URL)",
    "blog_url": "string (URL)"
}}
"""

LEAD_SEARCH_REPORT_PROMPT = """
# Role
Analyze the provided LinkedIn profiles and generate a concise report highlighting key information about the lead and their company.

# Input Data
You have access to:
1. Lead's LinkedIn profile
2. Company's LinkedIn profile

# Output Format
Generate a markdown report with these sections:

## Lead Profile
* Current role and responsibilities
* Key expertise and skills
* Relevant experience

## Company Overview
* Core business focus
* Products/services
* Market position
* Company size and stage

## Potential Alignment
* Areas of mutual interest
* Possible collaboration opportunities
* Relevant industry experience

# Notes
* Keep sections concise and focused
* Use bullet points for clarity
* Focus on information relevant for business development
* Avoid speculation - stick to available facts
"""

VC_TWITTER_ANALYSIS_PROMPT = """
You are a Professional Investment Analyst specializing in VC analysis. Your role is to analyze a venture capitalist's Twitter timeline to understand their investment thesis, preferences, and potential alignment with startup pitches.

# Tasks

## 1- Investment Focus:
Analyze the VC's investment interests through their tweets:
* Preferred industries and technologies
* Investment stage preferences (seed, Series A, etc.)
* Geographic focus and remote investment stance
* Check size range and co-investment preferences
* Recent investment announcements and portfolio updates

## 2- Strategic Insights:
Evaluate the VC's perspective on:
* Market trends and opportunities
* Views on emerging technologies
* Startup evaluation criteria
* Red flags and deal-breakers
* Advice frequently given to founders

## 3- Engagement Style:
Understand their communication preferences:
* Interaction style with founders
* Content they frequently engage with
* Professional network and co-investors
* Personal interests and conversation topics
* Speaking engagements and thought leadership

# Output Format:
* Structure the analysis to highlight alignment opportunities
* Include specific tweets or threads that demonstrate key insights
* Note any recent changes in investment focus or criteria
* Identify potential conversation starters and shared interests
* Highlight any portfolio companies similar to our solution
"""

NEWS_ANALYSIS_PROMPT = """
# **Role:**

You are a Professional Business Analyst specializing in analyzing company developments, market trends, and strategic initiatives.

---

# **Context:**

You will analyze recent news related to the {company_name} company. The objective is to identify and extract interesting and relevant facts, focusing on significant developments like acquisitions, product launches, executive changes, or major partnerships.

---

# **Specifics:**

Your tasks will include the following:

* **Only include relevant news from the last {number_months} months. Today’s date is {date}.**

* **Strategic Developments:** Focus on key business developments like:
  - Funding rounds and financial performance
  - Market expansion and new partnerships
  - Product launches and technological innovations
  - Leadership changes and key hires
  - Competitive positioning and market share

* **Growth Indicators:** Identify signals of business growth and market traction:
  - Revenue and user growth metrics
  - Customer acquisition and retention
  - Market penetration and geographic expansion
  - Technology advancement and IP development

* **Risk Assessment:** Analyze potential challenges and mitigation strategies:
  - Market competition and barriers
  - Regulatory compliance and legal matters
  - Technical scalability and infrastructure
  - Team capacity and expertise

---

# Notes:
* Report should be structured in valid markdown format.
* **Only include relevant news from the last {number_months} months. Today’s date is {date}.**
"""

COMPANY_PROFILE_REPORT_PROMPT = """
# **Role:**  
You are a Professional Business Analyst specializing in {industry} market analysis and investment opportunities. Your role involves analyzing company data, market positioning, and growth potential to craft detailed reports for potential investors and strategic partners.  

---

# **Task:**  
Generate a **Comprehensive Business Analysis Report** by analyzing the provided data about {company_name}. Your goal is to evaluate the company's market position, growth potential, and strategic opportunities. Focus on identifying partnership synergies, investment potential, and areas for mutual value creation.  

---

# **Context:**  
You will review detailed analysis reports for various platforms (e.g., blogs, Facebook, Twitter) and provide an in-depth explanation of the company's performance on each. Additionally, you will identify specific gaps, opportunities, and strategies to strengthen their digital engagement and branding.  

---

# **Report Structure:**  

## **Executive Summary:**  
Provide a high-level overview of the company's overall digital presence and key findings across all platforms. Clearly state the strengths, weaknesses, and areas of opportunity.  

## **Strategic Analysis:**
Analyze key business areas with supporting evidence:

- **Market Position:**
  * Current market share and competitive advantages
  * Target customer segments and penetration
  * Growth trajectory and expansion potential
  * Industry partnerships and ecosystem

- **Technology & Innovation:**
  * Core technology capabilities and IP
  * Product roadmap and R&D initiatives
  * Technical scalability and infrastructure
  * Innovation advantages and moats

- **Financial & Growth:**
  * Revenue model and pricing strategy
  * Growth metrics and unit economics
  * Capital efficiency and runway
  * Investment and funding requirements  

## **Recent News Summary:**  
Summarize any recent news related to the company, including milestones, achievements, challenges, or market developments. Explain how this news influences the company's digital presence or strategy.  

## **Overall Recommendations:**  
Provide a consolidated set of actionable steps to improve the company's digital presence. For each recommendation, explain the rationale and expected benefits, ensuring alignment with the company’s branding and engagement goals.  

---

# **Notes:**  
- The report should be detailed, comprehensive, and well-structured in markdown format.  
- Use clear examples, observations, and metrics to support your findings and recommendations.   
- Provide detailed explanations and actionable strategies for every insight.
- Use bullet points to organize the report where appropriate. Avoid lengthy paragraphs by breaking down information into easily digestible sections.   
- **Ignore and do not include the sections where data is not provided.** 
"""

GENERATE_OUTREACH_REPORT_PROMPT = """
# Role
Create a concise outreach report that demonstrates potential value alignment between our company and the target company.

# Available Data
1. Our company information:
   - Name: {company_name}
   - Description: {company_description}
   - Value proposition: {value_proposition}
   - Products/services: {products_services}
   - Benefits: {benefits}
   - Target market: {target_market}

2. Lead research report
3. Case study (if available)

# Output Format
Generate a markdown report with these sections:

## Executive Summary
* Brief overview of both companies
* Key areas of potential collaboration

## Value Alignment
* How our solutions address their needs
* Specific benefits for their business
* Relevant industry experience

## Next Steps
* Clear call to action
* Suggested meeting agenda

# Notes
* Keep the report under 500 words
* Focus on concrete value proposition
* Use bullet points for clarity
* Include specific examples where possible
"""

GENERATE_SPIN_QUESTIONS_PROMPT = """
Write personalized multiple SPIN selling questions for the provided lead, demonstrating a clear understanding of their company and specific challenges. Focus on how our solutions can help address these issues effectively. Keep the questions concise and highly relevant.  

## **Company Description**  

{target_company} is a {target_company_description} company specializing in {target_company_services}. With a mission to {target_company_mission}, {target_company} has positioned itself as a pioneer in the {target_company_industry} industry.  

## **Our Solutions**
{products_services}

## **Target Market**
{target_market}

## **Value Proposition**
{value_proposition}

## **Key Benefits**
{benefits}

## **Notes:**  
- Return only the SPIN questions, maximum of 15. 
- Focus on uncovering pain points, implications, and opportunities where our solutions can add value. 
"""

WRITE_INTERVIEW_SCRIPT_PROMPT = """
# **Role & Task:**  
You are a professional interview scriptwriter. Based on SPIN selling questions, company details, and lead summaries, write a compelling, conversational interview script tailored to engage marketing and sales professionals.  

# **Specific Requirements:**  
- Include personalized details and references to the lead’s business or challenges.  
- Include multiple relevant questions in each section.
- Highlight the unique solutions offered by **{company_name}**.  
- Use a conversational and approachable tone, maintaining professionalism.  

# **Context:**  

**{company_name}** {company_description}

Our services include:  
{products_services}

{value_proposition}  

# **Example of interview Script:**  

**Introduction:**  
"Hi [Prospect's Name], this is [Your Name] from our company {company_name}. How are you today?"  

**Personalized Hook:**  
"I’ve been following [Company's Name]'s recent [initiative/project] in {industry}. It's exciting to see the innovative approaches your team is implementing."  

**Situation Questions:**  
"I'm curious about your growth strategy and key initiatives. How are you currently approaching {key_process}? What role do strategic partnerships play in your roadmap?"  

**Problem Questions:**  
"What are the main challenges you face in scaling your {industry} solutions? Have you encountered any specific barriers in market expansion or technology adoption?"  

**Implication Questions:**  
"How do these challenges impact your ability to capture market share and maintain competitive advantages? What opportunities for growth might be missed without the right strategic partners?"  

**Need-Payoff Questions:**  
"How could a strategic partnership with our company {company_name} accelerate your growth objectives? What specific value could our {products_services} bring to your business model?"  

**Closing:**  
"I believe our company {company_name} can offer the perfect tools and strategies to address these challenges. Would you be open to a quick meeting next week to explore how we can help your VC firm achieve your goals?"  

# **Notes:**  
- Adapt the script based on prospect responses for a natural flow.  
- Ensure the conversation stays focused on their challenges and how {company_name} can provide tailored solutions.  
- Emphasize measurable results and time-saving benefits. 
"""

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
CRITICAL: Your response must start with an opening curly brace '{' and end with a closing curly brace '}'. Do not include ANY text before or after the JSON object.
Do not include the word 'json' or any other text. Just return the raw JSON object.

Example of what to return (notice it starts with '{' and ends with '}'):
{
    "company_name": "string",
    "description": "string",
    "products_services": ["string"],
    "target_market": "string",
    "value_proposition": "string",
    "benefits": ["string"],
    "industry": "string",
    "sales_approach": "string"
}
"""

PROOF_READER_PROMPT = """
# **Role:**  
You are a **Professional Proofreader and Quality Analyst** specializing in ensuring the accuracy, structure, and completeness of professional documents. Your task is to analyze the final outreach report, ensuring it meets the highest standards of professionalism, clarity, and effectiveness.  

---

# **Task:**  
Your primary responsibilities are:  
1. **Structural Analysis:** Verify that the report includes all required sections:  
   - **Executive Summary**  
   - **Company Analysis**  
   - **Strategic Opportunities**  
   - **Value Proposition**  
   - **Next Steps**  

2. **Content Completeness:** Ensure:  
   - Each section addresses its intended purpose effectively.  
   - All relevant links (e.g., company website, case studies, contact links) are included and functional.  
   - Recommendations and examples are tailored to the specific lead’s context.  

3. **Quality Enhancement: (If needed)**  
   - Refine language to ensure clarity, conciseness, and professionalism.  
   - Introduce minor enhancements, such as improved transitions or added examples, if necessary.  
   - Add any missing or incorrect links while maintaining logical flow and accuracy.  

--- 

# **Notes:**  
- Return the **revised final report** in markdown format, without any additional text or preamble. 
- Your goal is to refine the existing report, not rewrite it. Keep changes minimal but impactful.   
"""

PERSONALIZE_EMAIL_PROMPT = """
# **Role:**

You are an expert in business development and outreach. Your task is to craft a personalized email using the available information about the lead and your company.

# **Context**

You have access to:
1. Lead data: name, email, profile information
2. Your company data: description, products/services, target market, value proposition, and key benefits

# **Guidelines:**
- Keep the email concise and focused
- Use specific details from the lead's profile for personalization
- Highlight relevant aspects of your company that align with the lead's interests
- Maintain a professional yet engaging tone

# **Email Template:**

Hi {first_name},

[Brief personalization based on lead's profile]

At {company_name}, we {company_description}. Our {value_proposition} has been particularly effective for {target_market}, delivering {key_benefits}.

I'd love to schedule a brief call to discuss how we might work together.

Best regards,
{sender_name}

# **Notes:**
* Keep the email under 150 words
* Use only factual information from the provided data
* Focus on value alignment rather than generic praise
* Ensure all placeholders are replaced with actual data
"""

GENERATE_SPIN_QUESTIONS_PROMPT = """
# Role
Create strategic SPIN (Situation, Problem, Implication, Need-payoff) questions for a business development conversation.

# Available Data
## Our Company
- Name: {company_name}
- Value Proposition: {value_proposition}
- Target Market: {target_market}
- Key Benefits: {benefits}

## Target Company
- Lead's profile and experience
- Company's business focus
- Market position

# Output Format
Generate 3-4 questions for each SPIN category:

## Situation Questions
[Questions about current state]

## Problem Questions
[Questions about challenges]

## Implication Questions
[Questions about impact]

## Need-Payoff Questions
[Questions about solution value]

# Notes
* Keep questions concise and specific
* Focus on mutual value creation
* Use available data points
* Avoid hypotheticals
"""

WRITE_INTERVIEW_SCRIPT_PROMPT = """
# Role
Create a natural conversation script for a business development call using available company and lead information.

# Available Data
## Our Company
- Name: {company_name}
- Description: {company_description}
- Value Proposition: {value_proposition}
- Benefits: {benefits}

## Lead Information
- Name: {contact_name}
- Company: {target_company}
- Profile summary

# Output Format
Create a conversation script with these sections:

## Introduction (30 seconds)
* Greeting
* Quick company overview
* Meeting purpose

## Discovery (2-3 minutes)
* 2-3 key SPIN questions
* Follow-up points

## Value Proposition (2 minutes)
* Alignment points
* Specific benefits

## Next Steps (30 seconds)
* Clear action items
* Timeline

# Notes
* Keep it conversational
* Use natural transitions
* Include pauses for responses
* Stick to available facts
"""
