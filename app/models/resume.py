# app/models/resume.py - Resume section database model
#
# Import db from app (from app import db)
from app import db

#
# Set the table name:
 
class Resume(db.Model):

    __tablename__ = 'resume_section'
    
    id = db.Column(db.Integer, primary_key = True)
    section_type = db.Column(db.String(100), nullable = False)
    title = db.Column(db.String(200), nullable = False)
    
    subtitle = db.Column(db.String(200), nullable = True)    
    
    description = db.Column(db.Text, nullable = True)
    
    order_index = db.Column(db.Integer, default = 0)

    





