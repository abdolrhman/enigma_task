# Blog System

This is a blog system application built using Python and the Emmett framework. The application fetches blog posts from a private GitHub repository and displays them on a web interface. Users can log in using their GitHub accounts to view and manage the blog posts.

## Features

- Fetch and display blog posts from a private GitHub repository.
- User authentication via GitHub OAuth.
- View individual blog posts.
- Session management with cookies.

## Prerequisites

- Python 3.11
- GitHub account with a repository containing blog posts in Markdown format.
- GitHub App with necessary permissions to access the repository.

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/blog-system.git
    cd blog-system
    ```

2. Create a virtual environment and activate it:

    ```bash
    python -m venv .venv
    source .venv/bin/activate
    ```

3. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Create a `.env` file in the root directory and add the following environment variables:

    ```dotenv
    GITHUB_REPOSITORY="yourusername/yourrepository"
    GITHUB_CLIENT_ID="your_github_client_id"
    GITHUB_CLIENT_SECRET="your_github_client_secret"
    GITHUB_ACCESS_TOKEN="your_github_access_token"
    SECRET_KEY="your_secret_key"
    GITHUB_REDIRECT_URI="http://localhost:8000/auth/callback"
    ```

5. Create a GitHub App and obtain the following details:
    - `GITHUB_APP_ID`
    - `GITHUB_INSTALLATION_ID`
    - `GITHUB_PRIVATE_KEY_PATH`

6. Add the GitHub App details to the `.env` file:

    ```dotenv
    GITHUB_APP_ID="your_github_app_id"
    GITHUB_INSTALLATION_ID="your_github_installation_id"
    GITHUB_PRIVATE_KEY_PATH="path_to_your_private_key.pem"
    ```

## Usage

1. Start the application:

    ```bash
    emmett serve
    ```

2. Open your web browser and navigate to `http://localhost:8000`.

3. Log in using your GitHub account to view and manage blog posts.

## Project Structure

- `app.py`: Main application file.
- `auth.py`: Handles user authentication via GitHub OAuth.
- `git_service.py`: Fetches blog posts from the GitHub repository.
- `templates/`: Contains HTML templates for the application.
- `.env`: Environment variables for the application.
- `requirements.txt`: List of dependencies.


## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.