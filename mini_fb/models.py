from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.db.models import Q

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

    def get_friends(self):
        friends1 = Friend.objects.filter(profile1=self)
        friends2 = Friend.objects.filter(profile2=self)
        friends3 = []

        for friend in friends1:
            friends3.append(friend.profile2)

        for friend in friends2:
            friends3.append(friend.profile1)

        return friends3

    def get_friend_suggestions(self):
        all_profiles = Profile.objects.exclude(pk=self.pk)
        friend_pks = [friend.pk for friend in self.get_friends()]

        return all_profiles.exclude(pk__in=friend_pks)
    def add_friend(self, other):
        if self == other:
            raise Exception("Adding yourself")
        friendship_exists = Friend.objects.filter((Q(profile1=self) & Q(profile2=other)) | (Q(profile1=other) & Q(profile2=self))).exists()

        if not friendship_exists:
            Friend.objects.create(profile1=self, profile2=other)
        else:
            return

    def get_news_feed(self):
        friends = self.get_friends()
        profiles = friends + [self]

        news_feed = StatusMessage.objects.filter(profile__in=profiles).order_by('-timestamp')
        return news_feed

class StatusMessage(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    message = models.CharField(max_length=500)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.timestamp} - {self.profile.first_name}: {self.message}"

    def get_images(self):
        return Image.objects.filter(status_message=self)

class Image(models.Model):
    image_file = models.ImageField(upload_to='images/')
    status_message = models.ForeignKey(StatusMessage, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.status_message} {self.timestamp}"

class Friend(models.Model):
    profile1 = models.ForeignKey(Profile, related_name='friend_profile1', on_delete=models.CASCADE)
    profile2 = models.ForeignKey(Profile, related_name='friend_profile2', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.profile1} & {self.profile2}"

