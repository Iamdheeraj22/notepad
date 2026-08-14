class SystemService():
    def __init__(self):
        pass
    
    def getCurrentSystem(self):
        os_name = platform.system()
        return os_name