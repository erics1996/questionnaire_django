from rest_framework import serializers

from app import models
from django.template import loader


class SurveySerializer(serializers.ModelSerializer):
    """ModelSerializer类继承了Serializer，内部做了一些操作可以自动生成所有的字段"""
    grade = serializers.CharField(source='grade.name')  # models.Survey.grade.name
    valid_count = serializers.SerializerMethodField()  # 自定义字段；以有下面的get_valid_count方法
    handle_link = serializers.SerializerMethodField()
    handle = serializers.SerializerMethodField()
    add_time = serializers.DateTimeField(format='%Y-%m-%d %X')
    """
    格式化时间，也可以使用自定义方法:
    def get_xxx(self, instance):
        return instance.add_time.strftime('%Y-%m-%d %X')
    """

    class Meta:
        model = models.Survey
        # fields = "__all__"
        """
        rest_framework中时间默认是'DATE_FORMAT': ISO_8601,需要进行格式化，在settings.py配置不能生效
        """
        fields = ('grade', 'times', 'valid_count', 'handle_link', 'add_time', 'handle')

    def get_valid_count(self, instance):
        """
        获取有效的填写人数
        :param instance:Survey实例
        :return:
        """
        # return instance.pk
        return models.SurveyCode.objects.filter(survey=instance, is_used=True).count()

    def get_handle_link(self, instance):
        """
        获取问卷的填写链接
        :param instance:Survey实例
        :return:
        """
        # return instance.pk
        """
        print(self.context)
        # 源码中返回context
        1、get_serializer
        def get_serializer(self, *args, **kwargs):
            serializer_class = self.get_serializer_class()
            kwargs['context'] = self.get_serializer_context()
            return serializer_class(*args, **kwargs) # 这里把context传到序列化器的类中，所以可以使用context属性，拿到request对象
        2、get_serializer_context
        def get_serializer_context(self):
            return {
                'request': self.request,
                'format': self.format_kwarg,
                'view': self
            }
        """
        request = self.context.get('request')  # 如果不调用get_serializer方法，需要自己去传
        return f"{request.scheme}://{request.get_host()}/{instance.pk}"

    def get_handle(self, instance):
        """
        获取操作
        :param instance:Survey实例
        :return:
        """
        # return """
        # <el-button size="mini" @click="handleEdit(scope.$index, scope.row)">查看报告</el-button>
        # <el-button size="mini" type="danger" @click="handleDelete(scope.$index, scope.row)">下载</el-button>
        # """
        # render的时候需要传入页面和context
        return loader.render_to_string(
            'app/components/handle.html',
            context={
                'report_link': '',
                'download_link': f'/{instance.pk}/download/'
            }
        )
