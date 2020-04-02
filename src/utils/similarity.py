from src.controllers.tags import *
from src.models import Link, LinkDataAccess, ProjectDataAccess


def divide_into_shingles(shingle_length, title, description):
    shingles = []
    title = parse_description(title)
    description = parse_description(description)
    tokens = description.split()
    tokens2 = title.split()
    for token in tokens2:
        tokens.append(token)
    i = 0
    while i < len(tokens):
        j = 0
        shingle = []
        while j < shingle_length:
            if i+j < len(tokens):
                shingle.append(tokens[i+j])
            j += 1
        # Only add shingles of given length (happend at end of text)
        if len(shingle) == shingle_length:
            shingles.append(shingle)
        i += 1
    return shingles


def calculate_jaccard_index(title1, text1, title2, text2):
    matched_shingles = 0
    shingles1 = divide_into_shingles(3, title1, text1)
    shingles2 = divide_into_shingles(3, title2, text2)
    for shingle1 in shingles1:
        for shingle2 in shingles2:
            if shingle1 == shingle2:
                matched_shingles += 1
    if len(shingles1) == 0 or len(shingles2) == 0:
        raise Exception("Could not generate shingles!")
    return matched_shingles/(len(shingles1) + len(shingles2))


def calculate_match(project1, project2, html_content_lang):
    match = calculate_jaccard_index(project1['title'], project1[html_content_lang], project2['title'],
                                    project2[html_content_lang])
    # Compare tags
    for tag1 in project1['tags']:
        for tag2 in project2['tags']:
            if tag1 == tag2:
                match += 0.1
    # Compare types
    for type1 in project1['types']:
        for type2 in project2['types']:
            if type1 == type2:
                match += 0.01
    # Compare employees
    for employee1 in project1['employees']:
        for employee2 in project2['employees']:
            if employee1["employee"]['e_id'] == employee2["employee"]['e_id']:
                match += 0.05
    # Compare research groups
    if project1['research_group'] == project2['research_group']:
        match += 0.05
    return match


def construct_link_database():
    all_projects = ProjectDataAccess(get_db()).get_projects(True, True)
    all_projects = [project.to_dict() for project in all_projects]
    link_access = LinkDataAccess(get_db())
    dutch_projects = list()
    english_projects = list()
    # Devide projects on the language of their description
    for project in all_projects:
        if project['html_content_eng'] is not None:
            english_projects.append(project)
        if project['html_content_nl'] is not None:
            dutch_projects.append(project)
    # Calculate the match between english projects
    for project1 in english_projects:
        for project2 in english_projects:
            if not project1 == project2:
                match = calculate_match(project1, project2, 'html_content_eng')
                if match > 0.071:
                    try:
                        link_access.add_link(Link(project1['project_id'], project2['project_id'], match))
                    except:
                        pass
    # Calculate the match between dutch projects
    for project1 in dutch_projects:
        for project2 in dutch_projects:
            if not project1 == project2:
                match = calculate_match(project1, project2, 'html_content_nl')
                if match > 1:
                    try:
                        link_access.add_link(Link(project1['project_id'], project2['project_id'], match))
                    except:
                        pass


if __name__ == '__main__':
    construct_link_database()
