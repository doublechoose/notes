环境：python3.5.2

安装xlrd：

```
pip install xlrd
```



由于需要将翻译（excel格式的）转为xml，Android的strings.xml，粗略写了一个：

```python
from xml.dom.minidom import Document
import xlrd

#打开excel 文件
workbook = xlrd.open_workbook('filename.xls')

#获取sheet
Data_sheet = workbook.sheets()[0]

namecols = Data_sheet.col_values(0) #获取id list
encols = Data_sheet.col_values(2) # 获取翻译 list

#xml doc
doc = Document()
resources = doc.createElement("resources")
doc.appendChild(resources)

for x in range(1,len(namecols)):
	st = doc.createElement("string")
	st.setAttribute("name",namecols[x])
	name = doc.createTextNode(encols[x])
	st.appendChild(name)
	resources.appendChild(st)

filename = "filename.xml"
f = open(filename, "w")
f.write(doc.toprettyxml(indent="  "))
f.close()
```

excel 里的内容是这样的：

| key     | 中文   | 英文      |
| ------- | ---- | ------- |
| barrage | 弹幕   | barrage |
| flash   | 闪    | flash   |
| shy     | 害羞   | shy     |
| wave    | 波浪   | wave    |
| pinyin  | 拼音   | pinyin  |
以上
