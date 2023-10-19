from django.db import models

# Create your models here.
class NcsCodeInfo(models.Model):
    ncs_code = models.IntegerField(db_column='NCS_code', primary_key=True)  # Field name made lowercase.
    code1 = models.CharField(max_length=50, blank=True, null=True)
    code2 = models.CharField(max_length=50, blank=True, null=True)
    code3 = models.CharField(max_length=50, blank=True, null=True)
    code4 = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ncs_code_info'


class NcsJobname(models.Model):
    job_name = models.CharField(primary_key=True, max_length=30)
    ncs_code = models.ForeignKey(NcsCodeInfo, models.DO_NOTHING, db_column='NCS_code')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ncs_jobname'
        unique_together = (('job_name', 'ncs_code'),)

class Education(models.Model):
    no = models.AutoField(primary_key=True)
    ncs_code = models.ForeignKey('NcsCodeInfo', models.DO_NOTHING, db_column='NCS_code')  # Field name made lowercase.
    train_title = models.CharField(max_length=100, blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    train_center = models.ForeignKey('EducationCenter', models.DO_NOTHING, db_column='train_center')
    train_cost = models.IntegerField(blank=True, null=True)
    target_people = models.CharField(max_length=15, blank=True, null=True)
    quota = models.IntegerField(blank=True, null=True)
    link = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'education'


class EducationCenter(models.Model):
    train_center = models.CharField(primary_key=True, max_length=30)
    address = models.CharField(max_length=20)
    center_tel = models.CharField(max_length=13, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'education_center'
        unique_together = (('train_center', 'address'),)


class EmpInfo(models.Model):
    no = models.AutoField(primary_key=True)
    company = models.CharField(max_length=50, blank=True, null=True)
    job_name = models.CharField(max_length=30)
    city = models.CharField(max_length=10, blank=True, null=True)
    ncs_code = models.ForeignKey('NcsCodeInfo', models.DO_NOTHING, db_column='NCS_code')  # Field name made lowercase.
    stack = models.CharField(max_length=30, blank=True, null=True)
    link = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'emp_info'


class EmpPrediction(models.Model):
    no = models.AutoField(primary_key=True)
    date = models.IntegerField(blank=True, null=True)
    city = models.CharField(max_length=10, blank=True, null=True)
    industry = models.CharField(max_length=50, blank=True, null=True)
    job_offer = models.IntegerField(blank=True, null=True)
    job_search = models.IntegerField(blank=True, null=True)
    no_company = models.IntegerField(blank=True, null=True)
    unemployment = models.IntegerField(blank=True, null=True)
    population = models.IntegerField(blank=True, null=True)
    gdp = models.DecimalField(db_column='GDP', max_digits=8, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    i_rate = models.DecimalField(max_digits=8, decimal_places=0, blank=True, null=True)
    cli = models.DecimalField(db_column='CLI', max_digits=8, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    cfi = models.DecimalField(db_column='CFI', max_digits=8, decimal_places=0, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'emp_prediction'





class PredictionResult(models.Model):
    no = models.AutoField(primary_key=True)
    date = models.IntegerField(null=False)
    city = models.CharField(max_length=10, null=False)
    industry = models.CharField(max_length=50, null=False)
    result = models.DecimalField(max_digits=15, decimal_places=0, blank=True, null=True)
    user_id = models.CharField(max_length=300, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'prediction_result'