from django.test import TestCase
from .factories import BookFactory

# Create your tests here.

def generer_livres_factices(nb=20):
    livres = []
    for _ in range(nb):
        livre = BookFactory()
        livres.append(livre)
    print(f"{nb} livres générés avec succès !")
    return livres

if __name__ == "__main__":
    generer_livres_factices(20)
