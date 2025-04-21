from langchain_core.runnables.graph import MermaidDrawMethod

def draw_workflow_image(app):
  workflow_image = app.get_graph().draw_mermaid_png(
        draw_method=MermaidDrawMethod.API,
    )
  with open("workflow.png", "wb") as f:
        f.write(workflow_image)
