from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class Users:
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL('users_schema').query_db(query)
        users = []
        for user in results:
            users.append( cls(user) )
        return users

    @classmethod
    def save(cls, data ):
        query = "INSERT INTO users ( first_name , last_name , email , created_at, updated_at ) VALUES ( %(fname)s , %(lname)s , %(email)s , NOW() , NOW() );"
        return connectToMySQL('users_schema').query_db( query, data )

    @classmethod
    def get_user(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        result = connectToMySQL('users_schema').query_db(query,data)
        return cls(result[0])

    @classmethod
    def update(cls,data):
        query = "UPDATE users SET first_name=%(fname)s,last_name=%(lname)s, email=%(email)s, updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL('users_schema').query_db(query,data)

    @classmethod
    def destroy(cls,data):
        query = "DELETE FROM users WHERE id = %(id)s;"
        return connectToMySQL('users_schema').query_db(query,data)

    @staticmethod
    def validate_user(user):
        is_valid = True
        if len(user['fname']) <= 0:
            flash("First name is required.")
            is_valid = False
        if len(user['lname']) <= 0:
            flash("Last name is requried.")
            is_valid = False
        if len(user['email']) <= 0:
            flash("email is requried.")
            is_valid = False
        elif not EMAIL_REGEX.match(user['email']):
            flash("Invalid email address!")
            is_valid = False
        return is_valid