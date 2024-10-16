from django.db import models
from inventory.models import Pet
from django.contrib.auth.models import User # Can be changed later if a custom User model is made, only foreign key is required


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
    
class LootboxDropTable(models.Model):
    lootbox_drop_table_id = models.AutoField(primary_key=True)
    lootbox_id = models.ForeignKey(Lootbox, on_delete=models.CASCADE)
    pet_id = models.ForeignKey(Pet, on_delete=models.CASCADE)

    
class LootboxHistory(models.Model):
    lootbox_history_id = models.AutoField(primary_key=True)
    lootbox_id = models.ForeignKey(Lootbox, on_delete=models.CASCADE)
    date_opened = models.DateField(auto_now_add=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    total_roll = models.IntegerField(default=1)
    obtained_pets = models.ManyToManyField(Pet, related_name='obtained_pets')

    def __str__(self):
        return f'{self.lootbox_id} - {self.date_opened}'


class Pull(models.Model):
    pull_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    roll_info = models.IntegerField()
    lootbox_id = models.ForeignKey(Lootbox, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Pull {self.pull_id} by {self.user_id}'

class PullPet(models.Model):
    pull_pet_id = models.AutoField(primary_key=True)
    pull_id = models.ForeignKey(Pull, on_delete=models.CASCADE)
    pet_id = models.ForeignKey(Pet, on_delete=models.CASCADE)

    def __str__(self):
        return f'Pull {self.pull_id} - Pet {self.pet_id}'