from rest_framework import serializers
from app import models


class SurveySerializer(serializers.ModelSerializer):
    """ModelSerializer类继承了Serializer，内部做了一些操作可以自动生成所有的字段"""

    class Meta:
        model = models.Survey
        # fields=('id',)
        fields = "__all__"