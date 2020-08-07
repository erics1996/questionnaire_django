from django.db import models


# Create your models here.
class ClassList(models.Model):
    """班级表"""
    name = models.CharField(max_length=32, verbose_name='班级名称')


class SurveyTemplate(models.Model):
    """问卷模板表"""
    name = models.CharField(max_length=64, verbose_name='班级名称')
    question = models.ManyToManyField('SurveyQuestion', verbose_name="多对多关联调查问卷问题表")
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加的时间')


class Survey(models.Model):
    """问卷调查表"""
    times = models.PositiveSmallIntegerField(verbose_name='第几次问卷调查')
    count = models.PositiveSmallIntegerField(verbose_name='生成多少个唯一码')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加的时间')
    grade = models.ForeignKey('ClassList', on_delete=models.CASCADE, verbose_name='外键关联班级表')
    survey_template = models.ForeignKey('SurveyTemplate', on_delete=models.CASCADE, verbose_name='外键关联的模板表')


class SurveyCode(models.Model):
    """唯一码表"""
    unique_code = models.CharField(max_length=10, unique=True, verbose_name='唯一码')
    is_used = models.BooleanField(default=False, verbose_name='是否已经被使用')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加的时间')
    survey = models.ForeignKey('Survey', on_delete=models.CASCADE, verbose_name='外键关联问卷调查表')


class SurveyQuestion(models.Model):
    """问卷问题表"""
    survey_type_choices = (('choice', '单选'), ('suggest', '建议'))
    survey_type = models.CharField(max_length=32, choices=survey_type_choices, verbose_name='问题的类型')
    name = models.CharField(max_length=64, verbose_name='问题的名称')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加的时间')


class SurveyChoice(models.Model):
    """问卷选项表"""
    name = models.CharField(max_length=32, verbose_name='选项的名称')
    score = models.PositiveSmallIntegerField(verbose_name='分值')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加的时间')
    question = models.ForeignKey('SurveyQuestion', on_delete=models.CASCADE, verbose_name="外键关联调查问卷问题表")


class SurveyRecord(models.Model):
    """问卷记录表"""
    # null是针对数据库而言，如果null=True, 表示数据库的该字段可以为空
    # blank=True，表示你的表单填写该字段的时候可以不填
    score = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name='得分')
    content = models.CharField(max_length=1024, null=True, blank=True, verbose_name='内容')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加的时间')
    question = models.ForeignKey('SurveyQuestion', models.CASCADE, verbose_name='外键关联问卷的问题表')
    survey_code = models.ForeignKey('SurveyCode', models.CASCADE, verbose_name='外键关联唯一码表')
    survey = models.ForeignKey('Survey', models.CASCADE, verbose_name='外键关联问卷调查表')
