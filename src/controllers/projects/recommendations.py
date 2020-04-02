"""@package
This package enables the usage of recommendations.
"""

from flask import session
from flask_login import current_user
from src.models import StudentDataAccess, ProjectDataAccess, LinkDataAccess, LikeDataAccess, SessionDataAccess
from src.models.db import get_db
from random import shuffle


def get_projects_with_recommendations():
    """
    Fetches all projects, with their (updated) recommendation index.
    :return: Json of all projects
    """
    if current_user.is_authenticated and current_user.role == "student":
        # Check if student in database
        try:
            student = StudentDataAccess(get_db()).get_student(current_user.user_id)
            student_found = student is not None
            likes = LikeDataAccess(get_db()).get_student_likes(student.student_id)
            project_clicks = SessionDataAccess(get_db()).get_student_clicks(student.student_id)

            # If there are clicks present
            if project_clicks:
                max_clicks = max(project_clicks, key=project_clicks.get)
                max_clicks = project_clicks[max_clicks]
            else:
                max_clicks = 0

            recommendations = get_user_based_recommendations(get_favorite_projects(likes, project_clicks))

        except:
            student_found = False
    else:
        student_found = False

    project_access = ProjectDataAccess(get_db())
    active_only = not session.get("archive", False)
    all_projects = [obj.to_dict() for obj in project_access.get_projects(active_only)]

    max_views = project_access.get_most_viewed_projects(1, active_only)[0].view_count
    oldest, newest = project_access.get_oldest_and_newest()
    oldest = oldest.timestamp()
    biggest_difference = newest.timestamp() - oldest

    for project in all_projects:
        project["recommendation"] = 0

        if max_views != 0:
            project["recommendation"] += project["view_count"] / max_views

        if biggest_difference != 0:
            project["recommendation"] += (project["last_updated"] - oldest) / biggest_difference

        if not student_found:
            continue

        project["liked"] = project["project_id"] in likes

        if project["project_id"] in recommendations:
            project["recommendation"] += recommendations[project["project_id"]]

        if project["liked"]:
            project["recommendation"] += 0.5
        elif project["project_id"] in project_clicks and max_clicks != 0:
            project["recommendation"] += project_clicks[project["project_id"]] / max_clicks

    return all_projects


def get_user_based_recommendations(favorite_projects):
    """
    Fetches all user-specific recommendations, based on liked projects.
    :param favorite_projects: list of liked projects
    :return: dictionary containing a recommendation percentage for each project link
    """
    link_access = LinkDataAccess(get_db())

    # Get all links of the favorite projects
    all_links = []
    for project in favorite_projects:
        links = link_access.get_links_for_project(project)
        all_links.extend(links)

    # Edge case, no links so can't do anything
    if not all_links:
        return dict()

    max_match_percent = max(all_links, key=lambda link: link.match_percent).match_percent

    recommendations = dict()
    for link in all_links:
        recommendations[link.project_2] = link.match_percent / max_match_percent
    return recommendations


def get_favorite_projects(likes, project_clicks):
    """
    Fetches 20 liked projects, and when insufficient liked projects also the most viewed ones.
    :param likes: list containing all liked projects
    :param project_clicks: list of all project clicks
    :return: list of 20 favorite projects
    """
    # Get a list of (project, clicks) items sorted on their clicks
    most_clicked_projects = sorted(project_clicks.items(), key=lambda kv: kv[1])

    # List of maximum 20 favorite projects, first add the liked ones, then the most clicked ones
    favorite_projects = list(likes)
    shuffle(favorite_projects)
    favorite_projects = favorite_projects[:20]
    while len(favorite_projects) != 20 and len(most_clicked_projects) != 0:
        project = most_clicked_projects.pop(-1)[0]
        if project not in favorite_projects:
            favorite_projects.append(project)

    return favorite_projects
