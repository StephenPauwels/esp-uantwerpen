# Based on code of Len Feremans
import re
from collections import Counter
from flask import Blueprint, jsonify, request, abort
from flask_login import current_user
from src.models import ProjectDataAccess, TagDataAccess, GuideDataAccess
from src.models.db import DBConnection, get_db
from src.config import config_data

bp = Blueprint('tags', __name__)


@bp.route('/generate-tags', methods=['GET'])
def get_generated_tags():
    if not current_user.is_authenticated and current_user.role != "student":
        abort(401)
    title = request.args['title']
    data = request.args['data']
    generated_tags = make_tags_from_description(title, data)
    return jsonify(generated_tags.most_common(5))


@bp.route('/get-employee-tags/<string:e_id>', methods=['GET'])
def get_employee_tags(e_id):
    try:
        return jsonify([key for key, _ in make_tags_for_employee(e_id).most_common(5)])
    except Exception as e:
        print(e)


bigram_filter = ['master_thesis', 'project_student', 'http_www', 'https_www', 'research_group']


# =========================================================
# Clean HTML tags from description
# =========================================================


def parse_description(description):
    # Remove html tags, entities and URL's with regex
    regex_remove_list = [r'<[^>]*>', r'&[^;]+;', r'http(s)?://[a-zA-Z0-9_\-\.]+$]']
    for item in regex_remove_list:
        description = re.sub(item, ' ', description)
    # Remove common seperators
    remove_lst = ['\\n', '\\r', '\\', '/',
                  '(', ')', '.', ',', '!', '-', '\'', ':', '"', '[', ']', ';']
    for item in remove_lst:
        description = description.replace(item, ' ')
    # Lower case
    return description.lower()


# =========================================================
# Natural language processing: stopwoords removal  +  numeric symbols and lower case
# stopwords
# =========================================================


stopwords_nl = [u'de', u'en', u'van', u'ik', u'te', u'dat', u'die', u'in', u'een', u'hij', u'het', u'niet', u'zijn',
                u'is', u'was', u'op', u'aan', u'met', u'als', u'voor', u'had', u'er', u'maar', u'om', u'hem', u'dan',
                u'zou', u'of', u'wat', u'mijn', u'men', u'dit', u'zo', u'door', u'over', u'ze', u'zich', u'bij', u'ook',
                u'tot', u'je', u'mij', u'uit', u'der', u'daar', u'haar', u'naar', u'heb', u'hoe', u'heeft', u'hebben',
                u'deze', u'u', u'want', u'nog', u'zal', u'me', u'zij', u'nu', u'ge', u'geen', u'omdat', u'iets',
                u'worden', u'toch', u'al', u'waren', u'veel', u'meer', u'doen', u'toen', u'moet', u'ben', u'zonder',
                u'kan', u'hun', u'dus', u'alles', u'onder', u'ja', u'eens', u'hier', u'wie', u'werd', u'altijd',
                u'doch', u'wordt', u'wezen', u'kunnen', u'ons', u'zelf', u'tegen', u'na', u'reeds', u'wil', u'kon',
                u'niets', u'uw', u'iemand', u'geweest', u'andere']

stopwords_en = [u'i', u'me', u'my', u'myself', u'we', u'our', u'ours', u'ourselves', u'you', u'your', u'yours',
                u'yourself', u'yourselves', u'he', u'him', u'his', u'himself', u'she', u'her', u'hers', u'herself',
                u'it', u'its', u'itself', u'they', u'them', u'their', u'theirs', u'themselves', u'what', u'which',
                u'who', u'whom', u'this', u'that', u'these', u'those', u'am', u'is', u'are', u'was', u'were', u'be',
                u'been', u'being', u'have', u'has', u'had', u'having', u'do', u'does', u'did', u'doing', u'a', u'an',
                u'the', u'and', u'but', u'if', u'or', u'because', u'as', u'until', u'while', u'of', u'at', u'by',
                u'for', u'with', u'about', u'against', u'between', u'into', u'through', u'during', u'before', u'after',
                u'above', u'below', u'to', u'from', u'up', u'down', u'in', u'out', u'on', u'off', u'over', u'under',
                u'again', u'further', u'then', u'once', u'here', u'there', u'when', u'where', u'why', u'how', u'all',
                u'any', u'both', u'each', u'few', u'more', u'most', u'other', u'some', u'such', u'no', u'nor', u'not',
                u'only', u'own', u'same', u'so', u'than', u'too', u'very', u's', u't', u'can', u'will', u'just', u'don',
                u'should', u'now', u'd', u'll', u'm', u'o', u're', u've', u'y', u'ain', u'aren', u'couldn', u'didn',
                u'doesn', u'hadn', u'hasn', u'haven', u'isn', u'ma', u'mightn', u'mustn', u'needn', u'shan', u'shouldn',
                u'wasn', u'weren', u'won', u'wouldn']

stop_words = set(stopwords_nl + stopwords_en)


# Goes through a string, splits everything in seperate words and filters stop/name words
# @param text String to filter
# @param name_tokens Piece of people's name to exclude from bigrams
def get_normal_tokens(text, name_tokens):
    tokens = text.split()
    tokens_copy = []
    for token in tokens:
        if re.match('[a-z][a-z][a-z]+', token) and not (token in stop_words) and not (
                token in name_tokens) and "@" not in token:
            tokens_copy.append(token)
    return tokens_copy


