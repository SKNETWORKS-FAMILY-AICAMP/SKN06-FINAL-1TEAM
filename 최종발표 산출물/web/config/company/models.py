from django.db import models

class CompanyList(models.Model):
    id = models.AutoField(primary_key=True)
    corp_code = models.CharField(max_length=8, null=True, blank=True)
    corp_name = models.CharField(max_length=50, null=True, blank=True)
    stock_name = models.CharField(max_length=100, null=True, blank=True)
    stock_code = models.CharField(max_length=6, null=True, blank=True)
    ceo_nm = models.CharField(max_length=50, null=True, blank=True)
    corp_cls = models.CharField(max_length=10, null=True, blank=True)
    jurir_no = models.CharField(max_length=50, null=True, blank=True)
    bizr_no = models.CharField(max_length=50, null=True, blank=True)
    adres = models.CharField(max_length=255, null=True, blank=True)
    hm_url = models.CharField(max_length=255, null=True, blank=True)
    ir_url = models.CharField(max_length=255, null=True, blank=True)
    phn_no = models.CharField(max_length=50, null=True, blank=True)
    fax_no = models.CharField(max_length=100, null=True, blank=True)
    induty_code = models.CharField(max_length=10, null=True, blank=True)
    est_dt = models.DateField(null=True, blank=True)
    acc_mt = models.CharField(max_length=50, null=True, blank=True)
    a = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'company_list'
        managed = False  # 기존 테이블이므로 Django가 스키마를 관리하지 않습니다.

    def __str__(self):
        return self.corp_name or ''
# 직원 정보 테이블
class CompanyWorker(models.Model):
    idx = models.AutoField(primary_key=True)
    corp_code = models.CharField(max_length=500, null=True, blank=True)
    report_no = models.CharField(max_length=500, null=True, blank=True)
    corp_name = models.CharField(max_length=500, null=True, blank=True)
    department = models.CharField(max_length=500, null=True, blank=True)
    gender = models.CharField(max_length=500, null=True, blank=True)
    full_time_employee = models.IntegerField(null=True, blank=True)
    contract_worker = models.IntegerField(null=True, blank=True)
    total_staff = models.IntegerField(null=True, blank=True)
    avg_tenure = models.CharField(max_length=500, null=True, blank=True)
    avg_salary_per_employee = models.CharField(max_length=500, null=True, blank=True)

    class Meta:
        db_table = 'company_worker'
        managed = False  # 기존 테이블을 사용하기 때문에 Django에서 관리하지 않음

    def __str__(self):
        return f"{self.corp_name} - {self.department}"

