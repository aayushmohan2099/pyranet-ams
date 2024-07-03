from django.db import migrations, models

def populate_initial_data(apps, schema_editor):
    Member = apps.get_model('mlm', 'Member')
    for member in Member.objects.all():
        member.full_name = "Default Name"
        member.component = "Default Component"
        member.base_sale_profit = 0.00
        member.personal_profit = 0.00
        member.profit_to_head = 0.00
        member.profit_from_members = 0.00
        member.phone_number = "Default Number"
        member.save()

class Migration(migrations.Migration):

    dependencies = [
        ('mlm', '0002_auto_20240703_1136.py'),
    ]

    operations = [
        migrations.RunPython(populate_initial_data),
    ]
