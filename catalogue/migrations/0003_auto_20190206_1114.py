# Generated by Django 2.1.5 on 2019-02-06 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0002_case'),
    ]

    operations = [
        migrations.AddField(
            model_name='case',
            name='contact_allowed',
            field=models.BooleanField(default=True, help_text='Are you happy to be contacted about this case?'),
        ),
        migrations.AlterField(
            model_name='disease',
            name='category',
            field=models.CharField(choices=[('Alcohol and drug misuse', 'Alcohol and drug misuse'), ('Blood and lymph', 'Blood and lymph'), ('Brain, nerves and spinal cord', 'Brain, nerves and spinal cord'), ('Cancer', 'Cancer'), ('Diabetes', 'Diabetes'), ('Ears, nose and throat', 'Ears, nose and throat'), ('Eyes', 'Eyes'), ('Glands', 'Glands'), ('Heart and blood vessels', 'Heart and blood vessels'), ('Immune system', 'Immune system'), ('Infections and poisoning', 'Infections and poisoning'), ('Injuries', 'Injuries'), ('Kidneys, bladder and prostate', 'Kidneys, bladder and prostate'), ('Lungs and airways', 'Lungs and airways'), ('Mental health', 'Mental health'), ('Mouth', 'Mouth'), ('Muscle, bone and joints', 'Muscle, bone and joints'), ('Nutritional', 'Nutritional'), ('Pregnancy and childbirth', 'Pregnancy and childbirth'), ('Sexual and reproductive', 'Sexual and reproductive'), ('Stomach, liver and gastrointestinal tract', 'Stomach, liver and gastrointestinal tract'), ('Not Known', 'Not Known')], default='Other', max_length=99),
        ),
    ]
