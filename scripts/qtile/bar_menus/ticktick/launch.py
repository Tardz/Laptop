import subprocess
import signal
import os

def activate_virtualenv():
    activate_command = "source /home/jonalm/scripts/qtile/bar_menus/ticktick/bin/activate"
    subprocess.Popen(activate_command, shell=True)

def start_server():
    server_command = "python3 server.py"
    return subprocess.Popen(server_command, shell=True, preexec_fn=os.setsid)

def start_gtk_app():
    gtk_app_command = "python3 ticktick_menu.py"
    return subprocess.Popen(gtk_app_command, shell=True)

def stop_server(server_process):
    os.killpg(os.getpgid(server_process.pid), signal.SIGTERM)

if __name__ == "__main__":
    try:
        activate_virtualenv()

        server_process = start_server()
        gtk_app_process = start_gtk_app()

        gtk_app_process.wait()
    finally:
        stop_server(server_process)
