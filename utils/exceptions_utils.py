
class NotFoundError(Exception):
    def __init__(self, message=''):
        super(NotFoundError, self).__init__(message)