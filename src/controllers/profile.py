import os
import random
from flask import Blueprint, abort, jsonify
from flask_login import current_user
from src.models.db import get_db
from src.models import EmployeeDataAccess, GuideDataAccess, ResearchGroupDataAccess

bp = Blueprint('profile', __name__)


@bp.route('/random-profile-picture')
def random_profile_pic():
    if not current_user.is_authenticated or current_user.role == "student":
        abort(401)

    try:
        location = get_random_picture_location()
        return jsonify({'success': True, 'location': location}), 200, {'ContentType': 'application/json'}
    except:
        return jsonify({'success': False,
                        "message": "Randomize failed "}), \
               400, {'ContentType': 'application/json'}


@bp.route("/get-edit-profile-data/<string:name>")
def get_edit_profile_data(name):
    try:
        employee = EmployeeDataAccess(get_db()).get_employee_by_name(name)
        research_groups = ResearchGroupDataAccess(get_db()).get_research_groups(False)
        return jsonify({"employee": employee.to_dict(), "groups": [obj.to_dict() for obj in research_groups]})
    except:
        return jsonify({'success': False, "message": "Employee name from LDAP not found in database"}), 400, {
            'ContentType': 'application/json'}


@bp.route('/get-guides-project-info/<string:e_name>', methods=['GET'])
def get_guides_project_info(e_name):
    try:
        info = GuideDataAccess(get_db()).get_guides_project_info(e_name)
        return jsonify(info)
    except:
        return jsonify({'success': False, "message": "Employee name from LDAP not found in database"}), 404, {
            'ContentType': 'application/json'}


def get_random_picture_location():
    current_directory = os.path.dirname(os.path.abspath(__file__))
    picture_directory = os.path.join(current_directory, "static/images/avatars/png/")

    directory = "static/images/avatars/png/"

    avatars = []
    for file in os.listdir(picture_directory):
        location = os.path.join(directory, file)
        avatars.append(location)

    return random.choice(avatars)


def give_random_pictures():
    employeedata = EmployeeDataAccess(get_db())
    all_employees = employeedata.get_employees(False)

    for f in all_employees:
        if f.picture_location is None:
            f.picture_location = get_random_picture_location()
        employeedata.update_employee(f)
    return


if __name__ == "__main__":
    give_random_pictures()
