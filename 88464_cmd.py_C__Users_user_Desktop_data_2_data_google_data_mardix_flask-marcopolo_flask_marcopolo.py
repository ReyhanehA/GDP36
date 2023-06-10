"""
Flask-MarcoPolo

Command line tool

flask-marcopolo -c project_name

"""

import os
import argparse
import pkg_resources
import flask_marcopolo

PACKAGE = flask_marcopolo
CWD = os.getcwd()
PROJECTS_TEMPLATES = "projects_templates"


def get_project_dir_path(project_name):
    return "%s/%s" % (CWD, project_name)


def copy_resource(src, dest):
    """
    To copy package data to destination
    """
    dest = (dest + "/" + os.path.basename(src)).rstrip("/")
    if pkg_resources.resource_isdir(PACKAGE.__name__, src):
        if not os.path.isdir(dest):
            os.makedirs(dest)
        for res in pkg_resources.resource_listdir(__name__, src):
            copy_resource(src + "/" + res, dest)
    else:
        if os.path.splitext(src)[1] not in [".pyc"]:
            with open(dest, "wb") as f:
                f.write(pkg_resources.resource_string(__name__, src))


def create_project(project_name, template="default"):
    """
    Create the project
    """
    project_dir = get_project_dir_path(project_name)
    run_file = "%s/run_%s.py" % (CWD, project_name)
    run_tpl = pkg_resources.resource_string(__name__, '%s/run_%s.py.tpl' % (PROJECTS_TEMPLATES, template))

    if not os.path.isdir(project_dir):
        os.makedirs(project_dir)
    else:
        raise OSError("Project dir '%s' exists already " % project_name)

    if not os.path.isfile(run_file):
        with open(run_file, "wb") as f:
            f.write(run_tpl.format(project_name=project_name))

    copy_resource("%s/%s/" % (PROJECTS_TEMPLATES, template), project_dir)


def main():

    print("-" * 80)
    print("%s %s - CLI Tool" % (PACKAGE.__NAME__, PACKAGE.__version__))
    print("")

    parser = argparse.ArgumentParser()
    parser.add_argument("project_name",
                        help="Project name"
                        )
    parser.add_argument("-c", "--create",
                        help="To create a new project."
                             " [flask-marcopolo -c project_name]",
                        action="store_true")
    arg = parser.parse_args()

    try:
        if arg.project_name:
            project_name = arg.project_name
            if arg.create:
                create_project(project_name, "default")
                print("+ PROJECT CREATED SUCCESSFULLY!")
                print("\n+ %s -> %s" % (project_name, get_project_dir_path(project_name)))
                print("\n+ Run 'python run_%s.py' to start the project's server" % project_name)
    except Exception as ex:
        print("- ERROR: %s" % ex.__str__())

    print("")

