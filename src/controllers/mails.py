from flask import Blueprint, request, jsonify, render_template
from src.utils.mail import send_contact_message

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




