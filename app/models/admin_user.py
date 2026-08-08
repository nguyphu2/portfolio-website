
from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class AdminUser(UserMixin, db.Model):



#
# UserMixin gives Flask-Login the four required methods automatically:
#   is_authenticated, is_active, is_anonymous, get_id

    __tablename__ = 'admin_users'
    
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(150), unique = True, nullable = False)
    password_hash = db.Column(db.String(256), nullable = False)

    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash,password)

    def __repr__(self):
        
        return f'<AdminUser {self.username}'
  