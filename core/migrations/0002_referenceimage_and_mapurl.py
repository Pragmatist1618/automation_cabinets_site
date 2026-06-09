# Generated manually for the starter project.
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="ReferenceImage",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("image", models.ImageField(upload_to="references/")),
                ("title", models.CharField(blank=True, max_length=180)),
                ("is_main", models.BooleanField(default=False)),
                ("order", models.PositiveIntegerField(default=0)),
                ("case", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="images", to="core.referencecase")),
            ],
            options={"ordering": ["-is_main", "order", "id"]},
        ),
    ]
