"""
Entry point for PyInstaller executable.
Wraps the Streamlit CLI to run app.py.
"""
import streamlit.web.cli as stcli
import os
import sys

def resolve_path(path):
    """Returns absolute path to resource, works for dev and for PyInstaller"""
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        return os.path.join(sys._MEIPASS, path)
    return os.path.join(os.getcwd(), path)

if __name__ == "__main__":
    # Make sure we can find app.py
    app_path = resolve_path("app.py")
    
    # Set up the command line arguments for streamlit
    sys.argv = [
        "streamlit",
        "run",
        app_path,
        "--global.developmentMode=false",
    ]
    
    # Run the Streamlit CLI
    sys.exit(stcli.main())
