from rest_framework.generics import ListAPIView
from ..serializers import basic
from app import models
from rest_framework.response import Response
from rest_framework import filters
from rest_framework import pagination

"""从apiView可以知道rest_framework中的settings"""


class CustomFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, qs, view):
        """
        自定义的过滤器
        :param request:
        :param qs:
        :param view:
        :return:
        """
        return qs


class SurveysApi(ListAPIView):
    """
    获取一组数据需要：model和序列化器。不需要写gey请求，视图的逻辑，ListAPIView都帮我们做了，这里为了返回指定的数据，重新写了一些视图逻辑！
    重点：如果是自定义的字段，如grade__name，需要针对结果排序（OrderingFilter会自动根据非自定义字段排序）而不是针对queryset排序，自定义字段的排序需要通过结果来排序，如果是自定义排序会走自定义的方法
    """
    queryset = models.Survey.objects.all()
    serializer_class = basic.SurveySerializer
    # 过滤器
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, CustomFilter, ]  # 元组和列表都可以
    # 过滤字段。配合filters.SearchFilter使用，如果想要支持更多的字段搜索，添加字段名称即可
    search_fields = ['grade__name', ]
    # 过滤字段。配合filters.OrderingFilter，如果想要支持更多的字段搜索，添加字段名称即可
    ordering_fields = ['grade__name']
    # 分页器
    pagination_class = pagination.LimitOffsetPagination
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
        # queryset = self.get_queryset()  # 不要用 queryset = self.queryset，虽然本质上是一样的，不能直接调用
        queryset = self.filter_queryset(self.get_queryset())
        # 帮助我们实现分页
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)  # serializer.data是分页后的数据
        serializer = self.get_serializer(queryset, many=True)  # 本质上也就是调用序列化类做实例化
        # return Response(serializer.data)
        return Response({
            'code': 0,
            'data': {
                'table_column': self.table_column,
                'table_data': serializer.data,
            }
        })

    def get_paginated_response(self, data):
        """
        自定义分页返回的数据
        :param data: serializer.data
        :return:
        """
        print(data)
        """
        OrderedDict：有序的字典，通过双向链表实现，字典在3.6之前是无序的
        [OrderedDict([('grade', '计算机技术'), ('times', 1), ('valid_count', 0), ('handle_link', 'http://localhost:8000/1'), ('add_time', '2020-08-07 09:03:04'), ('handle', '<el-button size="mini" @click="handleEdit(scope.$index, scope.row)">\n    <a class="btn btn-primary" href="">查看报告</a>\n</el-button>\n<el-button size="mini" type="danger" @click="handleDelete(scope.$index, scope.row)">\n    <a class="btn btn-danger" href="">下载</a>\n</el-button>')]), OrderedDict([('grade', '网络工程'), ('times', 2), ('valid_count', 0), ('handle_link', 'http://localhost:8000/2'), ('add_time', '2020-08-07 09:30:45'), ('handle', '<el-button size="mini" @click="handleEdit(scope.$index, scope.row)">\n    <a class="btn btn-primary" href="">查看报告</a>\n</el-button>\n<el-button size="mini" type="danger" @click="handleDelete(scope.$index, scope.row)">\n    <a class="btn btn-danger" href="">下载</a>\n</el-button>')])]
        """
        ordering = self.request.query_params.get('ordering',
                                                 '')  # request.query_params获取所有参数，转换为字典,http://127.0.0.1:8000/api/surveys/?limit=2&search=&offset=1&ordering=
        reverse = False
        if ordering:
            if ordering.startwith('-'):
                reverse = True
                ordering = ordering[1:]
            data.sort(key=lambda item: item[ordering], reverse=reverse)

        return Response({
            'code': 0,
            'data': {
                'table_column': self.table_column,
                'table_data': {
                    'data': data,
                    'total': self.paginator.count
                },
            }
        })
