import os
import markdown
from github import GithubIntegration, Github
from dotenv import load_dotenv

load_dotenv()

# Read environment variables
APP_ID = os.getenv("GITHUB_APP_ID")
INSTALLATION_ID = int(os.getenv("GITHUB_INSTALLATION_ID"))
PRIVATE_KEY_PATH = os.getenv("GITHUB_PRIVATE_KEY_PATH")
REPOSITORY = os.getenv("GITHUB_REPOSITORY")

with open(PRIVATE_KEY_PATH, "r") as key_file:
    PRIVATE_KEY = key_file.read()

integration = GithubIntegration(APP_ID, PRIVATE_KEY)

def get_installation_token():
    access_token = integration.get_access_token(INSTALLATION_ID)
    return access_token.token

def get_github_client():
    token = get_installation_token()
    return Github(token)

def get_all_posts():
    try:
        github = get_github_client()
        repo = github.get_repo(REPOSITORY)
        print('repo', repo)
        contents = repo.get_contents("posts")
        print('contents', contents)
        posts = []
        for file in contents:
            if file.name.endswith('.md'):
                content = repo.get_contents(f"posts/{file.name}").decoded_content.decode()
                posts.append({
                    "filename": file.name,
                    "title": file.name.replace("-", " ").replace(".md", "").title(),
                    "content": markdown.markdown(content)
                })
        return posts
    except Exception as e:
        print(f"Error fetching posts: {e}")
        return []

def get_post(filename):
    try:
        github = get_github_client()
        repo = github.get_repo(REPOSITORY)
        content = repo.get_contents(f"posts/{filename}").decoded_content.decode()
        return markdown.markdown(content)
    except Exception as e:
        print(f"Error fetching post '{filename}': {e}")
        return None