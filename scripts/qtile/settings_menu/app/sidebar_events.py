import gi
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk, Gdk
import subprocess
import copy
import sys
import os

class EventHandler:
    def __init__(self, app):
        self.app = app

    def on_search_changed(self, entry):
        search_text = entry.get_text().lower()
        
        for row in self.app.side_bar.list.get_children():
            self.app.side_bar.list.remove(row)

        if not search_text:
            self.app.side_bar.configure_list()
            return
        
        new_list_elements = []

        for info in self.app.list_elements:
            if search_text in info["title"].lower():
                new_list_elements.append(info)
        
        self.app.side_bar.configure_list(new_list_elements)

    def on_search_pressed(self, entry):
        self.on_item_clicked(None, None, self.app.first_list_info, self.app.first_list_box)

    def on_item_pressed(self, widget, event, info, box):
        if event.keyval == Gdk.KEY_Return:
            self.on_item_clicked(widget, event, info, box)
        
    def on_item_clicked(self, widget, event, info, box):
        self.app.active_list_box.set_name("list-item-box-inactive")
        self.app.active_list_box = box
        self.app.active_list_box.set_name("list-item-box-active")
        self.app.active_list_text = info["title"]

        self.app.content.content_title.set_text(info["title"])
        self.app.content.content_icon.set_text(info["icon"])
        self.app.content.content_icon.set_name(info["css"] + "-content-icon")
        self.app.content.content_icon_box.set_name(info["css"] + "-box")

        if self.app.content.active_content_box:
            self.app.content.main_content_scrolled_window.remove(self.app.content.active_content_box)
        self.app.content.active_content_box = info["box"]
        if self.app.content.active_content_box:
            self.app.content.main_content_scrolled_window.add(self.app.content.active_content_box)
            self.app.content.active_content_box.show_all()

    def on_qtile_version_clicked(self):
        pass

    def on_qtile_switch_state_changed(self, switch, gparam, desc, data_key):
        self.app.required_restart = True
        self.app.qtile_data[data_key] = switch.get_active()
        if self.app.qtile_data[data_key]:
            desc.set_text("On")
            desc.set_name("sub-content-desc-active")
        else:
            desc.set_text("Off")
            desc.set_name("sub-content-desc-inactive")
        self.change_global_options_visability()

    def on_focus_clicked(self, widget, event, desc):
        self.required_restart = True
        self.app.qtile_data["focus_on_window_activation"] = desc
        self.app.content.active_focus_desc.set_name("focus-inactive")
        self.app.content.active_focus_desc = widget.get_child()
        self.app.content.active_focus_desc.set_name("focus-active")
        self.change_global_options_visability()

    def change_global_options_visability(self):
        if self.app.qtile_data == self.app.qtile_data_copy:
            self.app.content.save_box.get_style_context().remove_class('visible-box');
            self.app.content.save_box.get_style_context().add_class('hidden-box');
            self.app.content.revert_box.get_style_context().remove_class('visible-box');
            self.app.content.revert_box.get_style_context().add_class('hidden-box');
        else:
            self.app.content.save_box.get_style_context().add_class('visible-box');
            self.app.content.save_box.get_style_context().remove_class('hidden-box');
            self.app.content.revert_box.get_style_context().add_class('visible-box');
            self.app.content.revert_box.get_style_context().remove_class('hidden-box');

    def global_options_on_box_enter(self, widget, event, box, icon, box_css):
        box.set_name(box_css)
        icon.set_name("global-options-icon-active")

    def global_options_on_box_leave(self, widget, event, box, icon, icon_css):
        box.set_name("global-options-icon-box-inactive")
        icon.set_name(icon_css)

    def save_config(self, widget, event):
        self.app.content.original_focus_desc = self.app.content.qtile.active_focus_desc
        self.app.config_manager.write_config_to_file(self.app.qtile_data_file_path, self.app.qtile_data)
        self.app.load_qtile_data()
        if self.app.required_restart:
            subprocess.run("qtile cmd-obj -o cmd -f restart", shell=True)
        self.change_global_options_visability()
    
    def revert_config(self, widget, event):
        self.required_restart = False
        self.app.qtile_data = copy.deepcopy(self.app.qtile_data_copy)
        self.change_global_options_visability()
        self.update_content()

    def update_content(self):
        for switch in self.app.content.switches:
            switch[0].set_active(self.app.qtile_data[switch[1]])

        for desc in self.app.content.switch_descs:
            if self.app.qtile_data[desc[1]]:
                desc[0].set_text("On")
                desc[0].set_name("sub-content-desc-active")
            else:
                desc[0].set_text("Off")
                desc[0].set_name("sub-content-desc-inactive")

            self.app.content.active_focus_desc.set_name("focus-inactive")
            self.app.content.active_focus_desc = self.app.content.original_focus_desc
            self.app.content.active_focus_desc.set_name("focus-active")

    def on_exit_press(self, widget, event):
        self.exit_remove_pid()
    
    def get_mouse_position(self):
        from Xlib import display 
        try:
            d = display.Display()
            s = d.screen()
            root = s.root
            root.change_attributes(event_mask=0x10000)
            pointer = root.query_pointer()
            x, y = pointer.root_x, pointer.root_y
            return x, y
        except Exception:
            return None, None

    def on_focus_out(self, widget, event):
        if not self.app.ignore_focus_lost:
            self.exit_remove_pid()

    def on_button_press(self, widget, event):
        keyval = event.keyval
        state = event.state
        if keyval == Gdk.KEY_Escape:
            self.exit_remove_pid()
        if state & Gdk.ModifierType.CONTROL_MASK and keyval == Gdk.KEY_s:
            self.save_config(widget, event)

    def handle_sigterm(self, signum, frame):
        self.exit_remove_pid() 

    def exit_remove_pid(self):  
        try:
            with open(self.app.pid_file_path, "r") as file:
                pid = int(file.read().strip())
            try:
                os.remove(self.app.pid_file_path)
                os.kill(pid, 15)
            except ProcessLookupError:
                pass
        finally:
            sys.exit(0)