from app import app
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + "/..")

# Vercel expects a WSGI callable named 'app'
app = app