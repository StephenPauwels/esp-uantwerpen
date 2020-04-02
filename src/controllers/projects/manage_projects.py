"""@package
This package enables the management usage for the database.
"""

from flask import jsonify
from src.models import EmployeeDataAccess, GuideDataAccess, ProjectDataAccess, Guide, TagDataAccess
from src.models.db import get_db


def manage(data):
    """
    Modifies the database.
    :param data: object holding all data to be modified in the database.
    :return: Json with success/failure status.
    """
    for entry in data['entries']:

        entry_type = entry['entry_type']

        for project in data["projects"]:

            try:
                if "add-employee" == entry_type:
                    guidance = entry['guidance']
                    name = entry['name']
                    add_employee(project, guidance, name)

                elif "remove-employee" == entry_type:
                    name = entry['name']
                    employee = EmployeeDataAccess(get_db()).get_employee_by_name(name)
                    GuideDataAccess(get_db()).remove_guide(employee.e_id, project)

                elif "add-tag" == entry_type:
                    tag = entry['tag']
                    add_tag(project, tag)

                elif "remove-tag" == entry_type:
                    tag = entry['tag']
                    ProjectDataAccess(get_db()).remove_tag(project, tag)

                elif "add-type" == entry_type:
                    p_type = entry['type']
                    add_type(project, p_type)

                elif "remove-type" == entry_type:
                    p_type = entry['type']
                    ProjectDataAccess(get_db()).remove_type(project, p_type)

                elif "replace-group" == entry_type:
                    group = entry['group']
                    ProjectDataAccess(get_db()).set_research_group(project, group)

                elif "replace-active" == entry_type:
                    active = entry['active']
                    ProjectDataAccess(get_db()).set_active(project, active)

                else:
                    return jsonify({'success': False, "message": "Missing correct entry_type"}), 400, {
                        'ContentType': 'application/json'}

            except Exception as e:
                return jsonify({'success': False, "message": str(e)}), 400, {'ContentType': 'application/json'}

    return jsonify({'success': True}), 200, {'ContentType': 'application/json'}


def add_employee(project, guidance, name):
    """
    Adds an employee in the database.
    :param project: project id
    :param guidance: guidance type
    :param name: employee name
    """
    try:
        employee_access = EmployeeDataAccess(get_db())
        employee = employee_access.get_employee_by_name(name)
        guide = Guide(employee.e_id, project, guidance)
        GuideDataAccess(get_db()).add_guide(guide)
    except:
        pass


def add_tag(project, tag):
    """
    Adds a tag in the database.
    :param project: project id
    :param tag: tag name
    """
    try:
        TagDataAccess(get_db()).add_tag(tag)
    except:
        pass
    try:
        ProjectDataAccess(get_db()).add_project_tag(project, tag)
    except:
        pass


def add_type(project, p_type):
    """
    Adds a type in the database.
    :param project: project id
    :param p_type: type name
    """
    try:
        ProjectDataAccess(get_db()).add_type(project, p_type)
    except:
        pass
