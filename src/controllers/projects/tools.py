"""@package
This package enables the project editor.
"""

from src.models import ProjectDataAccess, EmployeeDataAccess, GuideDataAccess, Guide, DocumentDataAccess, \
    AttachmentDataAccess, TagDataAccess, Attachment, TypeDataAccess, Type, Document, Project
from src.models.db import get_db
from flask import jsonify


def project_editor(data):
    """
    Modifies an existing project and makes sure that database content is added/removed/updated where necessary.
    :param data: data object containing all info for the altered project
    :return: Json with success/failure status and the project id.
    """
    project_access = ProjectDataAccess(get_db())
    guide_access = GuideDataAccess(get_db())
    employee_access = EmployeeDataAccess(get_db())
    document_access = DocumentDataAccess(get_db())
    new_project = data.get('new', False)

    nl_data = data['html_content_nl']
    en_data = data['html_content_eng']
    if new_project:
        new_document = document_access.add_document(Document(None, en_data, nl_data))
        document_id = new_document.document_id
    else:
        document_id = data['description_id']
        document_access.update_document(Document(document_id, en_data, nl_data))

    title = data['title']
    group = data['research_group']
    max_students = data['max_students']
    is_active = data['is_active']

    if new_project:
        project = Project(None, title, max_students, document_id, group, is_active, None, 0, False)
        project = project_access.add_project(project)
        p_id = project.project_id
    else:
        p_id = data['project_id']
        project_access.update_project(p_id, title, max_students, group, is_active)
        guide_access.remove_project_guides(p_id)

    promotors = data['promotors']
    for promotor in promotors:
        if promotor != "":
            employee_id = employee_access.get_employee_by_name(promotor).e_id
            guide = Guide(employee_id, p_id, "Promotor")
            guide_access.add_guide(guide)

    copromotorlist = data['co-promotors']
    for copromotor in copromotorlist:
        if copromotor != "":
            employee_id = employee_access.get_employee_by_name(copromotor).e_id
            guide = Guide(employee_id, p_id, "Co-Promotor")
            guide_access.add_guide(guide)

    mentorlist = data['mentors']
    for mentor in mentorlist:
        if mentor != "":
            employee_id = employee_access.get_employee_by_name(mentor).e_id
            guide = Guide(employee_id, p_id, "Mentor")
            guide_access.add_guide(guide)

    tags = data['tags']
    if not new_project:
        project_access.remove_tags(p_id)
    tag_access = TagDataAccess(get_db())
    for tag in tags:
        if tag != "":
            try:
                tag_access.add_tag(tag)
            except:
                pass
            project_access.add_project_tag(p_id, tag)

    types = data['types']
    if not new_project:
        project_access.remove_types(p_id)
    type_access = TypeDataAccess(get_db())
    for p_type in types:
        try:
            mytype = Type(p_type, True)
            type_access.add_type(mytype)
        except:
            pass
        project_access.add_type(p_id, p_type)

    attachment_access = AttachmentDataAccess(get_db())
    if not new_project:
        attachment_access.remove_attachments(document_id)
    for json_attachment in data['attachments']:
        attachment = Attachment(name=json_attachment['name'], file_location=json_attachment['file_location'],
                                document_id=document_id)
        attachment_access.add_attachment(attachment)

    project_access.update_search_index()

    return jsonify({'success': True, 'project_id': p_id}), 200, {'ContentType': 'application/json'}
