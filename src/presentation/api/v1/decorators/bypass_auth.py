def bypass_auth():    
    def decorator(func):
        if not hasattr(func, "bypass_auth"):
            func.bypass_auth = True
        return func
    return decorator