from django.test import TestCase


# Create your tests here.
def iter_file(path, size=1024):
    '''
    读取文件中的内容
    :param path:
    :param size:每次读取的字节数1024byte=1MB
    :return:
    '''
    with open(path, 'rb') as f:
        """
        print(f.read(size))
        print(type(f.read(size)))  # <class 'bytes'>
        print(iter(lambda: f.read(), b''))  # <callable_iterator object at 0x7f8109e235e0>
        """
        for data in iter(lambda: f.read(size), b''):
            yield data


# 测试读取文件中的内容的函数
path = '//media/thanlon/存储盘/项目实施/开发/Django/questionnaire_django/manage.py'
iter_file(path)
for row in iter_file(path):
    print(row)
