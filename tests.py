import subprocess

def ping(host):
    try:
        subprocess.check_call(["ping", "-c", "1", host])
        return True
    except subprocess.CalledProcessError:
        return False

def command(cmd):
    try:
        subprocess.check_call(cmd, shell=True)
        return True
    except subprocess.CalledProcessError:
        return False
