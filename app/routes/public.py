from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db, limiter
from app.models import Project, Resume, Contact

public = Blueprint('public', __name__)

# Categories of Resume(section_type='skills') entries to leave out of the
# tech stack belt because they're methodology, not actual tools/technologies.
NON_TECH_SKILL_CATEGORIES = {'Analytics & Experimentation'}

SIMPLE_ICONS_BASE = 'https://cdn.simpleicons.org/'

# Some brands aren't in Simple Icons (trademark-policy exclusions) - those
# map to a full external URL instead of a Simple Icons slug.
TECH_ICON_MAP = {
    'python': SIMPLE_ICONS_BASE + 'python',
    'javascript': SIMPLE_ICONS_BASE + 'javascript',
    'c++': SIMPLE_ICONS_BASE + 'cplusplus',
    'mysql': SIMPLE_ICONS_BASE + 'mysql',
    'rstudio': SIMPLE_ICONS_BASE + 'rstudioide',
    'postgresql': SIMPLE_ICONS_BASE + 'postgresql',
    'git': SIMPLE_ICONS_BASE + 'git',
    'github': SIMPLE_ICONS_BASE + 'github',
    'asana': SIMPLE_ICONS_BASE + 'asana',
    'docker': SIMPLE_ICONS_BASE + 'docker',
    'pytorch': SIMPLE_ICONS_BASE + 'pytorch',
    'tensorflow': SIMPLE_ICONS_BASE + 'tensorflow',
    'scikit-learn': SIMPLE_ICONS_BASE + 'scikitlearn',
    'numpy': SIMPLE_ICONS_BASE + 'numpy',
    'pandas': SIMPLE_ICONS_BASE + 'pandas',
    'opencv': SIMPLE_ICONS_BASE + 'opencv',
    'yolov8': SIMPLE_ICONS_BASE + 'yolo',
    'huggingface': SIMPLE_ICONS_BASE + 'huggingface',
    'weights & biases': SIMPLE_ICONS_BASE + 'weightsandbiases',
    'power bi': 'https://upload.wikimedia.org/wikipedia/commons/c/cf/New_Power_BI_Logo.svg',
    'matplotlib': 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/matplotlib/matplotlib-original.svg',
    'tableau': 'https://upload.wikimedia.org/wikipedia/commons/4/4b/Tableau_Logo.png',
}

_AWS_LOGO = 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/amazonwebservices/amazonwebservices-original-wordmark.svg'
for _aws_service in ('aws', 's3', 'ec2', 'lambda', 'sagemaker', 'rds', 'iam', 'cloudwatch'):
    TECH_ICON_MAP[_aws_service] = _AWS_LOGO


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
@limiter.limit('5 per hour', methods=['POST'])
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
