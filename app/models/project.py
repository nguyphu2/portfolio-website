from app import db
from datetime import datetime


class Project(db.Model):

    __tablename__ = 'projects'
    
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(200), nullable = False)
    description = db.Column(db.Text, nullable = True)
    tech_stack = db.Column(db.String(300), nullable = True)
    github_url = db.Column(db.String(300), nullable = True)
        

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    live_url = db.Column(db.String(300), nullable = True)

    image_url = db.Column(db.String(300), nullable = True)
    status = db.Column(db.String(20), nullable = False, default = 'completed')

    