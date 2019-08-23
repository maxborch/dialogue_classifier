# Generated by Django 2.1.5 on 2019-01-30 17:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Case',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('patient_age', models.IntegerField(blank=True, null=True)),
                ('patient_comments', models.CharField(max_length=10000, null=True)),
                ('clinician_observations', models.CharField(max_length=10000, null=True)),
                ('ethnicity', models.CharField(choices=[('A: White - British', 'A: White - British'), ('B: White - Irish', 'B: White - Irish'), ('C: White - Any other White background', 'C: White - Any other White background'), ('D: Mixed - White and Black Caribbean', 'D: Mixed - White and Black Caribbean'), ('E: Mixed - White and Black African', 'E: Mixed - White and Black African'), ('F: Mixed - White and Asian', 'F: Mixed - White and Asian'), ('G: Mixed - Any other mixed background', 'G: Mixed - Any other mixed background'), ('H: Asian or Asian British - Indian', 'H: Asian or Asian British - Indian'), ('J: Asian or Asian British - Pakistani', 'J: Asian or Asian British - Pakistani'), ('K: Asian or Asian British - Bangladeshi', 'K: Asian or Asian British - Bangladeshi'), ('L: Asian or Asian British - Any other Asian background', 'L: Asian or Asian British - Any other Asian background'), ('M: Black or Black British - Caribbean', 'M: Black or Black British - Caribbean'), ('N: Black or Black British - African', 'N: Black or Black British - African'), ('P: Black or Black British - Any other Black background', 'P: Black or Black British - Any other Black background'), ('R: Other Ethnic Groups - Chinese', 'R: Other Ethnic Groups - Chinese'), ('S: Other Ethnic Groups - Any other ethnic group', 'S: Other Ethnic Groups - Any other ethnic group'), ('Z: Other Ethnic Groups - Not stated', 'Z: Other Ethnic Groups - Not stated')], default='Z: Other Ethnic Groups - Not stated', max_length=99)),
                ('gender', models.CharField(choices=[('0\t- Not Known', '0 - Not Known'), ('1\t- Male', '1\t- Male'), ('2\t- Female', '2 - Female'), ('9\t- Not Specified', '9 - Not Specified')], default='9 - Not Specified', max_length=99)),
                ('case_disease', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalogue.Disease')),
            ],
        ),
    ]