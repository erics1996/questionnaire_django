from django.apps import AppConfig
from django.utils.module_loading import import_module


class AppConfig(AppConfig):
    name = 'app'

    def ready(self):
        """
        项目启动的过程中被运行两次
        :return:
        """
        # print(1)  # 打印2次，
        # from app.signals import app  # 不符合pep8规范，应该使用下面的方式
        import_module('app.signals.app')