# 임원 정보 테이블
class CompanyExecutive(models.Model):
    idx = models.AutoField(primary_key=True)
    corp_code = models.CharField(max_length=500, null=True, blank=True)
    report_no = models.CharField(max_length=500, null=True, blank=True)
    corp_name = models.CharField(max_length=500, null=True, blank=True)
    name = models.CharField(max_length=500, null=True, blank=True)
    gender = models.CharField(max_length=500, null=True, blank=True)
    birth = models.CharField(max_length=500, null=True, blank=True)
    position = models.CharField(max_length=500, null=True, blank=True)
    job_role = models.CharField(max_length=500, null=True, blank=True)
    tenure = models.CharField(max_length=500, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    age_group = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'company_executive'
        managed = False

    def __str__(self):
        return f"{self.name} - {self.corp_name}"




class ConnectionBS(models.Model):
    idx = models.AutoField(primary_key=True)
    concept_id = models.CharField(max_length=255, blank=True, null=True)
    label_ko = models.CharField(max_length=255, blank=True, null=True)
    label_en = models.CharField(max_length=255, blank=True, null=True)
    class0 = models.CharField(max_length=255, blank=True, null=True)
    class1 = models.CharField(max_length=255, blank=True, null=True)
    class2 = models.CharField(max_length=255, blank=True, null=True)
    class3 = models.CharField(max_length=255, blank=True, null=True)
    class4 = models.CharField(max_length=255, blank=True, null=True)
    amount_2023 = models.DecimalField(
        max_digits=20, decimal_places=2, db_column='2023amount', blank=True, null=True
    )
    amount_2022 = models.DecimalField(
        max_digits=20, decimal_places=2, db_column='2022amount', blank=True, null=True
    )
    amount_2021 = models.DecimalField(
        max_digits=20, decimal_places=2, db_column='2021amount', blank=True, null=True
    )
    corp_code = models.CharField(max_length=20)

    class Meta:
        managed = False  # 이미 존재하는 테이블이므로 Django가 테이블을 관리하지 않음
        db_table = 'connection_bs'

class ConnectionCF(models.Model):
    idx = models.AutoField(primary_key=True)
    concept_id = models.CharField(max_length=255, blank=True, null=True)
    label_ko = models.CharField(max_length=255, blank=True, null=True)
    label_en = models.CharField(max_length=255, blank=True, null=True)
    class0 = models.CharField(max_length=255, blank=True, null=True)
    class1 = models.CharField(max_length=255, blank=True, null=True)
    class2 = models.CharField(max_length=255, blank=True, null=True)
    class3 = models.CharField(max_length=255, blank=True, null=True)
    class4 = models.CharField(max_length=255, blank=True, null=True)
    amount_2023 = models.DecimalField(
        max_digits=20, decimal_places=2, db_column='2023amount', blank=True, null=True
    )
    amount_2022 = models.DecimalField(
        max_digits=20, decimal_places=2, db_column='2022amount', blank=True, null=True
    )
    amount_2021 = models.DecimalField(
        max_digits=20, decimal_places=2, db_column='2021amount', blank=True, null=True
    )
    corp_code = models.CharField(max_length=20)

    class Meta:
        managed = False  # 이미 존재하는 테이블이므로 Django가 테이블을 관리하지 않음
        db_table = 'connection_cf'

class ConnectionCIS(models.Model):
    idx = models.AutoField(primary_key=True)
    concept_id = models.CharField(max_length=255, blank=True, null=True)
    label_ko = models.CharField(max_length=255, blank=True, null=True)
    label_en = models.CharField(max_length=255, blank=True, null=True)
    class0 = models.CharField(max_length=255, blank=True, null=True)
    class1 = models.CharField(max_length=255, blank=True, null=True)
    class2 = models.CharField(max_length=255, blank=True, null=True)
    class3 = models.CharField(max_length=255, blank=True, null=True)
    class4 = models.CharField(max_length=255, blank=True, null=True)
    amount_2023 = models.DecimalField(
        max_digits=20, decimal_places=2, db_column='2023amount', blank=True, null=True
    )
    amount_2022 = models.DecimalField(
        max_digits=20, decimal_places=2, db_column='2022amount', blank=True, null=True
    )
    amount_2021 = models.DecimalField(
        max_digits=20, decimal_places=2, db_column='2021amount', blank=True, null=True
    )
    corp_code = models.CharField(max_length=20)

    class Meta:
        managed = False  # 이미 존재하는 테이블이므로 Django가 테이블을 관리하지 않음
        db_table = 'connection_cis'

class ConnectionIS(models.Model):
    idx = models.AutoField(primary_key=True)
    concept_id = models.CharField(max_length=255, blank=True, null=True)
    label_ko = models.CharField(max_length=255, blank=True, null=True)
    label_en = models.CharField(max_length=255, blank=True, null=True)
    class0 = models.CharField(max_length=255, blank=True, null=True)
    class1 = models.CharField(max_length=255, blank=True, null=True)
    class2 = models.CharField(max_length=255, blank=True, null=True)
    class3 = models.CharField(max_length=255, blank=True, null=True)
    class4 = models.CharField(max_length=255, blank=True, null=True)
    amount_2023 = models.DecimalField(
        max_digits=20, decimal_places=2, db_column='2023amount', blank=True, null=True
    )
    amount_2022 = models.DecimalField(
        max_digits=20, decimal_places=2, db_column='2022amount', blank=True, null=True
    )
    amount_2021 = models.DecimalField(
        max_digits=20, decimal_places=2, db_column='2021amount', blank=True, null=True
    )
    corp_code = models.CharField(max_length=20)

    class Meta:
        managed = False  # 이미 존재하는 테이블이므로 Django가 테이블을 관리하지 않음
        db_table = 'connection_is'




class SingleBS(models.Model):
    idx = models.AutoField(primary_key=True)
    concept_id = models.CharField(max_length=255, blank=True, null=True)
    label_ko = models.CharField(max_length=255, blank=True, null=True)
    label_en = models.CharField(max_length=255, blank=True, null=True)
    class0 = models.CharField(max_length=255, blank=True, null=True)
    class1 = models.CharField(max_length=255, blank=True, null=True)
    class2 = models.CharField(max_length=255, blank=True, null=True)
    class3 = models.CharField(max_length=255, blank=True, null=True)
    class4 = models.CharField(max_length=255, blank=True, null=True)
    amount_2023 = models.DecimalField(
        max_digits=20, decimal_places=2, db_column='2023amount', blank=True, null=True
    )
    amount_2022 = models.DecimalField(
        max_digits=20, decimal_places=2, db_column='2022amount', blank=True, null=True
    )
    amount_2021 = models.DecimalField(
        max_digits=20, decimal_places=2, db_column='2021amount', blank=True, null=True
    )
    corp_code = models.CharField(max_length=20)

    class Meta:
        managed = False  # 이미 존재하는 테이블이므로 Django가 테이블을 관리하지 않음
        db_table = 'single_bs'

class SingleCF(models.Model):
    idx = models.AutoField(primary_key=True)
    concept_id = models.CharField(max_length=255, blank=True, null=True)
    label_ko = models.CharField(max_length=255, blank=True, null=True)
    label_en = models.CharField(max_length=255, blank=True, null=True)
    class0 = models.CharField(max_length=255, blank=True, null=True)
    class1 = models.CharField(max_length=255, blank=True, null=True)
    class2 = models.CharField(max_length=255, blank=True, null=True)
    class3 = models.CharField(max_length=255, blank=True, null=True)
    class4 = models.CharField(max_length=255, blank=True, null=True)
    amount_2023 = models.DecimalField(
        max_digits=20, decimal_places=2, db_column='2023amount', blank=True, null=True
    )
    amount_2022 = models.DecimalField(
        max_digits=20, decimal_places=2, db_column='2022amount', blank=True, null=True
    )
    amount_2021 = models.DecimalField(
        max_digits=20, decimal_places=2, db_column='2021amount', blank=True, null=True
    )
    corp_code = models.CharField(max_length=20)

    class Meta:
        managed = False  # 이미 존재하는 테이블이므로 Django가 테이블을 관리하지 않음
        db_table = 'single_cf'

class SingleCIS(models.Model):
    idx = models.AutoField(primary_key=True)
    concept_id = models.CharField(max_length=255, blank=True, null=True)
    label_ko = models.CharField(max_length=255, blank=True, null=True)
    label_en = models.CharField(max_length=255, blank=True, null=True)
    class0 = models.CharField(max_length=255, blank=True, null=True)
    class1 = models.CharField(max_length=255, blank=True, null=True)
    class2 = models.CharField(max_length=255, blank=True, null=True)
    class3 = models.CharField(max_length=255, blank=True, null=True)
    class4 = models.CharField(max_length=255, blank=True, null=True)
    amount_2023 = models.DecimalField(
        max_digits=20, decimal_places=2, db_column='2023amount', blank=True, null=True
    )
    amount_2022 = models.DecimalField(
        max_digits=20, decimal_places=2, db_column='2022amount', blank=True, null=True
    )
    amount_2021 = models.DecimalField(
        max_digits=20, decimal_places=2, db_column='2021amount', blank=True, null=True
    )
    corp_code = models.CharField(max_length=20)

    class Meta:
        managed = False  # 이미 존재하는 테이블이므로 Django가 테이블을 관리하지 않음
        db_table = 'single_cis'

class SingleIS(models.Model):
    idx = models.AutoField(primary_key=True)
    concept_id = models.CharField(max_length=255, blank=True, null=True)
    label_ko = models.CharField(max_length=255, blank=True, null=True)
    label_en = models.CharField(max_length=255, blank=True, null=True)
    class0 = models.CharField(max_length=255, blank=True, null=True)
    class1 = models.CharField(max_length=255, blank=True, null=True)
    class2 = models.CharField(max_length=255, blank=True, null=True)
    class3 = models.CharField(max_length=255, blank=True, null=True)
    class4 = models.CharField(max_length=255, blank=True, null=True)
    amount_2023 = models.DecimalField(
        max_digits=20, decimal_places=2, db_column='2023amount', blank=True, null=True
    )
    amount_2022 = models.DecimalField(
        max_digits=20, decimal_places=2, db_column='2022amount', blank=True, null=True
    )
    amount_2021 = models.DecimalField(
        max_digits=20, decimal_places=2, db_column='2021amount', blank=True, null=True
    )
    corp_code = models.CharField(max_length=20)

    class Meta:
        managed = False  # 이미 존재하는 테이블이므로 Django가 테이블을 관리하지 않음
        db_table = 'single_is'