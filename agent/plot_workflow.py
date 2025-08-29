from .workflow import app

# Generate the PNG
png_data = app.get_graph().draw_mermaid_png()

# Save to file
with open("workflow.png", "wb") as f:
    f.write(png_data)

print("Graph saved as workflow.png")
