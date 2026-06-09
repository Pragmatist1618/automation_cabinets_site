from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils.text import slugify

User = get_user_model()

class Service(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "title"]

    def __str__(self):
        return self.title


class ReferenceCase(models.Model):
    title = models.CharField(max_length=160)
    slug = models.SlugField(unique=True, blank=True)
    short_description = models.CharField(max_length=300)
    body = models.TextField(blank=True)
    client_name = models.CharField(max_length=160, blank=True)
    completion_date = models.DateField(null=True, blank=True)
    cover_image = models.ImageField(upload_to="references/", blank=True, null=True)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ["-completion_date", "title"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:150]
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("reference_detail", args=[self.slug])

    @property
    def main_image(self):
        first_main = self.images.filter(is_main=True).first()
        if first_main:
            return first_main.image
        first_image = self.images.first()
        if first_image:
            return first_image.image
        return self.cover_image

    def __str__(self):
        return self.title


class Project(models.Model):
    class Status(models.TextChoices):
        DRAFT = "draft", "Черновик"
        ACTIVE = "active", "Активный"
        DONE = "done", "Завершён"
        ARCHIVED = "archived", "Архив"

    title = models.CharField(max_length=160)
    slug = models.SlugField(unique=True, blank=True)
    customer_name = models.CharField(max_length=160, blank=True)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="owned_projects")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at", "title"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:150]
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("project_detail", args=[self.slug])

    def __str__(self):
        return self.title


class ProjectAccess(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="accesses")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="project_accesses")
    can_view_schemes = models.BooleanField(default=True)
    can_view_source = models.BooleanField(default=True)
    can_view_files = models.BooleanField(default=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [("project", "user")]

    def __str__(self):
        return f"{self.user} → {self.project}"


class ProjectFile(models.Model):
    class Category(models.TextChoices):
        SCHEME = "scheme", "Схема"
        SOURCE = "source", "Исходник"
        SPEC = "spec", "Спецификация"
        OTHER = "other", "Другое"

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="files")
    title = models.CharField(max_length=180)
    category = models.CharField(max_length=20, choices=Category.choices, default=Category.OTHER)
    file = models.FileField(upload_to="project_files/%Y/%m/")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["category", "title"]

    def __str__(self):
        return f"{self.project} / {self.title}"


class ContactMessage(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField()
    company = models.CharField(max_length=160, blank=True)
    phone = models.CharField(max_length=50, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_processed = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} — {self.email}"


class ReferenceImage(models.Model):
    case = models.ForeignKey(ReferenceCase, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="references/")
    title = models.CharField(max_length=180, blank=True)
    is_main = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["-is_main", "order", "id"]

    def save(self, *args, **kwargs):
        if self.is_main:
            ReferenceImage.objects.filter(case=self.case, is_main=True).exclude(pk=self.pk).update(is_main=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title or f"Image {self.pk}"
