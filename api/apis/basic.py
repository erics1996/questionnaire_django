from rest_framework.generics import ListAPIView
from ..serializers import basic
from app import models
from rest_framework.response import Response


class SurveysApi(ListAPIView):
    """
    获取一组数据需要：model和序列化器。不需要写gey请求，视图的逻辑，ListAPIView都帮我们做了，这里为了返回指定的数据，重新写了一些视图逻辑！
    """
    queryset = models.Survey.objects.all()
    serializer_class = basic.SurveySerializer
    table_column = [
        {
            'prop': 'add_time',
            'label': '日期'
        },
        {
            'prop': 'count',
            'label': '唯一码数量'
        },
        {
            'prop': 'grade',
            'label': '班级'
        },
        {
            'prop': 'id',
            'label': '编号'
        },
        {
            'prop': 'survey_template',
            'label': '模板'
        },
        {
            'prop': 'times',
            'label': '次数'
        }
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
