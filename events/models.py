from django.db import models
from django.db.models.signals import pre_save
from django.contrib.auth.models import User
from django.conf import settings
from django.urls import reverse
from django.dispatch import receiver
from django.template.defaultfilters import slugify
from django.core.validators import MaxValueValidator, MinValueValidator


class Connection(models.Model):
    user_id = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    following_user_id = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    class Meta:
        unique_together = ("user_id", "following_user_id")
        ordering = ["-created"]

    def __str__(self):
        return f"{self.user_id} is now following {self.following_user_id}"


class Tag(models.Model):
    name = models.CharField(max_length = 50)

    def __str__(self):
        return self.name


class Event(models.Model):
    STATUS = (('f', "Full"), ('e', "Expired"), ('a', "Active"), ('d', "Draft"),)

    name = models.CharField(max_length = 50)
    status = models.CharField(max_length=1, default='a', choices=STATUS)
    images = models.ImageField(null= True, blank = True)
    date = models.DateTimeField(null= True, blank = True)
    post_date = models.DateField(auto_now_add=True, null= True, blank = True)
    description = models.TextField(null= True, blank = True)
    location = models.CharField(max_length = 50, null= True, blank = True)
    max_capacity = models.PositiveIntegerField(null= True, blank = True)
    slug = models.SlugField(null= True, blank = True)
    is_public = models.BooleanField(default=True)
    is_free = models.BooleanField(default=True)
    price = models.FloatField(null= True, blank = True)
    remaining_tickets = models.PositiveIntegerField(null= True, blank = True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,
                    related_name='MyEvents', related_query_name ='organizer')
    tags = models.ManyToManyField(Tag, related_name='events')

    def __str__(self):
        return f"{self.id} - {self.name} - {self.created_by}"

    def get_absolute_url(self):
        return reverse('eventdetails', kwargs={'id':self.id})


class Reservation(models.Model):
    guest = models.ForeignKey(User, related_name= 'reservations', on_delete=models.CASCADE)
    event = models.ForeignKey(Event, related_name= 'reservations',on_delete=models.CASCADE)
    date = models.DateField(null= True, blank = True)
    num_tickets = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1),
                MaxValueValidator(5)], null= True, blank = True)
    reservation_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id} - {self.event} - {self.guest}"

def create_slug(instance, new_slug=None):
    slug = slugify(instance.name)
    if new_slug is not None:
        slug = new_slug
    qs = Event.objects.filter(slug=slug)
    if qs.exists():
        try:
            int(slug[-1])
            if "-" in slug:
                slug_list = slug.split("-")
                new_slug = "%s%s" % (slug[:-len(slug_list[-1])], int(slug_list[-1]) + 1)
            else:
                new_slug = "%s-1" % (slug)
        except:
            new_slug = "%s-1" % (slug)
        return create_slug(instance, new_slug=new_slug)
    return slug


@receiver(pre_save, sender=Event)
def generate_slug(instance, *args, **kwargs):
    if not instance.slug:
        instance.slug=create_slug(instance)
