from django.views.generic import TemplateView
import os
from django.conf import settings
from django.http.response import StreamingHttpResponse
from .. import models
import xlwt
from urllib.parse import quote


class IndexView(TemplateView):
    template_name = 'app/index.html'


class DownloadView(TemplateView):
    def get(self, request, *args, **kwargs):
        """
        下载报告的视图逻辑
        :param request:http请求对象
        :param args:
        :param kwargs:
        :return:
        """
        # print(kwargs.get('pk'))  # 获取url上传过来的数据
        """
        Tip：不要用其它only中的字段否则会再次执行sql
        survey加不加id都可以
        """
        codes = models.SurveyCode.objects.filter(survey=kwargs.get('pk')).only('unique_code')  # values和select也可以
        book = xlwt.Workbook()
        table = book.add_sheet('sheet1')
        table.write(0, 0, '唯一码')
        """
        print(
            codes)  # <QuerySet [<SurveyCode: SurveyCode object (1)>, <SurveyCode: SurveyCode object (2)>, <SurveyCode: SurveyCode object (3)>, <SurveyCode: SurveyCode object (4)>, <SurveyCode: SurveyCode object (5)>, <SurveyCode: SurveyCode object (6)>, <SurveyCode: SurveyCode object (7)>, <SurveyCode: SurveyCode object (8)>, <SurveyCode: SurveyCode object (9)>, <SurveyCode: SurveyCode object (10)>]>
        print(type(codes))  # <class 'django.db.models.query.QuerySet'>
        print(codes.iterator())  # <generator object QuerySet._iterator at 0x7f1ef3d465f0>
        """
        """
        enumerate()：函数用于将一个可遍历的数据对象(如列表、元组或字符串)组合为一个索引序列，同时列出数据和数据下标，一般用在for循环当中。
        enumerate(sequence, [start=0])
        sequence：一个序列、迭代器或其他支持迭代对象
        start：下标起始位置
        """
        for index, code in enumerate(codes.iterator(), 1):  # codes不使用iterator()也是可以的
            print(code, type(code))  # SurveyCode object (1) <class 'app.models.SurveyCode'>
            table.write(index, 0, code.unique_code)
        book.save('唯一码.xls')
        """
        for item in codes:
            print(item, type(item))  # SurveyCode object (1) <class 'app.models.SurveyCode'>
        """
        """
        print(settings)  # <Settings "questionnaire_django.settings">
        print(settings.BASE_DIR)  # 项目的绝对路径：/media/thanlon/存储盘/项目实施/开发/Django/questionnaire_django
        """

        # path = os.path.join(settings.BASE_DIR, '唯一码.xls')
        def iter_file(path, size=1024):
            with open(path, 'rb') as f:
                for data in iter(lambda: f.read(size), b''):
                    yield data

        path = os.path.join(settings.BASE_DIR, '唯一码.xls')
        response = StreamingHttpResponse(iter_file(path))
        # 文件内容响应类型，去掉也可以正常使用，最好加上
        response['Content-Type'] = 'application/octet-stream'
        # 内容描述
        response['Content-Disposition'] = 'attachment;{}'.format(
            "filename*=utf-8''{}".format(quote('唯一码.xls'))
        )
        """
        response['Content-Disposition'] = 'attachment;{}'.format(
            "filename={}".format(quote('唯一码.xls'))
        )
        """
        return response
