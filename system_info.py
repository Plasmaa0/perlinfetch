import platform
import subprocess
import os
import socket
import re
import screeninfo
import psutil

# Hostname
def hostname():
    host = platform.node()
    return host

# Machine type
def machine():
    machine = platform.machine()
    return machine

# Kernel version
def kernel():
    kernel_v = platform.release()
    return kernel_v

# Distro info
def distro():
    if platform.system() == 'Linux':
        with open('/etc/os-release') as f:
            distro = next((line.split('=')[1].strip().strip('"') for line in f if line.startswith('PRETTY_NAME')), '')
    else:
        distro = platform.system()
    return distro

# Window manager
def wm():
    try:
        window_manager = subprocess.check_output(['wmctrl', '-m'], universal_newlines=True).split('\n')[0].split(':')[1].strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        window_manager = "Unknown"
    return window_manager

# Number of packages installed via different package managers
def packages():
    pacman_count = str(subprocess.check_output(["pacman", "-Qq"]), 'utf-8').count('\n')
    return str(pacman_count)

# Local IP
def ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # This will try to connect to Google's DNS server using an unused port
        s.connect(('8.8.8.8', 80))
        local_ip = s.getsockname()[0]
    except:
        # If the above fails, fallback to the output of 'hostname -I'
        local_ip = subprocess.check_output(['hostname', '-I'], universal_newlines=True).strip().split(' ')[0]

    s.close()

    return str(local_ip)


# Terminal emulator
def term():
    terminal = os.environ.get('TERM')
    return terminal

# Shell
def shell():
    shell = os.environ.get('SHELL')
    return shell

# Uptime
def uptime():
    try:
        uptime = subprocess.check_output(['uptime', '-p'], universal_newlines=True).strip()
        match = re.search(r"up (\d+) hours?, (\d+) minutes?", uptime)
        hours = int(match.group(1))
        minutes = int(match.group(2))
        uptime_formatted = "{:d}:{:02d}".format(hours, minutes)
        return uptime_formatted
    except:
        return "error"

# CPU information
def cpu():
    # Run the lscpu command and capture the output
    proc = subprocess.Popen(['lscpu'], stdout=subprocess.PIPE)
    output, error = proc.communicate()

    # Parse the output for the "Model name" field
    model_name = [line.split(':')[1].strip() for line in output.decode().strip().split('\n') if 'Model name' in line][0]
    num_cores = int([line.split(':')[1].strip() for line in output.decode().strip().split('\n') if 'CPU(s)' in line][0])
    return f'{model_name} ({num_cores})'

# GPU information
def gpu():
    # Assuming nvidia-smi is installed and available on the system
    try:
        gpu_info = subprocess.check_output(['nvidia-smi', '-L'], universal_newlines=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        gpu_info = "---"
    gpu_info = gpu_info.split(':')[1].split('(UUID')[0].strip()
    return gpu_info

# Screen resolution of all monitors
def screen_res():
    # Get a list of all monitors on the system
    monitors = screeninfo.get_monitors()
    return ', '.join([f'{i.width}x{i.height}' for i in screeninfo.get_monitors()])

def ram_load():
    # Get the system memory usage statistics
    mem_stats = psutil.virtual_memory()

    # Extract the used memory size in bytes
    used_memory = mem_stats.used
    total_memory = mem_stats.total

    # Convert the size to a human-readable format using psutil's utility function
    used_memory_str = psutil._common.bytes2human(used_memory)
    total_memory_str = psutil._common.bytes2human(total_memory)
    return f'{used_memory_str} / {total_memory_str}'
