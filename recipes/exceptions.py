class AlreadyExistsException(Exception):
    def __init__(self, cls):
        self.class_name = cls.__name__
