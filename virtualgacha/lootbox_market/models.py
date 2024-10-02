from django.db import models

# Create your models here.
class Lootbox(models.Model):
    class TaggedRelevance(models.TextChoices):
        POPULAR = 'popular', 'Popular'
        RECENT = 'recent', 'Recent'
        FEATURED = 'featured', 'Featured'

    lootbox_id = models.AutoField(primary_key=True)
    lootbox_name = models.CharField(max_length=255)
    rate_cost = models.IntegerField()
    date_created = models.DateField(auto_now_add=True)
    is_available = models.BooleanField(default=True)
    image = models.ImageField(upload_to='lootbox_images/', blank=True, null=True)
    tagged_relevance = models.CharField(
        max_length=10,
        choices=TaggedRelevance.choices,
        default=TaggedRelevance.RECENT,
    )

    def __str__(self):
        return self.lootbox_name