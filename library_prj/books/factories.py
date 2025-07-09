import io
import random
from factory import Faker, post_generation, SubFactory, RelatedFactoryList
from factory.django import DjangoModelFactory
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
from .models import Book, Category, Genre
from library_prj.authors.models import Author
from library_prj.publishers.models import Publisher


def fake_image(name="test.jpg", size=(200, 300), color=(155, 0, 0)):
    file = io.BytesIO()
    image = Image.new("RGB", size, color)
    image.save(file, "JPEG")
    file.seek(0)
    return SimpleUploadedFile(name, file.read(), content_type="image/jpeg")


class AuthorFactory(DjangoModelFactory):
    first_name = Faker("first_name")
    last_name = Faker("last_name")
    biography = Faker("paragraph")
    birth_date = Faker("date_of_birth")
    nationality = Faker("country")
    photo = Faker("file_name", category="image")

    @post_generation
    def photo(self, create, extracted, **kwargs):
        self.photo = fake_image(name=f"author_{self.first_name}_{self.last_name}.jpg")
        if create:
            self.save()

    class Meta:
        model = Author


class PublisherFactory(DjangoModelFactory):
    name = Faker("company")
    address = Faker("address")
    website = Faker("url")
    contact = Faker("name")

    class Meta:
        model = Publisher


class CategoryFactory(DjangoModelFactory):
    name = Faker("word")
    description = Faker("sentence")
    image = Faker("file_name", category="image")

    @post_generation
    def image(self, create, extracted, **kwargs):
        self.image = fake_image(name=f"category_{self.name}.jpg")
        if create:
            self.save()

    class Meta:
        model = Category


class GenreFactory(DjangoModelFactory):
    name = Faker("word")
    description = Faker("sentence")

    class Meta:
        model = Genre


class BookFactory(DjangoModelFactory):
    title = Faker("sentence", nb_words=4)
    summary = Faker("paragraph")
    isbn = Faker("isbn13")
    publication_date = Faker("date_this_century")
    pages = Faker("random_int", min=50, max=1000)
    language = Faker("language_name")
    stock = Faker("random_int", min=0, max=100)
    image = Faker("file_name", category="image")
    cover_front = Faker("file_name", category="image")
    cover_back = Faker("file_name", category="image")
    is_deleted = False
    price = 1000  # Valeur par défaut, à adapter si besoin
    format = Faker("word")
    dimensions = Faker("word")
    poids = Faker("pydecimal", left_digits=3, right_digits=2, positive=True)
    illustrateur = Faker("name")
    collection = Faker("word")
    niveau_scolaire = "universitaire"
    public_cible = random.choice([
        "génie logiciel",
        "télécommunicateur",
        "geii",
        "compta"
    ])
    editeur = SubFactory(PublisherFactory)

    @post_generation
    def auteurs(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for auteur in extracted:
                self.auteurs.add(auteur)
        else:
            self.auteurs.add(AuthorFactory())

    @post_generation
    def categories(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for cat in extracted:
                self.categories.add(cat)
        else:
            self.categories.add(CategoryFactory())

    @post_generation
    def genres(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for genre in extracted:
                self.genres.add(genre)
        else:
            self.genres.add(GenreFactory())

    @post_generation
    def image(self, create, extracted, **kwargs):
        self.image = fake_image(name=f"book_{self.title}_main.jpg")
        if create:
            self.save()

    @post_generation
    def cover_front(self, create, extracted, **kwargs):
        self.cover_front = fake_image(name=f"book_{self.title}_front.jpg")
        if create:
            self.save()

    @post_generation
    def cover_back(self, create, extracted, **kwargs):
        self.cover_back = fake_image(name=f"book_{self.title}_back.jpg")
        if create:
            self.save()

    class Meta:
        model = Book 