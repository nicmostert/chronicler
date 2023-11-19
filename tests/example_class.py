"""Example of a class to be Annalized."""
from annalist.annalist import Annalist

annalizer = Annalist()


@annalizer.annalize
def return_greeting(name: str = "loneliness") -> str:
    """Return a friendly greeting."""
    return f"Hi {name}"


class Craig:
    """A standard issue Craig."""

    @annalizer.annalize
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
        self.height = height
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

    @surname.setter
    @annalizer.annalize
    def surname(self, value: str):
        """Set the surname of a Craig."""
        self._surname = value

    @property
    def shoesize(self):
        """The shoesize property."""
        return self._shoesize

    @shoesize.setter
    @annalizer.annalize(level="ERROR")
    def shoesize(self, value: int):
        """Set the shoesize of your Craig."""
        self._shoesize = value

    def grow_craig(self, feet: float):
        """Just a wrapper for the inner grow_craig."""

        @annalizer.annalize(
            message=f"{self.extra_info}",
            extra_info=self.extra_info,
        )
        def grow_craig(feet: float):
            """Grow your craig by specified amount of feet."""
            self.height += self.height + feet

        grow_craig(feet)

    @annalizer.annalize(message="Adding a message easily")
    def is_hurt_and_bearded(self) -> bool:
        """Return true if Craig is both injured and bearded."""
        return self.injured and self.bearded

    def __repr__(self) -> str:
        """Represent your Craig as a string."""
        return (
            f"Craig {self.surname} is {self.height} ft tall and wears "
            f"size {self.shoesize} shoes."
        )
