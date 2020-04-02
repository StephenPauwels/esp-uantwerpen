from flask import Blueprint, request, session
from flask_login import current_user
from datetime import datetime
from src.models.db import get_db
from src.models import SessionDataAccess, Session, QueryDataAccess, Query


bp = Blueprint('cookies', __name__)


@bp.route('/new_session')
def new_session():
    if not current_user.is_authenticated or current_user.role != "student":
        return "false"

    session_access = SessionDataAccess(get_db())
    dt = datetime.now()
    obj = Session(session_id=None, student=current_user.user_id, start_of_session=dt)
    s_id = session_access.add_session(obj).session_id
    session['session_id'] = s_id
    return str(obj.session_id)


@bp.route('/new_query', methods=['POST'])
def new_query():
    query_access = QueryDataAccess(get_db())

    query = request.form['search_terms']
    current_session = request.form['session_id']
    dt = datetime.now()
    obj = Query(session_id=current_session, time_of_query=dt, search_terms=query)
    query_access.add_query(obj)
    return "true"
