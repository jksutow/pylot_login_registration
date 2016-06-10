from system.core.model import Model
import re

class Login(Model):
    def __init__(self):
        super(Login, self).__init__()

    def get_all_users(self):
        query = "SELECT * from users ORDER BY created_at DESC"
        return self.db.query_db(query)

    def get_user_by_id(self, user_id):
        query = "SELECT * FROM users WHERE id = :user_id"
        data = {
            'user_id': user_id
        }
        return self.db.query_db(query, data)

    def login_user(self, info):
        password = info['password']
        errors = []

        user_query = "SELECT * FROM users WHERE email = :email LIMIT 1"
        user_data = {'email': info['email']}
        user = self.db.query_db(user_query, user_data)
        if user:
           # check_password_hash() compares encrypted password in DB to one provided by user logging in
            if self.bcrypt.check_password_hash(user[0]['password'], password):
                return {
                    "status": True,
                    "user": user[0]
                }
        # Whether we did not find the email, or if the password did not match, either way return False
            else:
                errors.append('Password and email combination does not match!')
        return {
            "status": False,
            "errors": errors
        }

    def create_user(self, info):
        EMAIL_REGEX = re.compile(r'^[a-za-z0-9\.\+_-]+@[a-za-z0-9\._-]+\.[a-za-z]*$')
        errors = []
        # Some basic validation
        if not info['first_name']:
            errors.append('First name cannot be blank')
        elif len(info['first_name']) < 2:
            errors.append('First name must be at least 2 characters long')
        if not info['last_name']:
            errors.append('Last name cannot be blank')
        elif len(info['last_name']) < 2:
            errors.append('Last name must be at least 2 characters long')
        if not info['email']:
            errors.append('Email cannot be blank')
        elif not EMAIL_REGEX.match(info['email']):
            errors.append('Email format must be valid!')
        if not info['password']:
            errors.append('Password cannot be blank')
        elif len(info['password']) < 8:
            errors.append('Password must be at least 8 characters long')
        elif info['password'] != info['confirm_pw']:
            errors.append('Password and confirmation must match!')

        if errors:
            return {
                "status": False,
                "errors": errors
            }
        else:
            first_name = info['first_name']
            last_name = info['last_name']
            email = info['email']
            password = info['password']
            hashed_pw = self.bcrypt.generate_password_hash(password)
            create_query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES (:first_name, :last_name, :email, :password, NOW(), NOW())"
            create_data = {
                'first_name': info['first_name'],
                'last_name': info['last_name'],
                'email': info['email'],
                'password': hashed_pw
            }
            self.db.query_db(create_query, create_data)

            get_user_query = "SELECT * FROM users ORDER BY id DESC LIMIT 1"
            users = self.db.query_db(get_user_query)
            return {
                "status": True,
                "user": users[0]
            }
