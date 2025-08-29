from IPython.display import Image
from .workflow import app

# Render inline
Image(app.get_graph().draw_mermaid_png())