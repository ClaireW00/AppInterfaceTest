# coding=utf8
import xlrd
import xlwt


# 打开Excel文件


def open_excel(file):
    try:
        data = xlrd.open_workbook(file)
        return data
    except Exception as e:
        print(str(e))


# 根据索引获取Excel表格中的数据，file：Excel文件路径，colnameindex:表头所在的行索引，by_index:表的索引,返回list
def read_excel_table_byindex(file, colnameindex=0, by_index=0):  # 默认第一行为表头
    data = open_excel(file)
    table = data.sheet_by_index(by_index)
    nrow = table.nrows  # 行数
    ncol = table.ncols  # 列数
    colname = table.row_values(colnameindex)  # 表列名
    testdata = []
    for r in range(colnameindex + 1, nrow):
        row = table.row_values(r)  # 取一行的值
        if row:
            kq = {}
            for c in range(ncol):
                if colname[c] != '':
                    if isinstance(row[c], float):  # 把浮点数转为字符串
                        kq[colname[c]] = str(int(row[c]))
                    else:
                        kq[colname[c]] = row[c]
        testdata.append(kq)
    return testdata


# 设置单元格样式
def set_style(name, height, bold=False):
    style = xlwt.XFStyle()  # 初始化样式
    font = xlwt.Font()  # 创建字体
    font.name = name
    font.bold = bold
    font.colour_index = 4
    font.height = height

    style.font = font
    return style


# 新建表格，写入Excel
def write_excel_table(file, data):  # data为list
    book = xlwt.Workbook(encoding='utf-8')
    sheet1 = book.add_sheet('test1', cell_overwrite_ok=True)
    nrow = len(data)  # list个数
    if nrow != 0:
        n = 0
        title = []
        for colname in data[0]:  # 写入表头
            sheet1.write(0, n, colname, set_style('Times New Roman', 220, True))
            title.append(colname)
            n += 1

        for row in range(nrow):  # 写入数据
            for key, value in data[row].items():
                j = 0
                while j < len(title):  # 将key与列表头title相同的值写入相应的列
                    if key == title[j]:
                        sheet1.write(row + 1, j, value)
                        break
                    j += 1

    book.save(file)  # 保存文件


if __name__ == '__main__':
    data = [{'姓名': 'lily', 'score': 100}, {'姓名': 'claire', 'score': 80}, {'score': 80, '姓名': 'lingling'}]
    # print(read_excel_table_byindex('E:\\test\\testcase1.xlsx'))
    write_excel_table('E:\\test\\002.xlsx', data)
