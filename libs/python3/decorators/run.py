def log_calls(func):

    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__} with {args}, {kwargs}")
        result = func(*args, **kwargs)
        print(f"{func.__name__} returned {result}")
        return result
    
    return wrapper


# the following means, from now on, add() will look like:
# log_calls(add(a,b))

@log_calls
def add(a, b, type="complex"):
    return a + b



SUM=add(3, 4, type="complex")

print(f"sum= {SUM}")