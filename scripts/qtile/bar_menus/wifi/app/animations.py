import gi
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk, Gdk
import subprocess
import copy
import sys
import os

class Animations:
    def __init__(self, app):
        self.app = app