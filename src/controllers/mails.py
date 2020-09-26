from flask import Blueprint, request, jsonify, render_template
from src.utils.mail import send_contact_message, send_mail
from src.models.db import get_db
from src.models import EmployeeDataAccess, ProjectDataAccess, StudentDataAccess, GuideDataAccess, RegistrationDataAccess
import datetime

bp = Blueprint('mails', __name__)


@bp.route('/admin-mail')
def admin_mail():
    return render_template('mails.html')


@bp.route('/mail', methods=['POST'])
def mail():
    first_name = request.json["first-name"]
    last_name = request.json["last-name"]
    role = request.json["role"]
    message = request.json["message"]
    send_contact_message(first_name, last_name, role, message)
    return jsonify({'success': True}), 200, {'ContentType': 'application/json'}


@bp.route('/admin-mail')
def view_admin_mail():
    return render_template('mails.html')


@bp.route('/admin-mail', methods=['POST'])
def post_admin_mail():
    data = request.get_json()
    subject = data['subject']
    content = data['content']
    receiver = data['receiver']
    lists = data['additions']

    is_student = receiver == 'students'
    if is_student:
        possible_receivers = StudentDataAccess(get_db()).get_students()
    else:
        possible_receivers = EmployeeDataAccess(get_db()).get_employees(False)

    for person in possible_receivers:
        mail_content = f'Beste {person.name},\n\n{content}'
        personal_lists = mail_lists(person, is_student, lists)
        mail_content += personal_lists

        # Don't send mail if not one list is relevant for this person
        if lists and not personal_lists:
            continue

        receiver_mail = person.student_id + "@ad.ua.ac.be" if is_student else person.email
        send_mail(receiver_mail, subject, mail_content)

    return jsonify({'success': True}), 200, {'ContentType': 'application/json'}


def order_lists(lists):
    # If roll over action is present, make sure the order is correct
    # This is important for the active and archived-old lists
    if 'archived-recent' in lists:
        lists.remove('archived-recent')
        lists.append('archived-recent')
        if 'active' in lists:
            lists.remove('active')
            lists.append('active')


def mail_lists(receiver, is_student, lists: list):
    order_lists(lists)
    text = ''
    for list_type in lists:
        func = globals()[list_type.replace('-', '_')]
        text += func(receiver, is_student)
    return text


def active(receiver, is_student):
    if is_student:
        return ''
    projects = GuideDataAccess(get_db()).get_projects_for_employee(receiver.e_id)
    access = ProjectDataAccess(get_db())
    projects = [access.get_project(x['project_id'], True) for x in projects]
    if not projects:
        return ''
    text = '\n\nACTIVE'
    for project in projects:
        text += project_link(project)
    return text


def archived_recent(receiver, is_student):
    if is_student:
        return ''
    projects = GuideDataAccess(get_db()).get_projects_for_employee(receiver.e_id)
    access = ProjectDataAccess(get_db())
    projects = [access.get_project(x['project_id'], True) for x in projects]
    if not projects:
        return ''
    text = '\n\nARCHIVED RECENT:'
    for project in projects:
        if project_is_full(project):
            access.set_active(project.project_id, False)
            text += project_link(project)
    return text


def project_link(project):
    return f'\n<a href="https://esp.uantwerpen.be/project-page?project_id={project.project_id}">{project.title}</a>'


def project_is_full(project):
    accepted = 0
    for registration in project.registrations:
        if registration['status'] == 'Accepted':
            accepted += 1
    return accepted == project.max_students


def archived_old(receiver, is_student):
    if is_student:
        return ''
    projects = GuideDataAccess(get_db()).get_projects_for_employee(receiver.e_id)
    access = ProjectDataAccess(get_db())
    projects = [access.get_project(x['project_id'], False) for x in projects]
    projects = [project for project in projects if not project.is_active]
    if not projects:
        return ''
    text = '\n\nARCHIVED OLD:'
    for project in projects:
        text += project_link(project)
    return text


def projects_assigned_new(receiver, is_student):
    access = ProjectDataAccess(get_db())
    if is_student:
        projects = access.get_project_ids(active_only=True)
        projects = [access.get_project(x, False) for x in projects]
    else:
        projects = GuideDataAccess(get_db()).get_projects_for_employee(receiver.e_id)
        projects = [access.get_project(x['project_id'], False) for x in projects]
    projects = filter(lambda p: p.is_active, projects)
    newly_assigned_projects = []
    for project in projects:
        newly_assigned_projects += [project for x in project.registrations if x['status'] == "Accepted"
                                    and x['last_updated'].month >= datetime.datetime.now().month - 2
                                    and x['last_updated'].year == datetime.datetime.now().year]
    if not newly_assigned_projects:
        return ''
    newly_assigned_projects = list(dict.fromkeys(newly_assigned_projects))
    text = "\n\nNEWLY ASSIGNED PROJECTS:"
    for project in newly_assigned_projects:
        text += project_link(project)
    return text


def projects_pending(receiver, is_student):
    if is_student:
        return ''
    projects = GuideDataAccess(get_db()).get_projects_for_employee(receiver.e_id)
    proj_access = ProjectDataAccess(get_db())
    projects = [proj_access.get_project(x['project_id'], False) for x in projects]
    projects = filter(lambda p: p.is_active, projects)
    reg_access = RegistrationDataAccess(get_db())
    pending_projects = [x for x in projects if reg_access.get_pending_registrations(x.project_id)]
    if not pending_projects:
        return ''
    text = "\n\nPROJECTS WITH PENDING REGISTRATIONS:"
    for project in pending_projects:
        text += project_link(project)
    return text

