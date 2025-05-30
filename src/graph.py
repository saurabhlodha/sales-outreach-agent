from langgraph.graph import END, StateGraph
from .nodes import OutReachAutomationNodes
from .state import GraphState
from .tools.leads_loader.lead_loader_base import LeadLoaderBase


class OutReachAutomation:
    def __init__(self, loader: LeadLoaderBase):
        # Initialize the automation workflow by building the graph
        self.app = self.build_graph(loader)

    def build_graph(self, loader):
        """
        Constructs the state graph for the outreach automation workflow.
        """
        # Create the main graph with a predefined state
        graph = StateGraph(GraphState)
        
        # Initialize the nodes with the provided lead loader
        nodes = OutReachAutomationNodes(loader)

        # **Step 1: Adding nodes to the graph**
        # Fetch new leads from the CRM
        graph.add_node("get_new_leads", nodes.get_new_leads)
        graph.add_node("check_for_remaining_leads", nodes.check_for_remaining_leads)

        # Research phase: gather data and insights about the lead
        graph.add_node("gather_lead_company_data", nodes.gather_lead_company_data)
        graph.add_node("fetch_linkedin_profile_data", nodes.fetch_linkedin_profile_data)
        graph.add_node("analyze_lead_social_profile", nodes.analyze_lead_social_profile)
        graph.add_node("review_company_website", nodes.review_company_website)
        graph.add_node("analyze_social_media_content", nodes.analyze_social_media_content)
        graph.add_node("analyze_recent_news", nodes.analyze_recent_news)
        graph.add_node("generate_company_profile_report", nodes.generate_company_profile_report)

        # Outreach preparation phase
        graph.add_node("generate_custom_outreach_report", nodes.generate_custom_outreach_report)
        graph.add_node("generate_personalized_email", nodes.generate_personalized_email)
        graph.add_node("generate_interview_script", nodes.generate_interview_script)

        # Reporting and finalization
        graph.add_node("save_reports_to_google_docs", nodes.save_reports_to_google_docs)
        graph.add_node("await_reports_creation", nodes.await_reports_creation)
        graph.add_node("update_CRM", nodes.update_CRM)

        # **Step 2: Setting up edges between nodes**

        # Entry point of the graph
        graph.set_entry_point("get_new_leads")

        # Transition from fetching leads to checking if there are leads to process
        graph.add_edge("get_new_leads", "check_for_remaining_leads")

        # Conditional logic for lead availability
        graph.add_conditional_edges(
            "check_for_remaining_leads",
            nodes.check_if_there_more_leads,
            {
                "Found leads": "gather_lead_company_data",  # Proceed if leads are found
                "No more leads": END  # Terminate if no leads remain
            }
        )

        # Research phase transitions
        graph.add_edge("gather_lead_company_data", "fetch_linkedin_profile_data")
        graph.add_edge("fetch_linkedin_profile_data", "analyze_lead_social_profile")
        graph.add_edge("analyze_lead_social_profile", "review_company_website")

        # Collect company information and branch into various analyses
        graph.add_edge("review_company_website", "analyze_social_media_content")
        graph.add_edge("review_company_website", "analyze_recent_news")

        # Analysis results converge into generating reports
        graph.add_edge("analyze_social_media_content", "generate_company_profile_report")
        graph.add_edge("analyze_recent_news", "generate_company_profile_report")
        graph.add_edge("generate_company_profile_report", "generate_custom_outreach_report")

        # Outreach material creation
        graph.add_edge("generate_custom_outreach_report", "generate_personalized_email")
        graph.add_edge("generate_custom_outreach_report", "generate_interview_script")

        # Await completion and finalize reports
        graph.add_edge("generate_personalized_email", "await_reports_creation")
        graph.add_edge("generate_interview_script", "await_reports_creation")
        graph.add_edge("await_reports_creation", "save_reports_to_google_docs")

        # Save reports and update the CRM
        graph.add_edge("save_reports_to_google_docs", "update_CRM")

        # Loop back to check for remaining leads
        graph.add_edge("update_CRM", "check_for_remaining_leads")
        return graph.compile()

