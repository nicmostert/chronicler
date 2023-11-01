"""Just testing some stuff here."""
# from annalist.annalist import FunctionLogger
from example_class import Craig

from annalist.annalist import Annalist

if __name__ == "__main__":
    ann = Annalist()
    ann.configure(
        logger_name="Let's make some Craigs",
        analyst_name="Nic Baby, Every Time",
    )
    ann2 = Annalist()

    cb = Craig("Beaven", 5.5, 9)
    print(cb)

    cb.grow_craig(1.5)
    cb.surname = "Coulomb"
    cb.shoesize = 11
    print(cb)
