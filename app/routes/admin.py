from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models import Project, Resume, Contact, AdminUser

admin = Blueprint('admin', __name__, url_prefix='/admin')


@admin.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = AdminUser.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('admin.dashboard'))

        flash('Invalid username or password')

    return render_template('admin/login.html')


@admin.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect(url_for('admin.login'))


@admin.route('/', methods=['GET'])
@login_required
def dashboard():
    project_count = Project.query.count()
    unread_count = Contact.query.filter_by(is_read=False).count()
    read_count = Contact.query.filter_by(is_read=True).count()
    resume_count = Resume.query.count()

    completed_count = Project.query.filter_by(status='completed').count()
    in_progress_count = Project.query.filter_by(status='in_progress').count()

    resume_by_type = {}
    for section_type, count in db.session.query(Resume.section_type, db.func.count(Resume.id)).group_by(Resume.section_type).all():
        resume_by_type[section_type] = count

    return render_template(
        'admin/dashboard.html',
        project_count=project_count,
        unread_count=unread_count,
        read_count=read_count,
        resume_count=resume_count,
        completed_count=completed_count,
        in_progress_count=in_progress_count,
        resume_by_type=resume_by_type,
    )


@admin.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        current_password = request.form.get('current_password')

        if not current_user.check_password(current_password):
            flash('Current password is incorrect')
            return render_template('admin/settings.html')

        new_username = request.form.get('username')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        if new_password and new_password != confirm_password:
            flash('New passwords do not match')
            return render_template('admin/settings.html')

        if new_username:
            current_user.username = new_username
        if new_password:
            current_user.set_password(new_password)

        db.session.commit()
        flash('Settings updated')
        return redirect(url_for('admin.settings'))

    return render_template('admin/settings.html')


# ---------------------------------------------------------------------------
# Projects CRUD
# ---------------------------------------------------------------------------

@admin.route('/projects', methods=['GET'])
@login_required
def projects():
    all_projects = Project.query.all()
    return render_template('admin/projects.html', projects=all_projects)


@admin.route('/projects/new', methods=['GET', 'POST'])
@login_required
def new_project():
    if request.method == 'POST':
        project = Project(
            title=request.form.get('title'),
            description=request.form.get('description'),
            tech_stack=request.form.get('tech_stack'),
            github_url=request.form.get('github_url'),
            live_url=request.form.get('live_url'),
            image_url=request.form.get('image_url'),
            status=request.form.get('status', 'completed'),
        )
        db.session.add(project)
        db.session.commit()
        return redirect(url_for('admin.projects'))

    return render_template('admin/project_form.html', project=None)


@admin.route('/projects/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_project(id):
    project = Project.query.get_or_404(id)

    if request.method == 'POST':
        project.title = request.form.get('title')
        project.description = request.form.get('description')
        project.tech_stack = request.form.get('tech_stack')
        project.github_url = request.form.get('github_url')
        project.live_url = request.form.get('live_url')
        project.image_url = request.form.get('image_url')
        project.status = request.form.get('status', 'completed')
        db.session.commit()
        return redirect(url_for('admin.projects'))

    return render_template('admin/project_form.html', project=project)


@admin.route('/projects/<int:id>/delete', methods=['POST'])
@login_required
def delete_project(id):
    project = Project.query.get_or_404(id)
    db.session.delete(project)
    db.session.commit()
    return redirect(url_for('admin.projects'))


# ---------------------------------------------------------------------------
# Resume sections CRUD
# ---------------------------------------------------------------------------

@admin.route('/resume', methods=['GET'])
@login_required
def resume():
    sections = Resume.query.order_by(Resume.order_index).all()
    return render_template('admin/resume.html', sections=sections)


@admin.route('/resume/new', methods=['GET', 'POST'])
@login_required
def new_resume_section():
    if request.method == 'POST':
        section = Resume(
            section_type=request.form.get('section_type'),
            title=request.form.get('title'),
            subtitle=request.form.get('subtitle'),
            description=request.form.get('description'),
            order_index=request.form.get('order_index', 0, type=int),
        )
        db.session.add(section)
        db.session.commit()
        return redirect(url_for('admin.resume'))

    return render_template('admin/resume_form.html', section=None)


@admin.route('/resume/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_resume_section(id):
    section = Resume.query.get_or_404(id)

    if request.method == 'POST':
        section.section_type = request.form.get('section_type')
        section.title = request.form.get('title')
        section.subtitle = request.form.get('subtitle')
        section.description = request.form.get('description')
        section.order_index = request.form.get('order_index', 0, type=int)
        db.session.commit()
        return redirect(url_for('admin.resume'))

    return render_template('admin/resume_form.html', section=section)


@admin.route('/resume/<int:id>/delete', methods=['POST'])
@login_required
def delete_resume_section(id):
    section = Resume.query.get_or_404(id)
    db.session.delete(section)
    db.session.commit()
    return redirect(url_for('admin.resume'))


# ---------------------------------------------------------------------------
# Messages
# ---------------------------------------------------------------------------

@admin.route('/messages', methods=['GET'])
@login_required
def messages():
    all_messages = Contact.query.order_by(Contact.created_at.desc()).all()

    for msg in all_messages:
        if not msg.is_read:
            msg.is_read = True
    db.session.commit()

    return render_template('admin/messages.html', messages=all_messages)
