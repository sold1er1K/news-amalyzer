from django.db import models

class News(models.Model):
    content = models.TextField()
    is_fake = models.BooleanField()
    probability = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"News: {self.content[:50]}... - Fake: {self.is_fake} - Probability: {self.probability}%"