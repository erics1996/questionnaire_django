from django.dispatch import receiver
from django.db.models.signals import post_save
from .. import models
# 获取随机字符串（24位大小英文字母加数字的组合）
from django.utils.crypto import get_random_string


@receiver(post_save, sender=models.Survey)
def create_unique_code_handler(sender, **kwargs):
    print('接收信号')
    print(sender)
    print(kwargs)
    """
    接收信号
    <class 'app.models.Survey'>
    {
        'signal': <django.db.models.signals.ModelSignal object at 0x7fa44c1ba6d0>, 
        'instance': <Survey: Survey object (1)>,
        'created': True, 
        'update_fields': None, 
        'raw': False, 
        'using': 'default'
    }
    """
    created = kwargs.get('created', False)
    if not created:
        return
    instance = kwargs.get('instance')
    if not instance:
        return
    count = instance.count
    codes = []
    while count:
        _code = get_random_string(8)  # 生成八位随机码
        # 做预检
        if models.SurveyCode.objects.filter(unique_code=_code).exists():
            continue
        codes.append(models.SurveyCode(unique_code=_code, survey=instance))
        count -= 1
    # 批量创建
    models.SurveyCode.objects.bulk_create(codes)
