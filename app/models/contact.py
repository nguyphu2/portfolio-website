from app import db
from datetime import datetime

class Contact(db.Model):
    __tablename__ = 'contact_messages'


    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    message= db.Column(db.Text, nullable=False)


    created_at = db.Column(db.DateTime, default=datetime.utcnow)
            
    is_read  = db.Column(db.Boolean, default=False)

