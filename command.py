#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
from extract import Extractor

_EXTRACT_SECTION = 'exsec'
_EXTRACT_SENTENCE = 'exsent'
_EXTRACT_TITLE_SEQUENCE = 'exseq'

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='公司年报内容提取器，用于提取年报中的管理层讨论与分析的内容、标题序列以及具有主谓结构的完整句子')
    parser.add_argument('command', help='%s: 提取管理层讨论与分析内容; %s: 提取具有主谓结构的完整句子; %s: 提取所有标题序列' %
                                        (_EXTRACT_SECTION, _EXTRACT_SENTENCE, _EXTRACT_TITLE_SEQUENCE),
                        choices=[_EXTRACT_SECTION, _EXTRACT_SENTENCE, _EXTRACT_TITLE_SEQUENCE])
    parser.add_argument('-t', '--with_tags', help='抽取句子时是否在关键词后添加词性标注', action='store_true')
    parser.add_argument('-o', '--output', help='提取后的内容的存放路径，若空则输出到显示屏')
    parser.add_argument('input', help='需要提取管理层讨论与分析内容的年报文本路径')
    args = parser.parse_args()

    # input
    with open(args.input, encoding='utf-8') as f:
        content = f.read()

    # extract
    if args.command == _EXTRACT_SECTION:
        result = Extractor.get_guanliceng(content)
    elif args.command == _EXTRACT_TITLE_SEQUENCE:
        result = Extractor.get_title_sequence(content)
        result = '\n'.join([each.raw_title for each in result])
    else:
        result = Extractor.get_complete_sentences(content, args.with_tags is True)
        result = ('\n' + '*' * 100 + '\n').join(result)

    # output
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(result)
    else:
        print(result)
