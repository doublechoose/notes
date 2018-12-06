# python 处理excel

**xlrd****模块**

使用步骤及方法：

**打开文件：**

import xlrd

excel=xlrd.open_workbook(*'E:/test.xlsx'*)

 

**获取sheet：**

table = excel.sheets()[0]       #通过索引获取  

table = excel.sheet_by_index(0)    #通过索引获取  

table = excel.sheet_by_name('Sheet1')   #通过表名获取  

 

备注：以下方法的操作都要在sheet基础上使用

**获取行数和列数**：

rows=table.nrows   #获取行数

cols=table.ncols    #获取列数

 

**获取单元格值：**

Data=table.cell(row,col).value  #获取表格内容，是从第一行第一列是从0开始的，注意不要丢掉 .value

 

**获取整行或整列内容**

Row_values=table.row_values(i)   #获取整行内容

Col_values=table.col_values(i)   #获取整列内容

 

**Openpyxl****模块**

 

**读**

**打开文件：**

from openpyxl import load_workbook

excel=load_workbook(*'E:/test.xlsx'*)

 

**获取sheet：**

table = excel.get_sheet_by_name('Sheet1')   #通过表名获取  

 

**获取行数和列数**：

rows=table.max_row   #获取行数

cols=table.max_column    #获取列数

 

**获取单元格值：**

Data=table.cell(row=row,column=col).value  #获取表格内容，是从第一行第一列是**从1开始**的，注意不要丢掉 .value

 

**写**

 

**#****打开文件**

excel=load_workbook(*'E:/test.xlsx'*)

sheet=excel.active

**#****设定单元格的值，两种方式**

sheet.cell(row=2,column=5).value=99

sheet.cell(row=3,column=5,value=100)

**#****保存修改的文件**

excel.save(*'E:/test.xlsx'*)



使用openpyxl

```
d = table.cell(row=2,column=5).value
d.strftime("%H:%M")

```

