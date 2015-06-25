from django.test import TestCase
from django.core.files import File

# Create your tests here.
from models import UserPhoto

class UserPhotoTests(TestCase):
    """UserPhoto model tests."""

    def test_photo_name(self):

        user_photo = UserPhoto(name='123')
        file = open("/home/zmenka/files/123.jpg")
        django_file = File(file)
        user_photo.photo.save("qwe.jpg", django_file, save=True)
        print(user_photo.photo.name, user_photo.photo.url)
        self.assertEquals(
            str(user_photo.name),
            u'123',
        )