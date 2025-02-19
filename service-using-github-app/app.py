import os
from emmett import App, redirect
from emmett.templating.templater import Templater
from dotenv import load_dotenv
from git_service import get_all_posts, get_post
from emmett.sessions import SessionManager

load_dotenv()

app = App(__name__)
app.config.secret_key = os.getenv("SECRET_KEY")
# Configure cookie-based session management.
app.pipeline = [SessionManager.cookies(app.config.secret_key)]

templater = Templater(path="templates")


@app.route("/")
async def index():
    """Display all blog posts from the private repository."""
    posts = get_all_posts()
    print('posts', posts)
    return templater.render("index.html", {"posts": posts})

@app.route("/post/<filename>")
async def post_detail(filename):
    """Display a single blog post's content."""
    content = get_post(filename)
    if not content:
        return redirect("/")
    return templater.render("post.html", {"content": content})
if __name__ == "__main__":
    app.cli()