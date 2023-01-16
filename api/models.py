import requests
from django.db import models
from django.contrib.auth import get_user_model
from django.template.defaultfilters import slugify
import random  
import string
from django.core.files.base import ContentFile

class Country(models.Model):
    name = models.CharField(primary_key=True, max_length=255)
    population = models.IntegerField()


    def __str__(self):
        return self.name


class Review(models.Model):
    slug =  models.SlugField(primary_key=True, blank=True, unique=True)
    title = models.CharField(max_length=50, null=True, blank=True)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    image = models.ImageField(upload_to='country_images', null=True, blank=True)


    def __str__(self):
        return self.slug


    def save(self, *args, **kwargs): 
        if not self.slug:
            self.slug = self.unique_slug_generator(self)
        return super().save(*args, **kwargs)


    def random_string_generator(self, size = 10, chars = string.ascii_lowercase + string.digits): 
        return ''.join(random.choice(chars) for _ in range(size)) 


    def unique_slug_generator(self, instance, new_slug = None): 
        if new_slug is not None: 
            slug = new_slug 
        else: 
            slug = slugify(instance.title) 
        qs_exists = instance.__class__.objects.filter(slug = slug).exists() 
        if qs_exists: 
            new_slug = f'{slug}-{self.random_string_generator(size = 4)}'
                
            return self.unique_slug_generator(instance, new_slug = new_slug) 
        return slug 