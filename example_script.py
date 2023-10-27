from annalist.annalist import FunctionLogger

logger = FunctionLogger("Audit", "Nic Baby")


@logger.annalize
def test_function(arg):
    """
    Docstring
    """
    return len(arg)


if __name__ == "__main__":
    ret = test_function("Hello")
