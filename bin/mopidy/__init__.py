from toolkit import stat
import subprocess
import os, signal

def start_music_server(args):
    global music_server_proc
    stat("Starting mopidy music server")
    if (args.card == 1):
        stat("Starting on card 1")
        music_server_proc = subprocess.Popen(["/usr/bin/mopidy", "--config", "/usr/share/mopidy/conf.d:/etc/mopidy/mopidy.conf"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
    else:
        stat("Starting on card 0")
        music_server_proc = subprocess.Popen(["/usr/bin/mopidy", "--config", "/usr/share/mopidy/conf.d:/etc/mopidy/mopidy.conf:/etc/mopidy/xcard0.conf"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)


def stop_music_server():
    stat("Stopping mopidy music server")
    os.kill(music_server_proc.pid, signal.SIGTERM)
    stat("Stopped mopidy music server")
