#!/usr/bin/env python

import dbus
from dbus.mainloop.glib import DBusGMainLoop

# Initialize D-Bus main loop
DBusGMainLoop(set_as_default=True)

# Connect to NetworkManager's D-Bus interface
bus = dbus.SystemBus()
nm = bus.get_object('org.freedesktop.NetworkManager', '/org/freedesktop/NetworkManager')
nm_iface = dbus.Interface(nm, 'org.freedesktop.NetworkManager')

# Get all active connections
active_connections = nm_iface.Get('org.freedesktop.NetworkManager', 'ActiveConnections', dbus_interface='org.freedesktop.DBus.Properties')

# Loop through active connections and find the Wi-Fi device
for active_conn in active_connections:
    print(active_conn)
    conn_iface = dbus.Interface(active_conn, 'org.freedesktop.NetworkManager.Connection.Active')
    # connection_type = conn_iface.ConnectionType
    # if connection_type == '802-11-wireless':
    #     devices = conn_iface.Devices
    #     for device in devices:
    #         device_iface = dbus.Interface(device, 'org.freedesktop.NetworkManager.Device')
    #         device_type = device_iface.DeviceType
    #         if device_type == 2:  # DeviceType 2 corresponds to Wi-Fi
    #             wireless_iface = dbus.Interface(device, 'org.freedesktop.NetworkManager.Device.Wireless')
    #             access_points = wireless_iface.GetAccessPoints()
    #             for ap in access_points:
    #                 ssid = ap.Get('org.freedesktop.NetworkManager.AccessPoint', 'Ssid', dbus_interface='org.freedesktop.DBus.Properties')
    #                 strength = ap.Get('org.freedesktop.NetworkManager.AccessPoint', 'Strength', dbus_interface='org.freedesktop.DBus.Properties')
    #                 print(f"SSID: {ssid.decode('utf-8')}, Strength: {strength}")