from app.exceptions.base import TodoListException

class ValidationException(TodoListException):
    pass

class BusinessRuleException(TodoListException):
    pass
