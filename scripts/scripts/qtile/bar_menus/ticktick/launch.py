import subprocess
import signal
import os

# def set_environment_variables():
#     virtualenv_path = "/home/jonalm/scripts/qtile/bar_menus/ticktick/bin/activate"
#     os.environ["PATH"] = f"{virtualenv_path}/bin:{os.environ['PATH']}"
#     os.environ["VIRTUAL_ENV"] = virtualenv_path

def activate_virtualenv():
    virtualenv_path = "/home/jonalm/scripts/qtile/bar_menus/ticktick/bin/activate"

    activate_command = f"source {virtualenv_path} && env"
    env_output = subprocess.check_output(activate_command, shell=True, executable="/bin/bash")

    env_lines = env_output.decode("utf-8").splitlines()
    for line in env_lines:
        key, value = line.split("=", 1)
        os.environ[key] = value

def start_server():
    server_command = "python3 server.py"
    # with open("/tmp/script_output.log", "w") as log_file:
        # return subprocess.Popen(["python3", "scripts/qtile/bar_menus/ticktick/server.py"], stdout=log_file, stderr=subprocess.STDOUT)
    return subprocess.Popen(server_command, shell=True, preexec_fn=os.setsid)

def start_gtk_app():
    gtk_app_command = "python3 ticktick_menu.py"
    # with open("/tmp/script_output.log", "w") as log_file:
        # return subprocess.run(["python3", "scripts/qtile/bar_menus/ticktick/ticktick_menu.py"], stdout=log_file, stderr=subprocess.STDOUT)
    return subprocess.Popen(gtk_app_command, shell=True)

def stop_server(server_process):
    os.killpg(os.getpgid(server_process.pid), signal.SIGTERM)
    print("Server stopped!")

if __name__ == "__main__":
    server_process = None
    try:
        activate_virtualenv()

        server_process = start_server()
        gtk_app_process = start_gtk_app()

        gtk_app_process.wait()
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if server_process is not None:
            stop_server(server_process)
