import subprocess

def get_wifi_ssid():
    try:
        # Run nmcli to get the active connection name
        connection_output = subprocess.check_output(['nmcli', '-t', '-f', 'NAME', 'connection', 'show', '--active'], text=True)
        connection_names = connection_output.strip().split('\n')

        # If there are connection names, use the first one (which should be the SSID)
        if connection_names:
            ssid = connection_names[0]
            return ssid
        else:
            return 'Not Connected'
    except subprocess.CalledProcessError:
        return 'Error'

if __name__ == '__main__':
    ssid = get_wifi_ssid()
    print(ssid)
