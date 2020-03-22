from django.db import models
from django.utils import timezone
from django.dispatch import receiver
import datetime, os
from django.contrib.postgres.fields import ArrayField, JSONField
from sorl.thumbnail import get_thumbnail

from io import BytesIO
from PIL import Image
from django.core.files import File


def compress(image):
    im = Image.open(image)
    # create a BytesIO object
    im_io = BytesIO() 
    # save image to BytesIO object
    im.save(im_io, 'JPEG', quality=70) 
    # create a django-friendly Files object
    new_image = File(im_io, name=image.name)
    return new_image

# Create your models here.
class Product(models.Model):
 
    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']

    title = models.CharField(max_length=200)
    price = models.FloatField()
    discount_price = models.FloatField()
    category = ArrayField(base_field=models.CharField(max_length=200), default=list)
    description = models.TextField()
    image = models.ImageField(upload_to='images/')
    
    @property
    def thumbnail(self):
        if self.image:
            return get_thumbnail(self.image, '350x350', quality=90)
        return None

    def save(self, *args, **kwargs):
        # call the compress function
        new_image = compress(self.image)
        # set self.image to new_image
        self.image = new_image
        # save
        super().save(*args, **kwargs)

    
class Order(models.Model):

    def __str__(self):
        return self.name
    class Meta:
        ordering = ['-created'] # latest to oldest

    items = JSONField(blank=True, default=dict)
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    address = models.CharField(max_length=1000)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    zipcode = models.CharField(max_length=200)
    total = models.CharField(max_length=200)

    created = models.DateTimeField(editable=False)
    modified = models.DateTimeField()

    def save(self, *args, **kwargs):
        #On save, update timestamps
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(Order, self).save(*args, **kwargs)

class Contact(models.Model):
    def __str__(self):
        return self.contact_email

    class Meta:
        ordering = ['-created'] # latest to oldest

    contact_email = models.EmailField(max_length=200)
    created = models.DateTimeField(editable=False)
    modified = models.DateTimeField()

    def save(self, *args, **kwargs):
        #On save, update timestamps
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(Contact, self).save(*args, **kwargs)

@receiver(models.signals.post_delete, sender=Product)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)

@receiver(models.signals.pre_save, sender=Product)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `MediaFile` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_file = Product.objects.get(pk=instance.pk).image
    except Product.DoesNotExist:
        return False

    new_file = instance.image
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)
