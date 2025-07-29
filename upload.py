import requests
import base64
import os
import sys
from dotenv import load_dotenv

# Load GitHub credentials from .env file
load_dotenv()
GITHUB_USERNAME = os.getenv("GITHUB_USERNAME")
GITHUB_REPO = os.getenv("GITHUB_REPO")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

def upload_to_github(file_path):
    """Uploads a file to GitHub and returns the public URL."""
    
    # Read the file content
    try:
        with open(file_path, "rb") as file:
            content = base64.b64encode(file.read()).decode("utf-8")
    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
        return None

    # Define GitHub API URL
    file_name = os.path.basename(file_path)
    github_path = f"encoded_images/{file_name}"  # Folder in repo
    url = f"https://api.github.com/repos/{GITHUB_USERNAME}/{GITHUB_REPO}/contents/{github_path}"

    # Prepare data payload
    payload = {
        "message": f"Upload {file_name}",
        "content": content,
        "branch": "main"  # Change if using a different branch
    }

    # Make the request
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    response = requests.put(url, json=payload, headers=headers)

    if response.status_code == 201:
        print("Upload successful!")
        github_file_url = response.json()["content"]["download_url"]
        print(f"File URL: {github_file_url}")
        return github_file_url
    else:
        print("Upload failed:", response.json())
        return None

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python upload_to_github.py <file_path>")
    else:
        upload_to_github(sys.argv[1])
