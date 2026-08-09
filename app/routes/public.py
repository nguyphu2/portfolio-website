from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models import Project, Resume, Contact

public = Blueprint('public', __name__)

# Categories of Resume(section_type='skills') entries to leave out of the
# tech stack belt because they're methodology, not actual tools/technologies.
NON_TECH_SKILL_CATEGORIES = {'Analytics & Experimentation'}

TECH_ICON_MAP = {
    'python': 'python',
    'javascript': 'javascript',
    'c++': 'cplusplus',
    'postgresql': 'postgresql',
    'git': 'git',
    'github': 'github',
    'asana': 'asana',
    'docker': 'docker',
    'pytorch': 'pytorch',
    'tensorflow': 'tensorflow',
    'scikit-learn': 'scikitlearn',
    'numpy': 'numpy',
    'pandas': 'pandas',
    'opencv': 'opencv',
    'huggingface': 'huggingface',
    'weights & biases': 'weightsandbiases',
    # AWS, S3, Lambda, Power BI, Tableau, and Matplotlib have no icon in
    # Simple Icons' library (likely trademark-policy exclusions) - they
    # intentionally fall back to text-only pills rather than a broken image.
}


def _split_skills(text):
    """Split a comma-separated skills string into items, without breaking
    apart anything inside parentheses (e.g. "AWS (S3, EC2, Lambda)")."""
    items = []
    depth = 0
    current = ''
    for ch in text:
        if ch == '(':
            depth += 1
            current += ch
        elif ch == ')':
            depth -= 1
            current += ch
        elif ch == ',' and depth == 0:
            if current.strip():
                items.append(current.strip())
            current = ''
        else:
            current += ch
    if current.strip():
        items.append(current.strip())
    return items


def _expand_parenthetical(item):
    """Turn "AWS (S3, EC2, Lambda)" into separate items: AWS, S3, EC2, Lambda."""
    if '(' not in item or not item.endswith(')'):
        return [item]
    base, _, inner = item.partition('(')
    base = base.strip()
    inner = inner[:-1]
    subs = [s.strip() for s in inner.split(',') if s.strip()]
    return [base] + subs


def _build_tech_stack(skill_sections):
    items = []
    for section in skill_sections:
        if section.title in NON_TECH_SKILL_CATEGORIES:
            continue
        for name in _split_skills(section.description or ''):
            for display_name in _expand_parenthetical(name):
                base = display_name.lower()
                items.append({'name': display_name, 'icon': TECH_ICON_MAP.get(base)})

    midpoint = (len(items) + 1) // 2
    return items[:midpoint], items[midpoint:]


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
    skill_sections = [s for s in sections if s.section_type == 'skills']
    tech_row1, tech_row2 = _build_tech_stack(skill_sections)
    return render_template('resume.html', sections=sections, tech_row1=tech_row1, tech_row2=tech_row2)


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
