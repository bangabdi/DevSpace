import re
import requests


def get_skills_text():
    """
    Returns text of skills and resources hosted in a github repo.
    """
    url = "https://raw.githubusercontent.com/lauragift21/awesome-learning-resources/master/README.md"
    r = requests.get(url)

    if r.status_code != 200:
        raise Exception("Fetch failed with status code %s." % r.status_code)

    return r.text


def get_link_info_from_text(text):
    """
    Return list of name and links from a text.
    """
    # Anything that isn't a square closing bracket
    name_regex = "[^]]+"

    # Anything enclosed in parantheses
    url_regex = "[^)]+"
    markup_regex = '\[({0})]\(\s*({1})\s*\)'.format(name_regex, url_regex)

    link_info = []
    for name, link in re.findall(markup_regex, text):
        link_info.append((name, link))

    return link_info


def get_skill_from_subheading(text):
    """
    Return list of skills by finding heading 2 from a text
    """
    # Ignore these heading 2 from match
    ignore_names = ["Table of Contents"]

    skills = []
    for match in re.findall("## (...*)", text):
        if match not in ignore_names:
            skills.append(match)

    return skills


def get_skill_regex(skills):
    """
    Returns a regex which will match any skill in the text
    """
    skills_piped = "|".join(skills)
    skill_regex = "## (%s)" % skills_piped
    return skill_regex


def get_resources_for_skills(text):
    """
    Return cleaned data of skills and resources from a text.

    Return format:

    {
        <skill_1>: [
            (<resource_name_1>, <resource_link_1>),
            (<resource_name_2>, <resource_link_2>),
            (<resource_name_3>, <resource_link_3>),
        ],
        <skill_2>: [
            (<resource_name_1>, <resource_link_1>),
            (<resource_name_2>, <resource_link_2>),
            (<resource_name_3>, <resource_link_3>),
        ],
        ...
    }
    """
    skills = get_skill_from_subheading(text)
    skill_regex = get_skill_regex(skills)

    skill = None
    SKILL_RESOURCES_MAP = {}
    resources_found = False
    for line in text.split("\n"):
        match = re.findall(skill_regex, line)

        # If the current line is a skill name
        # set SKILL_RESOURCES_MAP dict with the skill key
        if match:
            skill = match[0]
            SKILL_RESOURCES_MAP[skill] = []
            resources_found = True

        # If the current line has a hyperlink and is not a skill line,
        # it must be a resource link line. Append the resource line
        # in the resource list
        elif resources_found and line:
            resource = get_link_info_from_text(line)
            if resource:
                resource = resource[0]

                SKILL_RESOURCES_MAP[skill].append(resource)

    return SKILL_RESOURCES_MAP


def print_skill_json(SKILL_RESOURCES_MAP):
    import json
    print(json.dumps(SKILL_RESOURCES_MAP, indent=2))

if __name__ == '__main__':
    skills_text = get_skills_text()
    SKILL_RESOURCES_MAP = get_resources_for_skills(skills_text)
    print_skill_json(SKILL_RESOURCES_MAP)