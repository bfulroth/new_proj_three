import os

# If the project rendered is not yet under version control get version from cookiecutter template
project_root = os.path.dirname(os.path.dirname(__file__))
if not os.path.exists(project_root + '/.git'):
    __version__ = "0.1.0"

# If the project is under version control use setuptools_scm to track version.
else:
    from setuptools_scm import get_version
    __version__ = get_version(root='..', relative_to=__file__)