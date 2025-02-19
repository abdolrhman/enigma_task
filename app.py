import os
from emmett import App, redirect, request, session
from emmett.templating.templater import Templater
from git_service import get_all_posts, get_post
from dotenv import load_dotenv
from auth import create_auth_module
from emmett.sessions import SessionManager

load_dotenv()

app = App(__name__)
app.config.secret_key = os.getenv("SECRET_KEY")

app.pipeline = [SessionManager.cookies(app.config.secret_key)]

# Register authentication module
app.module("auth", create_auth_module(app), url_prefix="/auth")

templater = Templater(path="templates")

@app.route("/")
async def index():
    setattr(request, 'session', session)
    """Render homepage with all blog posts (only for authenticated users)."""
    user_token = session.get("github_token")

    print('user_token', user_token)
    if not user_token:
        return redirect("/auth/login")

    posts = get_all_posts(user_token)
    return dict(posts=posts)


@app.route("/post/<filename>")
async def post_detail(filename):
    """Render a single post page (only for authenticated users)."""
    user_token = request.cookies.get("github_token")

    if not user_token:
        return redirect("/auth/login")

    content = get_post(user_token, filename)

    if not content:
        return redirect("/")

    return templater.render("post.html", {"content": content})


if __name__ == "__main__":
    app.cli()