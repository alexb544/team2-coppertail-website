from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_alter_profile_avatar'),
    ]

    operations = [
        migrations.AddField(
            model_name='dog',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='dog_images'),
        ),
    ]
