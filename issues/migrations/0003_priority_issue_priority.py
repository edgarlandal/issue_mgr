from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("issues", "0005_auto_20231004_0517"),
    ]

    operations = [
        migrations.CreateModel(
            name="Priority",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=128)),
                ("description", models.CharField(max_length=256)),
            ],
        ),
        migrations.AddField(
            model_name="issue",
            name="priority",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="issues.priority",
            ),
            preserve_default=False,
        ),
    ]
