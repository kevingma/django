from django.db import models
from django.urls import reverse

class Profile(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    city = models.CharField(max_length=50)
    email_address = models.EmailField(unique=True)
    pfp_url = models.URLField(max_length=200)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_status_messages(self):
        return StatusMessage.objects.filter(profile=self).order_by('-timestamp')

    def get_absolute_url(self):
        return reverse('show_profile', kwargs={'pk': self.pk})

class StatusMessage(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    message = models.CharField(max_length=500)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.timestamp} - {self.profile.first_name}: {self.message}"