# 操作excel写内容
import xlwt

# 创建一个excel对象
book = xlwt.Workbook()
# 添加一个表格
table = book.add_sheet('sheet1')
# 根据行和列添加数据
table.write(0, 0, 'Erics')  # 第一行第一列
table.write(0, 1, 'Kiku')  # 第一行第二列
table.write(0, 2, 'Liki')  # 第一行第三列
table.write(0, 3, 'Kili')  # 第一行第四列
table.write(1, 0, 'Erics')  # 第二行第一列
table.write(1, 1, 'Kiku')  # 第二行第二列
table.write(1, 2, 'Liki')  # 第二行第三列
table.write(1, 3, 'Kili')  # 第二行第四列
# 保存文件
book.save('name.xls')
"""
    A    B     C     D
Erics	Kiku	Liki	Kili
Erics	Kiku	Liki	Kili
"""
