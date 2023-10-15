import os

# Log requests to stdout
accesslog = "-"

# Listen on 0.0.0.0:$PORT or 0.0.0.0:8000
bind = f"0.0.0.0:{os.environ.get('PORT', '8000')}"

# Set a 5 min timeout---the data takes a while to load on initial startup.
timeout = 60*5
