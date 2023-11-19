"""Just testing some stuff here."""
# from annalist.annalist import FunctionLogger
from annalist.annalist import Annalist
from tests.example_class import Craig

if __name__ == "__main__":
    ann = Annalist()
    ann.configure(
        analyst_name="Nic Baby, Every Time",
    )
    ann2 = Annalist()

    cb = Craig("Beaven", 5.5, 9)
    print(cb)

    cb.grow_craig(1.5)
    cb.surname = "Coulomb"
    cb.shoesize = 11
    print(cb)
