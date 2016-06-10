from system.core.router import routes

routes['default_controller'] = 'Logins'
routes['POST']['/users'] = 'Logins#register'
routes['POST']['/users/login'] = 'Logins#login'
routes['POST']['/users/success'] = 'Logins#success'
    # routes['VERB']['/URL/GOES/HERE'] = 'Controller#method'
