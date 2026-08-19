from django.db import models


class Skill(models.Model):

    name = models.CharField(max_length=100)

    category = models.CharField(max_length=100)

    proficiency = models.IntegerField(default=80)

    def __str__(self):
        return self.name

class Project(models.Model):

    title = models.CharField(max_length=200)

    description = models.TextField()

    technologies = models.CharField(max_length=300)

    github_url = models.URLField(blank=True)

    live_url = models.URLField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Profile(models.Model):

    name = models.CharField(max_length=100)

    role = models.CharField(max_length=150)

    short_bio = models.TextField()

    about = models.TextField()

    email = models.EmailField()

    phone = models.CharField(max_length=20, blank=True)

    location = models.CharField(max_length=100, blank=True)

    github_url = models.URLField(blank=True)

    linkedin_url = models.URLField(blank=True)

    resume_url = models.URLField(blank=True)

    def __str__(self):
        return self.name

class Experience(models.Model):

    job_title = models.CharField(max_length=150)

    company = models.CharField(max_length=150)

    start_date = models.DateField()

    end_date = models.DateField(blank=True, null=True)

    description = models.TextField()

    is_current = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.job_title} - {self.company}"

class Education(models.Model):

    degree = models.CharField(max_length=150)

    institution = models.CharField(max_length=200)

    start_year = models.IntegerField()

    end_year = models.IntegerField(blank=True, null=True)

    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.degree} - {self.institution}"

class ContactMessage(models.Model):

    name = models.CharField(max_length=100)

    email = models.EmailField()

    subject = models.CharField(max_length=200)

    message = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"           