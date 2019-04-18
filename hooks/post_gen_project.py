import os


PROJECT_DIRECTORY = os.path.realpath(os.path.curdir)


if __name__ == "__main__":
    if "{{ cookiecutter.use_pylint }}" != "y":
        os.remove(os.path.join(PROJECT_DIRECTORY, "pylintrc"))
