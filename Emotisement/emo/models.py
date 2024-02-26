# Emotisement/models.py

from django.db import models

class Video(models.Model):
    title = models.TextField(default='Enter title')
    video_tags = models.TextField(default='no tags provided')  # Add video_tags field
    video_description = models.TextField(default='No description provided')  # Add video_description field
    video_file = models.FileField(upload_to='Emotisement/%y')

    def __str__(self):
        return self.title



class VideoEmotions(models.Model):
    video = models.ForeignKey('Video', on_delete=models.CASCADE)
    emotions_and_timestamp = models.JSONField(null=True)

    def __str__(self):
        return f"Emotions for {self.video.id}"
