from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models import Project, Resume, Contact

public = Blueprint('public', __name__)


@public.route('/')
def home():
    projects = Project.query.filter_by(status='completed').order_by(Project.created_at.desc()).all()
    return render_template('index.html', projects=projects)


@public.route('/projects')
def projects():
    all_projects = Project.query.order_by(Project.created_at.desc()).all()
    return render_template('projects.html', projects=all_projects)


@public.route('/resume')
def resume():
    sections = Resume.query.order_by(Resume.order_index).all()
    return render_template('resume.html', sections=sections)


@public.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        message = Contact(
            name=request.form.get('name'),
            email=request.form.get('email'),
            message=request.form.get('message'),
        )
        db.session.add(message)
        db.session.commit()
        flash('Message sent!')
        return redirect(url_for('public.contact'))

    return render_template('contact.html')
