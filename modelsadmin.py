from django.db import models

class Role(models.Model):
    user_role = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.user_role}"

class User(models.Model):
    username = models.CharField(max_length=64)
    password = models.CharField(max_length=64)
    email = models.EmailField()
    first = models.CharField(max_length=64)
    last = models.CharField(max_length=64)
    role = models.CharField(max_length=64)#models.ForeignKey(Role, on_delete=models.CASCADE, related_name="role")

    def __str__(self):
        return f"{self.username} ({self.first} {self.last})"
