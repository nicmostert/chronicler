from annalist.annalist import decorator_logger


@decorator_logger
def test_function(arg):
    """
    Docstring
    """
    return len(arg)


if __name__ == "__main__":
    ret = test_function("Hello")
