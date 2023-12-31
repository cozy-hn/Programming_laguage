from ctl_input import print_f
class Error_controller:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.warnings, self.errors = list(), list()
            self.initialized = True
    
    def print_error(self):
        if self.warnings or self.errors:
            for i in self.warnings:
                print_f(f"\033[93m(Warning): {i}\033[0m")
            for i in self.errors:
                print_f(f"\033[91m(Error): {i}\033[0m")
            self.warnings.clear()
            self.errors.clear()
        else:
            print_f("\033[92m(OK)\033[0m")

    
    def add_error(self, error):
        self.errors.append(error)
    
    def add_warning(self, warning):
        self.warnings.append(warning)