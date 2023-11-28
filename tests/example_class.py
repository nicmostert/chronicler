"""Example of a class to be Annalized."""
# from annalist.annalist import Annalist, MethodDecorator
from annalist.annalist import Annalist
from annalist.decorators import ClassLogger, function_logger

ann = Annalist()

extra_info = {"injured": "Yessir."}


@function_logger(message="Just saying hi.", extra_info=extra_info)
def return_greeting(name: str = "loneliness") -> str:
    """Return a friendly greeting."""
    return f"Hi {name}"


def which_craig_is_that(sits: str = "left") -> str:
    """Which craig based on seat."""
    if sits == "left":
        return "Beaven"
    else:
        return "Coulomb"


class Craig:
    """A standard issue Craig."""

    @ClassLogger  # type: ignore
    def __init__(
        self,
        surname: str,
        height: float,
        shoesize: int,
        injured: bool,
        bearded: bool,
    ):
        """Initialize a Craig."""
        self._surname = surname
        self._height = height
        self._shoesize = shoesize
        self.injured = injured
        self.bearded = bearded
        self.extra_info = {
            "injured": self.injured,
            "bearded": self.bearded,
        }

    @property
    def surname(self):
        """The surname property."""
        return self._surname

    @ClassLogger  # type: ignore
    @surname.setter
    def surname(self, value: str):
        """Set the surname of a Craig."""
        self._surname = value

    @property
    def shoesize(self):
        """The shoesize property."""
        return self._shoesize

    @ClassLogger  # type: ignore
    @shoesize.setter
    def shoesize(self, value: int):
        """Set the shoesize of your Craig."""
        self._shoesize = value

    @property
    def height(self):
        """The height property."""
        return self._height

    @ClassLogger  # type: ignore
    @height.setter
    def height(self, value):
        self._height = value

    @ClassLogger
    def grow_craig(self, feet: float):
        """Grow your craig by specified amount of feet."""
        self.height = self.height + feet  # type: ignore

    @ClassLogger
    def is_hurt_and_bearded(self) -> bool:
        """Return true if Craig is both injured and bearded."""
        return self.injured and self.bearded

    # This one has an input arg with the same name as a class attr.
    @ClassLogger
    def measure_the_craig(self, height: float | None = None) -> float:
        """Return true if Craig is both injured and bearded."""
        if height is None:
            return self.height
        else:
            return height

    @ClassLogger
    @staticmethod
    def what_is_a_craig():
        """Explain a craig."""
        return "They sit next to me."

    @ClassLogger
    @classmethod
    def army_of_craigs(cls, surnames: list):
        """Make an army of tall, healthy, shaven craigs."""
        army = []
        for surn in surnames:
            new_craig = cls(
                surname=surn,
                height=6.9,
                shoesize=11,
                injured=False,
                bearded=False,
            )
            army += [new_craig]

        return army

    # def __repr__(self) -> str:
    #     """Represent your Craig as a string."""
    #     return (
    #         f"Craig {self.surname} is {self.height} ft tall and wears "
    #         f"size {self.shoesize} shoes."
    #     )
