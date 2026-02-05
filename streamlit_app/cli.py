"""
Command-line interface for the Streamlit app.
"""

import sys
import subprocess


def main():
    """Main entry point for running the Streamlit app."""
    subprocess.run([
        sys.executable, "-m", "streamlit", "run",
        "streamlit_app/app.py"
    ])


if __name__ == "__main__":
    main()
