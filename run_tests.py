import subprocess

command = 'nosetests --exe --with-coverage --cover-erase --cover-html '
command += '--cover-package=fuzzy_adventure.query_decomposition '
# command += '--cover-package=fuzzy_adventure.hana '
subprocess.call(command, shell=True)

