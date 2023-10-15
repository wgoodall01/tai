import os

# Log requests to stdout
accesslog = "-"

# Listen on 0.0.0.0:$PORT or 0.0.0.0:8000
bind = f"0.0.0.0:{os.environ.get('PORT', '8000')}"
