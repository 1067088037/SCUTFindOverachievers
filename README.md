# SCUTFindOverachievers

华南理工大学找到卷王 —— 基于 Python 的综测系统数据爬虫

## 需求背景

经过了一年时间的相处，想不想知道谁是你们班最卷的卷王？

在每年的综测期间，SCUT的学生信息管理系统会开放本学年同班级内所有人的成绩。

但逐一查看成绩显然是一个费时费力的工作，因此就有了这个自动化脚本。

## 配置方法

需要准备好 Python 环境，并且能够正常使用 python 和 pip 命令。

### 获取源码

```bash
git clone https://github.com/1067088037/SCUTFindOverachievers.git
```

或直接下载源码Zip

### 安装依赖

```bash
pip install urllib3 # 用于处理HTTP请求和响应
pip install lxml # 用于解析HTML数据
```

## 使用方法

建议配合 Google Chrome 浏览器完成操作。

### 登录官网

打开 http://xsgl.7i5q.cas.scut.edu.cn/sms2/homepage.jsp

使用统一认证登录，等待网页加载完成。

### 获取 Cookies

按下键盘上的 F12 进入调试器，将上方的标题栏切换到“网络”

![image-20220909083008901](.\assets\image-20220909083008901.png)

在左侧目录找到“智育测评”，并点击打开。

![image-20220909083125947](.\assets\image-20220909083125947.png)

可以看到调试器的内容发生了变化，找到名称为“intellectual_main.jsp”的项，选中打开。

![image-20220909083321701](.\assets\image-20220909083321701.png)

复制请求标头中的Cookies，不包括开头的“Cookies：”，从“JSEESIONID”开始复制。

![image-20220909083459785](.\assets\image-20220909083459785.png)

### 导入 Cookies

使用记事本或其它文本编辑软件打开源代码中的 config.py，将刚才复制的内容粘贴到 cookies 的一对单引号内。

![image-20220909083740362](.\assets\image-20220909083740362.png)

### 运行软件

```bash
python .\main.py
```

看到“连接成功，请稍后...”的提示文字后说明软件正常，等待数秒钟即可。

若出现“连接失败”，请检查 Cookies 是否正确复制或是否过期、网络是否连接。

### 数据处理

直接将显示出来的数据复制到 Excel 中任意单元格即可。