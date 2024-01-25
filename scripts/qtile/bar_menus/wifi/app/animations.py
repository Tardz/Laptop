import gi
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk, Gdk, GLib
import subprocess

class Animations:
    def connect_process_start(self, password):
        ssid = self.network["SSID"]
        result = None
        if self.network["KNOWN"]:
            result = subprocess.call(f"nmcli connection up id {ssid}", shell=True)
        else: 
            result = subprocess.call(f"nmcli device wifi connect {ssid} password {password}", shell=True)

        if result == 0:
            with self.connect_process_successful.get_lock():
                self.connect_process_successful.value = True
        elif result == 4:
            with self.wrong_password.get_lock():
                self.wrong_password = True
        else:
            self.connect_process_start(password)

    def activate_load_circle_stage_1(self):
        self.load_circle_1.set_name("connect-animation-active")
        GLib.timeout_add(self.load_speed, self.activate_load_circle_2)
        return False

    def activate_load_circle_2(self):
        self.load_circle_2.set_name("connect-animation-active")
        GLib.timeout_add(self.load_speed, self.activate_load_circle_3)
        return False
    
    def activate_load_circle_3(self):
        self.load_circle_3.set_name("connect-animation-active")
        GLib.timeout_add(self.load_speed, self.deactivate_load_circle_stage_1)
        return False
    
    def deactivate_load_circle_stage_1(self):
        with self.wrong_password.get_lock():
            if self.wrong_password.value:
                for child in self.get_children():
                    self.remove(child)
                self.wrong_password = False
                self.terminate_connect_process()
                return False
        
        with self.connect_process_successful.get_lock():
            if self.connect_process_successful.value:
                self.terminate_connect_process()
                self.network_icon.set_name("connect-animation-active")
                self.ping_process = Process(target=self.ping_process_start)
                self.ping_process.start()
                GLib.timeout_add(self.load_speed, self.activate_load_circle_stage_2)
            else:
                self.load_circle_1.set_name("connect-animation-inactive")
                self.load_circle_2.set_name("connect-animation-inactive")
                self.load_circle_3.set_name("connect-animation-inactive")
                GLib.timeout_add(self.load_speed, self.activate_load_circle_stage_1)
        return False
    
    def terminate_connect_process(self):
        self.connect_process.terminate()
        self.connect_process.join()
        self.connect_process_successful = False
        self.connect_process = None 

    def ping_process_start(self):
        result = subprocess.call("ping -c 2 google.com", shell=True)
        if result == 0:
            with self.ping_process_successful.get_lock():
                self.ping_process_successful.value = True
                print(f"Worker: {self.ping_process_successful.value}")
        else:
            time.sleep(3)
            self.ping_process_start()
    
    def activate_load_circle_stage_2(self):
        self.load_circle_4.set_name("connect-animation-active")
        GLib.timeout_add(self.load_speed, self.activate_load_circle_4)
        return False

    def activate_load_circle_4(self):
        self.load_circle_5.set_name("connect-animation-active")
        GLib.timeout_add(self.load_speed, self.activate_load_circle_5)
        return False
    
    def activate_load_circle_5(self):
        self.load_circle_6.set_name("connect-animation-active")
        GLib.timeout_add(self.load_speed, self.deactivate_load_circle_stage_2)
        return False

    def deactivate_load_circle_stage_2(self):
        with self.ping_process_successful.get_lock():
            if self.ping_process_successful.value:
                self.ping_process_successful = False
                self.ping_process.terminate()
                self.ping_process.join()
                self.ping_process = None
                self.internet_icon.set_name("connect-animation-active")
                self.ignore_focus_lost = False
                GLib.timeout_add(self.load_speed, self.connection_successful_animation)
            else:
                self.load_circle_4.set_name("connect-animation-inactive")
                self.load_circle_5.set_name("connect-animation-inactive")
                self.load_circle_6.set_name("connect-animation-inactive")
                GLib.timeout_add(self.load_speed, self.activate_load_circle_stage_2)
        return False
    
    def connection_successful_animation(self):
        self.laptop_icon.set_name("connect-animation-success")
        self.network_icon.set_name("connect-animation-success")
        self.internet_icon.set_name("connect-animation-success")
        self.load_circle_1.set_name("connect-animation-success")
        self.load_circle_2.set_name("connect-animation-success")
        self.load_circle_3.set_name("connect-animation-success")
        self.load_circle_4.set_name("connect-animation-success")
        self.load_circle_5.set_name("connect-animation-success")
        self.load_circle_6.set_name("connect-animation-success")
        
        GLib.timeout_add(400, self.exit)
        return False