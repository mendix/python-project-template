import re
import sys

MODULE_REGEX = r"^[_a-zA-Z][_a-zA-Z0-9]+$"
PACKAGE_NAME = "{{ cookiecutter.package_name }}"

if __name__ == "__main__":
    if not re.match(MODULE_REGEX, PACKAGE_NAME):
        sys.exit("ERROR: The package name is not a valid Python module name.")
