import re


def normalize_project_name(name):
    # https://www.python.org/dev/peps/pep-0503/#normalized-names
    return re.sub(r"[-_.]+", "-", name).lower()
