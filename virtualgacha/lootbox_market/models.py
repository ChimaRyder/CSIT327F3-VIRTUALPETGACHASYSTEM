from django.db import models
from inventory.models import Pet
from django.contrib.auth.models import User # Can be changed later if a custom User model is made, only foreign key is required
from login_register.models import Profile

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
    
    def get_10_cost(self):
        return self.rate_cost * 10

    def __str__(self):
        return self.lootbox_name
    
class LootboxDropTable(models.Model):
    lootbox_drop_table_id = models.AutoField(primary_key=True)
    lootbox_id = models.ForeignKey(Lootbox, on_delete=models.CASCADE)
    pet_id = models.ForeignKey(Pet, on_delete=models.CASCADE)


class Pull(models.Model):
    pull_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    roll_info = models.IntegerField()
    lootbox_id = models.ForeignKey(Lootbox, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

    def get_pulled_pets(self):
        return PullPet.objects.filter(pull_id=self.pull_id)

    def get_total_spent(self):
        return self.roll_info * self.lootbox_id.rate_cost
    
    def get_user_avatar(self):
        profile = Profile.objects.filter(user=self.user_id).first()
        return profile.get_profile_image_url()

    def __str__(self):
        return f'Pull {self.pull_id} by {self.user_id}'

class PullPet(models.Model):
    pull_pet_id = models.AutoField(primary_key=True)
    pull_id = models.ForeignKey(Pull, on_delete=models.CASCADE)
    pet_id = models.ForeignKey(Pet, on_delete=models.CASCADE)

    def __str__(self):
        return f'Pull {self.pull_id} - Pet {self.pet_id}'