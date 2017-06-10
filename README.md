# Annual

公司年报内容一般均包含以下内容：

1. 重要提示
2. 公司基本情况
3. 会计数据和业务数据摘要
4. 股本变动及股东情况
5. 董事、监事和高级管理人员
6. 公司治理结构
7. 股东大会情况简介
8. 董事会报告
9. 监事会报告
10. 重要事项
11. 财务会计报告
12. 备查文件目录

Annual可用于自动识别、提取年报文本中的“董事会报告”章节中的“管理层讨论与分析”部分，
以及识别、提取年报中含有主谓结构的完整句子

## Installation
如果需要利用annual进行开发，请先使用setup.py进行安装
```
$ cd ${PATH_TO_Annual}
$ python setup.py install
```

## Command line tool
命令行工具为项目根目录下的command.py文件

1. 提取管理层讨论与分析章节
    ```
    $ python ${PATH_TO_Annual}/command.py -o output.txt exsec input.txt
    ```
2. 提取句子
    ```
    $ python ${PATH_TO_Annual}/command.py -o output.txt exsent input.txt
    ```
3. 提取标题序列
    ```
    $ python ${PATH_TO_Annual}/command.py -o output.txt exseq input.txt
    ```
4. 更详细的使用说明请看命令行工具提供的help
    ```
    $ python ${PATH_TO_Annual}/command.py -h
    ```

## Develops with Annual
1. Annual需要python3.5+，请确保系统中已经安装
2. 所需依赖均记录于requirements.txt文件，可使用以下命令安装依赖工具
    ```
    $ pip install -r requirements.txt
    ```

## API
Annual也提供了开发用的API

1. 获取年报中的标题序列
    ```
    from annual.extract import Extractor

    with open('annual.txt') as f:
        content = f.read()
    titles = Extractor.get_title_sequence(content)
    ```
2. 获取年报中的管理层讨论与分析的内容
    ```
    section = Extractor.get_guanliceng(content)
    ```
3. 获取年报中的完整句子
    ```
    sentences = Extractor.get_complete_sentences(content)
    ```
