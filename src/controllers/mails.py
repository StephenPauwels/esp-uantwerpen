from flask import Blueprint, request, jsonify, render_template
from src.utils.mail import send_contact_message, send_mail
from src.models.db import get_db
from src.models import EmployeeDataAccess, ProjectDataAccess, StudentDataAccess

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
        mail_content = f'Beste {person.name}\n\n{content}'
        personal_lists = mail_lists(person, is_student, lists)
        mail_content += personal_lists

        # Don't send mail if not one list is relevant for this person
        if lists and not personal_lists:
            continue

        receiver_mail = person.student_id + "@ad.ua.ac.be" if is_student else person.email
        send_mail(receiver_mail, subject, mail_content)

    return jsonify({'success': True}), 200, {'ContentType': 'application/json'}


def mail_lists(receiver, is_student, lists):
    text = ''
    for list_type in lists:
        if list_type == 'active':
            text += active(receiver, is_student)
    return text


def active(receiver, is_student):
    pass


def archived_recent(receiver, is_student):
    pass


def archived_old(receiver, is_student):
    pass


def projects_assigned_new(receiver, is_student):
    pass


def projects_pending(receiver, is_student):
    pass

