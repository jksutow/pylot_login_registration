from system.core.controller import *

class Logins(Controller):
    def __init__(self, action):
        super(Logins, self).__init__(action)
        self.load_model('Login')
        # self.db = self._app.db

    def index(self):
        return self.load_view('index.html')

    def register(self):
        user_info = {
            "first_name": request.form['first_name'],
            "last_name": request.form['last_name'],
            "email": request.form['email'],
            "password": request.form['password'],
            "confirm_pw": request.form['confirm_pw']
        }
        create_status = self.models['Login'].create_user(user_info)
        if create_status['status'] == True:
            session['id'] = create_status['user']['id']
            session['first_name'] = create_status['user']['first_name']
            return self.load_view('success.html')
        else:
            for message in create_status['errors']:
                flash(message, 'regis_errors')
            return redirect('/')

    def login(self):
        login_info = {
            "email": request.form['email'],
            "password": request.form['password']
        }
        login_status = self.models['Login'].login_user(login_info)
        if login_status['status'] == True:
            session['id'] = login_status['user']['id']
            session['first_name'] = ['user']['first_name']
            return self.load_view('success.html')
        else:
            for Login_message in login_status['errors']:
                flash(Login_message, 'login_errors')
            return redirect('/')