# ==============================================================
# Enumerate bi-grams, and count global frequency
# Count number of occurences of each token/work and each bigram
# ==============================================================


# Collects the bigrams from the title and description, joins them in one string with _ separator and stores it
# @param project Object with title (project[0]) and description (project[1])
def enumerate_bigrams(project, name_tokens):
    tokens = get_normal_tokens(project[0], name_tokens) + get_normal_tokens(project[1], name_tokens)
    project_bigrams = list()
    for z in range(0, len(tokens) - 1):
        token = tokens[z]
        token_next = tokens[z + 1]
        project_bigram = token + ' ' + token_next
        if not bigram_filter.count(project_bigram) == 1:
            project_bigrams.append(project_bigram)
    return project_bigrams


# ==============================================================
# General functions
# ==============================================================

# Finds the tags for a description.
# @param description The description to extract the tags from
# @param tags A list of all existing tags to compare with found tags
def find_tags_for_description(title, description, tags):
    project_data = [parse_description(title), parse_description(description)]
    bigrams = enumerate_bigrams(project_data, set())
    cnt_bigrams = Counter()
    for bigram in bigrams:
        cnt_bigrams[bigram] += 1
    for tag in tags:
        if tag in cnt_bigrams:
            cnt_bigrams[tag] += 3
    return cnt_bigrams


# Finds the tags for a project
# @param project A project in dict form
def find_tags_for_project(project):
    project_data = []
    # Make employee name tokens to exlude from text
    name_tokens = set()
    if type(project['employees']) == dict:
        for key in project['employees']:
            for name in project['employees'][key]:
                for name_token in name.lower().split():
                    name_tokens.add(name_token)
    else:
        for employee in project['employees']:
            for name_token in employee["employee"]["name"].lower().split():
                name_tokens.add(name_token)
    # Parse title and description
    project_data.append(parse_description(project['title']))
    if project['html_content_eng'] is not None:
        project_data.append(parse_description(project['html_content_eng']))
    else:
        project_data.append(parse_description(project['html_content_nl']))
    # Collects the bigrams
    return enumerate_bigrams(project_data, name_tokens)


# Finds the tags for a list of projects
# @param projects A list of projects
def find_all_project_tags(projects):
    cnt_bigrams = Counter()
    for project in projects:
        bigrams = find_tags_for_project(project)
        for bigram in bigrams:
            cnt_bigrams[bigram] += 1
    return cnt_bigrams


# Generates tags for a given title and description
#  @return Counter with tags
def make_tags_from_description(title, description):
    tags = TagDataAccess(get_db()).get_tags()
    return find_tags_for_description(title, description, tags)


# Generates tags for a certain projects that already has all it's data
#  @return A set of tags
def make_project_tags(p_id):
    project = ProjectDataAccess(get_db()).get_project(p_id, False)
    return find_tags_for_project(project.to_dict())


# Generates tags for all the projects
#  @return Counter with tags
def make_all_tags():
    all_projects = ProjectDataAccess(get_db()).get_projects(True)
    data_dct = [obj.to_dict() for obj in all_projects]
    return find_all_project_tags(data_dct)


# Generates tags for a certain employee
#  @param e_id Employee id
def make_tags_for_employee(e_id):
    cnt_bigrams = Counter()
    employee_projects = GuideDataAccess(get_db()).get_projects_for_employee(e_id)
    project_access = ProjectDataAccess(get_db())
    for project in employee_projects:
        tags = project_access.get_project_tags(project['project_id'])
        for tag in tags:
            cnt_bigrams[tag] += 1
    return cnt_bigrams


# 1 TIME USE. Fills tag database
def construct_tag_database():
    conn = DBConnection(dbname=config_data['dbname'], dbuser=config_data['dbuser'], dbpass=config_data['dbpass'],
                        dbhost=config_data['dbhost'])

    tag_access = TagDataAccess(conn)
    project_access = ProjectDataAccess(conn)

    # Add most common tags
    common_tags = make_all_tags()
    common_tags_list = []
    for tag, index in common_tags.most_common(200):
        if index > 2:
            try:
                tag_access.add_tag(tag)
            except:
                pass
            common_tags_list.append(tag)
    # Link tags with projects
    # Get all the project id's
    id_list = project_access.get_project_ids()
    for p_id in id_list:
        # Collect all the bigrams for the given project
        bigrams = make_project_tags(p_id)
        # Keep count of how many tags were added to the project
        tags_added = 0
        reserve_tags = {}
        # First associate the tags that are already in the database
        for bigram in bigrams:
            if common_tags_list.count(bigram) >= 1 and tags_added < 5:
                try:
                    project_access.add_project_tag(p_id, bigram)
                    tags_added += 1
                except Exception:
                    pass
            else:
                reserve_tags[bigram] = p_id
        # Associate the rest of the tags (max 5 tags)
        while tags_added < 5 and reserve_tags:
            tag, p_id = reserve_tags.popitem()
            # Add try because the tag might already exist in the database
            try:
                tag_access.add_tag(tag)
            except Exception:
                pass
            try:
                project_access.add_project_tag(p_id, tag)
            except:
                pass
            tags_added += 1


if __name__ == '__main__':
    construct_tag_database()
