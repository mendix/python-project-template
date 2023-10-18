import os
import subprocess

PROJECT_DIRECTORY = os.path.realpath(os.path.curdir)


if __name__ == "__main__":
    # if " cookiecutter.use_sometool }}" != "y":
    #     os.remove(os.path.join(PROJECT_DIRECTORY, "sometoolrc"))
    # The above couple lines are left as an example for the future.

    # Generate the Poetry lockfile
    subprocess.call(["poetry", "lock"], stderr=subprocess.STDOUT)
