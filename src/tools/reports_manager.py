from .reports import Report

class ReportManager:
    def __init__(self):
        self.reports = {}
    
    def add_report(self, report: Report):
        self.reports[report.title] = report
    
    def get_report(self, title: str) -> str:
        return self.reports.get(title, "").content if title in self.reports else ""
    
    def get_all_reports(self) -> list[Report]:
        return list(self.reports.values())
    
    def clear_reports(self):
        self.reports.clear()

