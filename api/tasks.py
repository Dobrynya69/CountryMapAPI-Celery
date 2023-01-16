import os
from celery import shared_task
from .models import *
from PIL import Image
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.core.files.temp import NamedTemporaryFile
import requests
from django.core.files import File
import io

@shared_task
def create_review(data, user_pk):
    country = Country.objects.get(pk=data['country'])
    user = get_user_model().objects.get(pk=user_pk)
    review = Review.objects.create(title=data['title'], text=data['text'], author=user, country=country)
    
    image_name = review.slug + '.jpeg'
    image_url = get_random_src(requests.get(url=f"https://api.pexels.com/v1/search?query={country.name}", headers={'Authorization': '563492ad6f91700001000001018f97a09de4429093e75a2b70f8cc60'}).json())
    image_response = requests.get(image_url)
    image = Image.open(io.BytesIO(image_response.content))
    image.save(image_name, format=image.format)
    
    with open(image_name, 'rb') as file:
        picture = File(file)
        review.image.save(image_name, picture, True)

    os.remove(image_name)


def get_random_src(json):
    lenght = len(json['photos'])
    rand_int = random.randint(0, lenght - 1)
    return json['photos'][rand_int]['src']['large']