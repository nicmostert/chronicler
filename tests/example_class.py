"""Example of a class to be Annalized."""
from annalist.annalist import Annalist

annalizer = Annalist()


class Craig:
    """A standard issue Craig."""

    @annalizer.annalize
    def __init__(
        self,
        surname: str,
        height: float,
        shoesize: int,
    ):
        """Initialize a Craig."""
        self._surname = surname
        self.height = height
        self._shoesize = shoesize

    @property
    def surname(self):
        """The surname property."""
        return self._surname

    @surname.setter
    @annalizer.annalize
    def surname(self, value):
        """Set the surname of a Craig."""
        self._surname = value

    @property
    def shoesize(self):
        """The shoesize property."""
        return self._shoesize

    @shoesize.setter
    @annalizer.annalize
    def shoesize(self, value):
        """Set the shoesize of your Craig."""
        self._shoesize = value

    @annalizer.annalize
    def grow_craig(self, feet):
        """Grow your craig by specified amount of feet."""
        self.height = self.height + feet

    def __repr__(self):
        """Represent your Craig as a string."""
        return (
            f"Craig {self.surname} is {self.height} ft tall and wears "
            f"size {self.shoesize} shoes."
        )
