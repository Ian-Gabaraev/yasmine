# Class for handling errors and exceptions.

class Error:
    def __init__(self, error_message):
        self.bot = None
        self.error_message = error_message
        self.master_id = None
        self.current_user_id = None

    def log(self):
        pass

    def view_error(self, hashcode):
        pass

    def notify_master(self):
        pass

    def notify_user(self):
        pass