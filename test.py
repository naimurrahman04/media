import psutil

for process in psutil.process_iter():
    try:
        # Check if the process name contains 'python'
        if 'python' in process.name():
            print("Process is running in the background")
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        pass
