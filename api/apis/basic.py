from rest_framework.generics import ListAPIView
from ..serializers import basic
from app import models
from rest_framework.response import Response

"""从apiView可以知道rest_framework中的settings"""


class SurveysApi(ListAPIView):
    """
    获取一组数据需要：model和序列化器。不需要写gey请求，视图的逻辑，ListAPIView都帮我们做了，这里为了返回指定的数据，重新写了一些视图逻辑！
    """
    queryset = models.Survey.objects.all()
    serializer_class = basic.SurveySerializer
    table_column = [
        {
            'prop': 'grade',
            'label': '问卷调查的班级'
        },
        {
            'prop': 'times',
            'label': '第几次问卷调查'
        },
        {
            'prop': 'valid_count',
            'label': '填写人数'
        },
        {
            'prop': 'handle_link',
            'label': '填写链接'
        },
        {
            'prop': 'add_time',
            'label': '创建时间'
        },
        {
            'prop': 'handle',
            'label': '操作'
        },
    ]

    def list(self, request, *args, **kwargs):
        """
        重写父类的list方法
        :param request:http请求对象
        :param args:
        :param kwargs:
        :return:
        """
        # queryset = self.filter_queryset(self.get_queryset())  # self.get_queryset()返回一个queryset；filter_queryset：过滤queryset，返回的还是queryset；本质上就是调用self.queryset
        queryset = self.get_queryset()  # 不要用 queryset = self.queryset，虽然本质上是一样的，不能直接调用
        serializer = self.get_serializer(queryset, many=True)  # 本质上也就是调用序列化类做实例化
        # return Response(serializer.data)
        return Response({
            'code': 0,
            'data': {
                'table_column': self.table_column,
                'table_data': serializer.data,
            }
        })
