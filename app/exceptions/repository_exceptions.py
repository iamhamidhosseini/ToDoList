from app.exceptions.base import TodoListException

class ProjectNotFoundException(TodoListException):
    pass

class TaskNotFoundException(TodoListException):
    pass

class DuplicateProjectException(TodoListException):
    pass

class DuplicateTaskException(TodoListException):
    pass

class LimitExceededException(TodoListException):
    pass


