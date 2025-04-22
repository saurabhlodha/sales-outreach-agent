WEBSITE_ANALYSIS_PROMPT = """
The provided webpage content is scraped from: {main_url}.

# Tasks

## 1- Summarize webpage content:
Write a 500 words comprehensive summary in markdown format analyzing:

1. Business Model & Value Creation:
* Core business model and revenue streams
* Market opportunity and growth potential
* Competitive advantages and unique selling propositions

2. Technology & Innovation:
* Key technological capabilities and IP
* Innovation roadmap and R&D focus
* Technical scalability and infrastructure

3. Market Position:
* Target market segments and size
* Current market share and positioning
* Growth strategy and expansion plans

4. Team & Leadership:
* Key executive backgrounds
* Domain expertise and track record
* Advisory board and partnerships

5. Financial Overview:
* Revenue model and pricing strategy
* Current financial metrics (if available)
* Funding history and capital allocation

## 2- Extract Important Links:
* Company social profiles and professional networks
* News and press coverage
* Product documentation or technical resources

# IMPORTANT:
* Focus on business metrics and growth indicators
* Highlight potential synergies and partnership opportunities
* Identify key risks and mitigation strategies
"""

LEAD_SEARCH_REPORT_PROMPT = f"""
# **Role:**

You are a Professional Business Analyst tasked with crafting a comprehensive report based on the LinkedIn profiles of both an individual and their company and the content of their website. 
Your goal is to provide an in-depth overview of the lead's professional background, the company's mission and activities, and identify key business insights that might inform potential opportunities or partnerships.

---

# **Task:**

Craft a detailed business profile report that includes insights about the individual lead and their associated company based on the provided LinkedIn and website information.
This report should include the following:

## **Company Overview:**
* **Name & Description:** Provide a brief description of the company, its mission, and its core business activities.
* **Website & Location:** Include the company's website URL and its headquarters' location(s).
* **Industry & Size:** Report the company’s industry and employee size.
* **Mission:** Summarize the company’s mission and primary offerings.  
* **Product and services:** Highlight areas where the company excels and its offered product and services.  

## **Lead Profile Summary:**
* **Professional Experience:** Summarize the lead’s current and past roles, including key responsibilities and achievements. Focus on their career trajectory, skill set, and contributions at each company.
* **Education:** List the lead's relevant educational background, including fields of study and the duration of their studies.
* **Skills & Expertise:** Identify the lead’s main areas of expertise, including any specific skills they bring to their role.
* **Key Insights:** Offer insights into the lead’s leadership qualities, relevant achievements, or experience that can be beneficial for future collaboration or partnerships.

---

# Notes:

* Focus on crafting a report that gives clear, actionable insights based on the data provided. 
* Use bullet points to organize the report where appropriate, ensuring clarity and conciseness. Avoid lengthy paragraphs by breaking down information into easily digestible sections.
* Final report should be well-organized in markdown format, with distinct sections for the company overview and lead profile. 
* Return only final report without any additional text or preamble.
"""

TWITTER_ANALYSIS_PROMPT = """
You are a Professional Business Analyst specializing in company analysis. Your role is to analyze the company's social media presence to understand their business strategy, market position, and potential opportunities for investment or partnership.

# Tasks

## 1- Business Overview:
Analyze the company's public presence focusing on:
* Business model and value proposition
* Target market and customer segments
* Industry positioning and competitive advantages
* Growth trajectory and market expansion

## 2- Strategic Analysis:
Evaluate the company's strategic direction through:
* Product/service announcements and launches
* Partnership and collaboration announcements
* Market expansion and growth initiatives
* Customer success stories and case studies
* Industry thought leadership and expertise

## 3- Investment Indicators:
Identify key business metrics and growth signals:
* Revenue and business growth indicators
* Customer acquisition and retention signals
* Market penetration and expansion evidence
* Team growth and key hires
* Technology advancement and innovation

# Output Format:
* Structure the analysis to highlight business potential and growth opportunities
* Support insights with specific examples and evidence
* Focus on strategic value and partnership potential
* Identify specific ways the company's solutions can benefit target customers
* Highlight synergies and collaboration opportunities
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

DIGITAL_PRESENCE_REPORT_PROMPT = """
# **Role:**  
You are a Professional Business Analyst specializing in {industry} market analysis and investment opportunities. Your role involves analyzing company data, market positioning, and growth potential to craft detailed reports for potential investors and strategic partners.  

---

# **Task:**  
Generate a **Comprehensive Business Analysis Report** by analyzing the provided data about {company_name}. Your goal is to evaluate the company's market position, growth potential, and strategic opportunities. Focus on identifying partnership synergies, investment potential, and areas for mutual value creation.  

---

# **Context:**  
You will review detailed analysis reports for various platforms (e.g., blogs, Facebook, Twitter, YouTube) and provide an in-depth explanation of the company's performance on each. Additionally, you will identify specific gaps, opportunities, and strategies to strengthen their digital engagement and branding.  

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

