# Generated manually for the starter project.
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import django.utils.text

class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Service",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=120)),
                ("description", models.TextField()),
                ("order", models.PositiveIntegerField(default=0)),
            ],
            options={"ordering": ["order", "title"]},
        ),
        migrations.CreateModel(
            name="ReferenceCase",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=160)),
                ("slug", models.SlugField(blank=True, unique=True)),
                ("short_description", models.CharField(max_length=300)),
                ("body", models.TextField(blank=True)),
                ("client_name", models.CharField(blank=True, max_length=160)),
                ("completion_date", models.DateField(blank=True, null=True)),
                ("cover_image", models.ImageField(blank=True, null=True, upload_to="references/")),
                ("is_published", models.BooleanField(default=True)),
            ],
            options={"ordering": ["-completion_date", "title"]},
        ),
        migrations.CreateModel(
            name="Project",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=160)),
                ("slug", models.SlugField(blank=True, unique=True)),
                ("customer_name", models.CharField(blank=True, max_length=160)),
                ("description", models.TextField(blank=True)),
                ("status", models.CharField(choices=[("draft", "Черновик"), ("active", "Активный"), ("done", "Завершён"), ("archived", "Архив")], default="active", max_length=20)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("owner", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="owned_projects", to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ["-updated_at", "title"]},
        ),
        migrations.CreateModel(
            name="ContactMessage",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=120)),
                ("email", models.EmailField(max_length=254)),
                ("company", models.CharField(blank=True, max_length=160)),
                ("phone", models.CharField(blank=True, max_length=50)),
                ("message", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("is_processed", models.BooleanField(default=False)),
            ],
            options={"ordering": ["-created_at"]},
        ),
        migrations.CreateModel(
            name="ProjectFile",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=180)),
                ("category", models.CharField(choices=[("scheme", "Схема"), ("source", "Исходник"), ("spec", "Спецификация"), ("other", "Другое")], default="other", max_length=20)),
                ("file", models.FileField(upload_to="project_files/%Y/%m/")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("project", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="files", to="core.project")),
            ],
            options={"ordering": ["category", "title"]},
        ),
        migrations.CreateModel(
            name="ProjectAccess",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("can_view_schemes", models.BooleanField(default=True)),
                ("can_view_source", models.BooleanField(default=True)),
                ("can_view_files", models.BooleanField(default=True)),
                ("active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("project", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="accesses", to="core.project")),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="project_accesses", to=settings.AUTH_USER_MODEL)),
            ],
            options={"unique_together": {("project", "user")}},
        ),
    ]
