import os
from emmett import AppModule, request, response, redirect, session
from authlib.integrations.starlette_client import OAuth
from dotenv import load_dotenv
from emmett.routing.urls import url
from authlib.integrations.base_client import OAuthError

load_dotenv()

print(os.getenv("GITHUB_CLIENT_ID"))
print(os.getenv("GITHUB_CLIENT_SECRET"))

oauth = OAuth()
oauth.register(
    name='github',
    client_id=os.getenv("GITHUB_CLIENT_ID"),
    client_secret=os.getenv("GITHUB_CLIENT_SECRET"),
    authorize_url='https://github.com/login/oauth/authorize',
    authorize_params=None,
    access_token_url='https://github.com/login/oauth/access_token',
    access_token_params=None,
    refresh_token_url=None,
    redirect_uri=os.getenv("GITHUB_REDIRECT_URI"),
    api_base_url='https://api.github.com/',
    client_kwargs={'scope': 'repo user:email'}
)

def create_auth_module(app):
    auth = AppModule(app, 'auth', import_name=__name__)

    @auth.route('/auth/login')
    async def login():
        redirect_uri = url('auth.callback', scheme=True)
        print('session', session)
        # Patch request to include the global session
        setattr(request, 'session', session)
        # Call Authlib's authorize_redirect to get a starlette redirect response.
        starlette_response = await oauth.github.authorize_redirect(request, redirect_uri)
        print(starlette_response)
        # Extract the Location header and return an Emmett redirect response.
        target_url = starlette_response.headers.get("location")
        return redirect(target_url)


    @auth.route('/auth/callback')
    async def callback():
        try:
            print('hello world')
            print('session', session)
            # Monkey-patch request to add a session attribute.
            # This makes Authlib happy by letting it do: request.session
            setattr(request, 'session', session)
            print('request', request)
            # token = await oauth.github.authorize_access_token(request)
            token = await oauth.github.authorize_access_token(request)
            # Now this call will use "https://api.github.com/user"
            user = await oauth.github.get('user', token=token)
            print('tokennn', token)
            print('user', user)
            print('session', session)
            # user = await oauth.github.get('user', token=token)
            session['user'] = user.json()['login']
            session['github_token'] = token['access_token']
            return redirect(url('index'))
        except OAuthError as e:
            print(f"OAuth Error: {e}")
            return "Authentication failed. Please try again."

    @auth.route('/logout')
    async def logout():
        session.clear()
        return redirect(url('index'))

    return auth