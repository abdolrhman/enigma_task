from emmett import AppModule, redirect, session
from emmett.routing.urls import url

def create_auth_module(app):
    auth = AppModule(app, 'auth', import_name=__name__)

    @auth.route('/login')
    async def login():
        # In this scenario, you might simply set a dummy user.
        session['user'] = 'admin'
        return redirect(url('index'))

    @auth.route('/logout')
    async def logout():
        session.clear()
        return redirect(url('index'))

    return auth