import subprocess
from subprocess import CalledProcessError

"""
"""

def start_jenkins():
    port = 8081
    if jenkins_alive() == False:
        command = 'nohup java -jar /usr/share/jenkins/jenkins.war --httpPort=' + str(port) + ' > jenkins_log.txt &'
        subprocess.call(command, shell=True)
    else:
        print "A process is already running on port 8081"



def stop_jenkins():
    try:
        r = subprocess.check_output('sudo netstat -tulpn | grep :8081', shell=True)
        port = r.split()[-1].split('/')[0]
        command = 'kill ' + port
        subprocess.call(command, shell=True)

        try:
            subprocess.check_output('sudo netstat -tulpn | grep :8081', shell=True)
            raise Exception("Process was not succesfully killed")
        except CalledProcessError:
            print "Process succesfully killed"

    except CalledProcessError:
        print "No process found on port 8081."


def jenkins_alive():
    try:
        subprocess.check_output('sudo netstat -tulpn | grep :8081', shell=True)
        return True
    except Exception:
        return False