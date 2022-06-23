from flask import Blueprint, request, render_template, jsonify
from flask_login import current_user
from src.controllers.supporting_lists.manage_lists import manage, update_item
from src.models.type import TypeDataAccess
from src.models.tag import TagDataAccess
from src.models.research_group import *
from src.models.study_field import *
from src.models.employee import *
from src.models.db import get_db

bp = Blueprint('manage_lists', __name__)


@bp.route('/modify-lists', methods=["GET", "POST"])
def modify_lists():
    """
    Handles the GET & POST request to '/modify-lists'.
    GET: requests to render page
    POST: request managing sent data
    :return: Json with failure status / template rendering / function call to manage data
    """
    if not current_user.is_authenticated or current_user.role == "student":
        return jsonify({'success': False}), 400, {'ContentType': 'application/json'}
    if request.method == "GET":
        return render_template('supporting_lists.html')
    else:
        return manage(request.json)


@bp.route('/get-all-list-data', methods=['GET'])
def get_all_list_data():
    """
    Handles the GET request to '/get-all-list-data'.
    :return: Json with all list data
    """
    conn = get_db()

    all_types = TypeDataAccess(conn).get_types(False)
    all_tags = TagDataAccess(conn).get_tags()
    all_groups = ResearchGroupDataAccess(conn).get_research_groups(False)
    all_employees = EmployeeDataAccess(conn).get_employees(False)
    all_promotors = EmployeeDataAccess(conn).get_promotors(False)

    result = {
        "types": [obj.to_dict() for obj in all_types],
        "tags": all_tags,
        "research groups": [obj.to_dict() for obj in all_groups],
        "employees": [obj.to_dict() for obj in all_employees],
        "promotors": [obj.to_dict() for obj in all_promotors]
    }

    return jsonify(result)


@bp.route("/update-profile", methods=["POST"])
def update_profile():
    """
    Handles the POST request to '/update-profile'.
    :return: function call to update_item with sent data
    """
    return update_item(request.json)
