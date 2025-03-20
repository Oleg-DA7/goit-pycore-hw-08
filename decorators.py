from functools import wraps

def error_decorator(default_result=None):
    def decorator(func):
        @wraps(func)
        def inner(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except ValueError:
                print("Give me correct command please.")
                return default_result                
            except (KeyError, TypeError):             
                print("Enter the argument for the command")
            except (IndexError, AttributeError):            
                print("Item not found")
                return default_result
        return inner
    return decorator