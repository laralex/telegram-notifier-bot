import inspect

def get_caller_function_name():
    frame = inspect.currentframe()
    caller_frame = frame.f_back
    if caller_frame is not None:
        return caller_frame.f_code.co_name
    return None