GLOBAL_LEAD_RESEARCH_REPORT_PROMPT = """
# **Role:**  
You are a Professional Business Analyst specializing in company evaluation and strategic partnerships. Your role involves analyzing company profiles, market opportunities, and growth potential to identify valuable collaboration and investment opportunities.

---

# **Task:**  
Generate a **Global Report** by analyzing the provided lead and company profiles, along with the company's digital presence data. The goal is to provide a comprehensive overview of the lead and their associated company, including engagement history and actionable recommendations. The report should help in understanding the company’s position, challenges, and opportunities while offering strategies to enhance engagement and outreach.

---

# **Context:**  
You will review:  
1. The **Lead Profile**, which includes professional details such as their journey, role, and interests.  
2. The **Company Profile**, which contains information on the {company_name} company's industry, size, mission, services & offerings, and positioning.  
3. The **Digital Presence Report**, summarizing the company's activities on blogs, social media platforms, and recent news.  

This information will form the basis of a structured report to support lead qualification, engagement planning, and company branding strategies.

---

# **Report Structure:**  

## **I. Lead Profile:**  
Provide a detailed description of the lead's professional background, including:  
- Current role and responsibilities.  
- Career history and notable achievements.  
- Interests, skills, and areas of expertise.  

## **II. Company Overview:**  
Describe the company’s profile, including:  
- Industry and size.  
- Mission and vision statements.  
- Products and services.  
- Market positioning and key differentiators.  

## **III. Engagement History:**  
### **Recent News:**  
Summarize relevant recent news about the company, including funding updates, product launches, or strategic changes. Highlight how this news may impact its market position or strategy.  

### **Social Media and Blog Activity:**  
Construct a detailed analysis of the company's digital presence, including:  
- **Current State:**  
  Evaluate performance on each platform (e.g., blogs, Facebook, Twitter, YouTube). Include key metrics, examples of successful or underperforming posts, and trends.  
- **Potential Improvements:**  
  Provide tailored recommendations for each platform to enhance engagement, visibility, and alignment with company goals.  

---

# **Notes:**  
- The report should be comprehensive, actionable, and formatted in markdown for clarity and usability.  
- Include examples, observations, and metrics where applicable to support your insights and recommendations.  
- Avoid summarizing excessively; instead, provide explicit details and actionable strategies.  
- Use bullet points to organize the report where appropriate. Avoid lengthy paragraphs by breaking down information into easily digestible sections.   
"""

GENERATE_OUTREACH_REPORT_PROMPT = """
# **Role:**  
You are a Professional Business Analyst specializing in {industry} market analysis and strategic partnerships. Your task is to write a comprehensive, personalized report demonstrating how our solutions align with the company's business objectives and can drive measurable value through potential collaboration or investment.  

---

# **Task:**  
Using the provided research report about the lead's company and the accompanying case study, generate a detailed outreach report that highlights:  
1. The lead's company challenges and opportunities.  
2. How our AI-driven solutions can help them solve their challenges.  
3. Showcase the tangible results that we achieved with similar businesses through our solutions.  

---

# **Context:**  
You have access to:  
1. A **detailed research report** about the lead’s company, including their services, challenges, and digital presence.  
2. A **relevant case study** showcasing the success of our AI-driven solutions in similar contexts.  

## **About us:** 

{company_description}

{value_proposition}

Trusted by innovative businesses, {company_name} combines {products_services} to deliver impactful, measurable results. {benefits} 

---

# **Instructions:**  
Your report should include the following five sections:  
   
**1. Introduction:** 
- Information about who we are and what are our services and offerings.

**2. Business Analysis:**  
- **Company Overview:** Summarize the lead’s business, industry, and key offerings.  
- **Challenges Identified:** Highlight their key challenges based on the research report.  
- **Potential for Improvement:** Identify areas where AI-driven solutions can drive measurable results.  

**3. Relevant AI Solutions:**  
- Propose three tailored AI-powered solutions addressing specific challenges or goals. Examples include:  
  - AI-driven social media automation across different platforms.  
  - AI blog content automation & SEO optimization. 
  - AI chatbots for website customer engagement.  
---

## **Introduction**  
At **{company_name}**, {company_description}

{value_proposition}

With our key benefits:
{benefits}

We're excited about the opportunity to partner with **{target_company}** to achieve measurable growth in your industry.

---

## **Business Analysis**  

### **Company Overview:**  
{target_company} is a {target_company_description} company specializing in {target_company_services}. With a mission to {target_company_mission}, {target_company} has positioned itself as a pioneer in the {target_company_industry} industry.  

### **Challenges Identified:**  
{challenges}  

### **Potential for Improvement:**  
{improvement_opportunities}  

---

### **Proposed Solutions**  

{solutions}  

---

### **Expected Results**  

{expected_results}

---

### **Next Steps**  

We'd love to discuss how these tailored solutions can help {target_company} achieve its goals. Let's schedule a 30-minute call to explore opportunities and create a roadmap for success.  

**Next Steps:**  
- Reply to this email with your availability.  
- We'll schedule a brief discovery call.  

We look forward to partnering with you!

--- 

**{company_name}** 

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
"Hi [Prospect's Name], this is [Your Name] from {company_name}. How are you today?"  

**Personalized Hook:**  
"I’ve been following [Company's Name]'s recent [initiative/project] in {industry}. It's exciting to see the innovative approaches your team is implementing."  

**Situation Questions:**  
"I'm curious about your growth strategy and key initiatives. How are you currently approaching {key_process}? What role do strategic partnerships play in your roadmap?"  

**Problem Questions:**  
"What are the main challenges you face in scaling your {industry} solutions? Have you encountered any specific barriers in market expansion or technology adoption?"  

**Implication Questions:**  
"How do these challenges impact your ability to capture market share and maintain competitive advantages? What opportunities for growth might be missed without the right strategic partners?"  

**Need-Payoff Questions:**  
"How could a strategic partnership with {company_name} accelerate your growth objectives? What specific value could our {products_services} bring to your business model?"  

**Closing:**  
"I believe {company_name} can offer the perfect tools and strategies to address these challenges. Would you be open to a quick meeting next week to explore how we can help [Company's Name] achieve your goals?"  

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