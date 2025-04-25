from langchain_core.runnables.graph import MermaidDrawMethod

def draw_workflow_image(app):
  app.get_graph().draw_mermaid_png(
    output_file_path="workflow.png",
    draw_method=MermaidDrawMethod.PYPPETEER,
  )
