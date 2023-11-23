import inspect
import logging
from functools import partial

from annalist.annalist import Annalist

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)
logger.addHandler(logging.StreamHandler())

ann = Annalist()


class Wrapper:
    """Wrapper that triggers on __get__."""

    def __init__(self, func, message=None):
        """Call the init function of super.

        Also puts the called function on the namespace.
        """
        super().__init__()
        self.func = func

    def __call__(self, *args, **kwargs):
        """Triggers when func is a function."""
        logger.debug("CALLING FUNCTION.")
        return self.func(*args, **kwargs)

    def __call_method__(self, instance, *args, **kwargs):
        """Call from LoggingDecorator.__call_method__."""
        logger.debug("CALLING METHOD.")
        return self.func.__get__(instance)(*args, **kwargs)

    def __get_property__(self, instance, *args, **kwargs):
        """Call from LoggingDecorator.__get_property__."""
        logger.debug("GETTING PROPERTY.")
        return self.func.__get__(instance)(*args, **kwargs)

    def __set_property__(self, instance, *args, **kwargs):
        """Call from LoggingDecorator.__set_property__."""
        logger.debug("SETTING PROPERTY.")
        return self.func.__set__(instance)(*args, **kwargs)

    def __get__(self, instance, _):
        """Triggers when instance.method() is called."""
        logger.debug(f"GETTER CALLED on {self.func}")
        logger.debug(f"is it a property? {isinstance(self.func, property)}")
        if isinstance(self.func, property):
            return self.__get_property__(instance)
        else:
            return partial(self.__call_method__, instance)

    def __set__(self, instance, anything):
        """Triggers when setter is called."""
        logger.debug(f"SETTER CALLED on {self.func} with value {anything}")
        if isinstance(self.func, property):
            return self.__set_property__(instance, anything)
        return partial(self.__call_property__, instance)


class LoggingDecorator(Wrapper):
    """Logging Class."""

    def __call__(self, *args, **kwargs):
        """Triggers when a function is called.

        Logs, then sends to Wrapper.__call__.
        """
        logger.debug(f"FUNCTION CALLED {self.func}")
        logger.debug(
            f"You decorated a function called {self.func.__name__} "
            f"with args {args}, and kwargs {kwargs}"
        )
        ret_val = super().__call__(*args, **kwargs)
        logger.info(f"FUNCTION {self.func} takes args {args} and {kwargs}")
        logger.info(f"FUNCTION {self.func} RETURNS {ret_val}")
        return ret_val

    def __call_method__(self, instance, *args, **kwargs):
        """Triggers when a method is called (through __get__).

        Logs, then sends to Wrapper.__call_method__.
        """
        logger.debug("METHOD seen, let's get it.")
        logger.debug(
            f"You decorated a method called {self.func.__name__} "
            f"with instance {instance}, "
            f"args {args}, and kwargs {kwargs}"
        )
        ret_val = super().__call_method__(instance, *args, **kwargs)
        logger.info(f"METHOD {self.func} takes args {args} and {kwargs}")
        logger.info(f"METHOD {self.func} is on {instance}")
        logger.info(f"METHOD {self.func} RETURNS {ret_val}")

        message = (
            f"METHOD {self.func.__qualname__} takes "
            + f"args {args} and kwargs {kwargs}. "
            + f"It is on an instance of {instance.__class__.__name__}, "
            + f"and returns the value {ret_val}."
        )

        if hasattr(self.func, "__wrapped__"):
            ret_func = inspect.unwrap(self.func)
        else:
            ret_func = self.func

        logger.debug(self.func)
        # I'm unwrapping here in case the func is a
        # classmethod (which is a wrapper).
        fill_data = self._inspect_instance(ret_func, instance, args, kwargs)

        ann.log_call(
            message=message,
            level=ann.default_level,
            func=ret_func,
            ret_val=ret_val,
            extra_data=fill_data,
            args=args,
            kwargs=kwargs,
        )
        logger.debug("DONE LOGGING METHOD")
        return ret_val

    def __get_property__(self, instance):
        """Triggers when a property is called (through __get__).

        Logs, then sends to Wrapper.__call_property__
        """
        logger.debug("PROPERTY seen, let's get it.")
        logger.debug(
            f"You decorated a property called {self.func.fget} "
            f"on instance {instance}, "
        )
        value = self.func.fget(instance)
        logger.debug(f"PROPERTY IS {value}")
        return value

    def __set_property__(self, instance, value):
        """Triggers when a property setter is called.

        Logs, then sends to Wrapper.__set_property__
        """
        logger.debug("PROPERTY seen, let's SET it.")
        logger.debug(
            f"You decorated a property called {self.func.fset} "
            f"on instance {instance}, "
        )
        logger.debug("Constructing Message")

        logger.debug("inspecting instance")
        fill_data = self._inspect_instance(
            self.func.fset,
            instance,
            [],
            {},
            setter_value={self.func.fset.__name__: value},
        )
        message = (
            f"PROPERTY {self.func.fset.__qualname__} "
            + f"SET TO {value}. "
            + f"It is on an instance of {instance.__class__.__name__}."
        )
        ann.log_call(
            message=message,
            level=ann.default_level,
            func=self.func.fset,
            ret_val=None,
            extra_data=fill_data,
            args=value,
            kwargs=None,
        )

        logger.info(f"PROPERTY {self.func.fset} SET TO {value}")
        return self.func.fset(instance, value)

    @staticmethod
    def _inspect_instance(func, instance, args, kwargs, setter_value={}):
        arg_values = list(args) + list(kwargs.values())
        argspec = inspect.getfullargspec(func)

        if (len(argspec.args) > 0) and (argspec.args[0] == "self"):
            func_args = argspec.args[1:]
        else:
            func_args = argspec.args

        fill_data = {}

        if len(setter_value) != 0:
            if list(setter_value.keys())[0] in ann.all_attributes:
                fill_data = setter_value

        logger.debug(f"Function Arguments: {func_args}")
        logger.debug(f"Argument Values: {arg_values}")
        logger.debug(f"Looking for: {ann.all_attributes}")
        # if is_setter:
        #     if func.__name__ in ann.all_attributes:

        for attr in ann.all_attributes:
            if attr in fill_data:
                pass
            elif attr in func_args:
                logger.info(f"Found {attr} in method args.")
                fill_data[attr] = arg_values[func_args.index(attr)]
            elif hasattr(instance, attr):
                logger.info(f"Found {attr} in class attributes.")
                fill_data[attr] = getattr(instance, attr)
        logger.info(f"fill_data = {fill_data}")

        return fill_data
