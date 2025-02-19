import os
import markdown
from github import Github
from dotenv import load_dotenv

load_dotenv()

# Get repository name from .env
GITHUB_REPOSITORY = os.getenv("GITHUB_REPOSITORY")


def get_github_client(token):
    """Initialize a GitHub client with the authenticated user's token."""
    return Github(token)


def get_all_posts(user_token):
    try:
        github = get_github_client(user_token)
        repo = github.get_repo(GITHUB_REPOSITORY)
        contents = repo.get_contents("posts")
        print('contents', contents)
        posts = []
        for file in contents:
            content = repo.get_contents(f"posts/{file.name}").decoded_content.decode()
            posts.append({
                "filename": file.name,
                "title": file.name.replace("-", " ").replace(".md", "").title(),
                "content": markdown.markdown(content)  # Convert Markdown to HTML
            })

        print("posts", posts)
        return posts
    except Exception as e:
        print(f"Error fetching posts: {e}")
        return []


def get_post(user_token, filename):
    try:
        github = get_github_client(user_token)
        repo = github.get_repo(GITHUB_REPOSITORY)
        content = repo.get_contents(f"posts/{filename}").decoded_content.decode()
        return markdown.markdown(content)  # Convert Markdown to HTML
    except Exception as e:
        print(f"Error fetching post '{filename}': {e}")
        return None