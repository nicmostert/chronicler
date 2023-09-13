from chronicler.chronicler import decorator_logger


@decorator_logger
def test_function(arg):
    return len(arg)

if __name__ == "__main__":
    ret = test_function("Hello")
