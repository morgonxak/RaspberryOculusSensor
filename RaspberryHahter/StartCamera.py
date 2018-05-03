import subprocess

def start():
    p2 = subprocess.Popen("sh /home/pi/runCamera.sh" , shell=True, stdout=subprocess.PIPE)

def stop():
    proc1 = "killall -s 9 mjpg_streamer"
    subprocess.Popen(proc1, shell=True)