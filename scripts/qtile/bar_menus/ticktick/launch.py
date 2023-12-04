import subprocess
import signal
import os

def activate_virtualenv():
    virtualenv_path = "bin/activate"

    activate_command = f"source {virtualenv_path} && env"
    env_output = subprocess.check_output(activate_command, shell=True, executable="/bin/bash")

    env_lines = env_output.decode("utf-8").splitlines()
    for line in env_lines:
        key, value = line.split("=", 1)
        os.environ[key] = value

def start_server():
    server_command = "python3 server.py"
    return subprocess.Popen(server_command, shell=True, preexec_fn=os.setsid)

def start_gtk_app():
    gtk_app_command = "python3 ticktick_menu.py"
    return subprocess.Popen(gtk_app_command, shell=True)

def stop_server(server_process):
    os.killpg(os.getpgid(server_process.pid), signal.SIGTERM)
    print("Server stopped!")

if __name__ == "__main__":
    try:
        activate_virtualenv()

        server_process = start_server()
        gtk_app_process = start_gtk_app()

        gtk_app_process.wait()
    finally:
        stop_server(server_process)
