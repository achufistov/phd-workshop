from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import date
import uuid

class UserProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    full_name = models.CharField(max_length=255, verbose_name="ФИО")
    passport_number = models.CharField(max_length=20)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    position = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    hire_date = models.DateField()
    address = models.TextField()
    phone_number = models.CharField(max_length=15)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    
    def __str__(self):
        return self.full_name

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(
            user=instance,
            full_name=f"{instance.first_name} {instance.last_name}".strip() or instance.username,
            passport_number="0000 000000",
            salary=0.00,
            position="Employee",
            department="General",
            hire_date=date.today(),
            address="Not specified",
            phone_number="+70000000000"
        )

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Post(models.Model):
    CATEGORY_CHOICES = [
        ('strategy', 'Стратегия развития'),
        ('innovation', 'Инновации'),
        ('culture', 'Корпоративная культура'),
        ('tech', 'Технологии'),
        ('news', 'Новости компании'),
    ]

    title = models.CharField(max_length=200)
    content = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'Comment by {self.author.username} on {self.post.title}'
