# coding:utf-8
import os
import re
import string

import Levenshtein

import annual.label_recognize as label_recognize
import annual.number_convert as number_convert
from annual.parse.parse import parse

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

chinese_numbers = set('零一二三四五六七八九十')
digit_numbers = set(string.digits)
fuzzy_match = set(u'、（） ．.')


class Title:
    CHINESE = 1
    DIGIT = 2

    def __init__(self, number_label, raw_title, real_title, line_number, index_prefix, index_suffix, index_type):
        self.index = number_label
        self.raw_title = raw_title
        self.real_title = real_title
        self.line_number = line_number
        self._index_prefix = None
        self._index_suffix = None
        self.index_prefix = index_prefix
        self.index_suffix = index_suffix
        self.index_type = index_type

    @property
    def index_prefix(self):
        return self._index_prefix

    @index_prefix.setter
    def index_prefix(self, value):
        self._index_prefix = Title.__standardize(value)

    @property
    def index_suffix(self):
        return self._index_suffix

    @index_suffix.setter
    def index_suffix(self, value):
        self._index_suffix = Title.__standardize(value)

    @staticmethod
    def __standardize(value):
        return value

    def __str__(self):
        return '<Title index:%s, raw_title: %s, line_number: %s>' % (self.index, self.raw_title[:10], self.line_number)


class Extractor:

    @staticmethod
    def _get_titles(content):
        titles = []
        for line_number, line in enumerate(content.splitlines()):
            if line_number == 614:
                pass
            line = line.strip()
            # 取小标题的前三个字符(unicode)与数字集做交集运算，有数字有可能是小标题
            start = line[:3]

            # 没有数字或者太短的行不是标题行
            index_type = None
            numbers = None
            start_set = set(start)
            if start_set & chinese_numbers:
                index_type = Title.CHINESE
                numbers = chinese_numbers
            elif start_set & digit_numbers:
                index_type = Title.DIGIT
                numbers = digit_numbers | {'.'}
            if not index_type or len(line) < 4:
                continue

            # 取出标号，遍历小标题的字符，取出第一个数字到不是数字为止
            index = []
            number_next = -1
            prefix = ''
            suffix = ''
            for i, char in enumerate(line):
                if char in numbers:
                    index.append(char)
                elif index and set(index) | {'.'} != set(index):
                    number_next = i
                    suffix += char
                    break
                else:
                    prefix += char
            # 数字后面2个字符以内没有分隔符说明不是小标题
            title = ''
            for i in range(number_next, min(len(line), number_next+3)):
                if line[i] in fuzzy_match:
                    title = line[i+1:]
                elif title:
                    break
            title = re.sub(r'[.…]+\d*$', '', title)
            if not title:
                continue

            index = ''.join(index).strip('.').split('.')[-1]

            # 汉字数转换成阿拉伯数
            if index[0] in chinese_numbers:
                index = number_convert.convert(index)

            index = int(index)

            if index >= 50:
                continue
            title_object = Title(index, line, title, line_number, prefix, suffix, index_type)
            titles.append(title_object)
        return titles

    @staticmethod
    def get_title_sequence(content):
        """提取年报中的标题序列"""
        titles = Extractor._get_titles(content)
        return label_recognize.recognize(titles)

    @staticmethod
    def get_guanliceng(content):
        """提取年报中管理层讨论与分析的内容"""
        content_list = content.splitlines()
        # 获取标题
        titles = Extractor.get_title_sequence(content)
        if not titles:
            return ''

        # 提取与"管理层讨论与分析"相似的标题
        min_distance = 10
        result = ''
        for i, title_obj in enumerate(titles):
            index, title, real_title = title_obj.index, title_obj.raw_title, title_obj.real_title
            real_title = ''.join(real_title.split())
            if not re.match('.*讨论与分析', title) and not re.match('.*讨论与分析', real_title):
                continue
            distance = Levenshtein.distance(real_title, '管理层讨论与分析')
            if distance < min_distance:
                if i + 1 < len(titles):
                    internal = content_list[title_obj.line_number+1: titles[i+1].line_number]
                else:
                    internal = content_list[title_obj.line_number+1:]
                internal = '\n'.join(internal).strip()
                if internal:
                    min_distance = distance
                    result = internal
        if result:
            return result

        # 提取与"董事会报告"相似的标题
        min_distance = 10
        for i, title_obj in enumerate(titles):
            index, title, real_title = title_obj.index, title_obj.raw_title, title_obj.real_title
            real_title = ''.join(real_title.split())
            if not re.match('.*董事.*报告', title) and not re.match('.*董事.*报告', real_title):
                continue
            distance = Levenshtein.distance(real_title, '董事会报告')
            if distance < min_distance:
                if i + 1 < len(titles):
                    next_title = titles[i+1]
                    internal = content_list[title_obj.line_number+1: next_title.line_number]
                else:
                    internal = content_list[title_obj.line_number:]
                internal = '\n'.join(internal).strip()
                if internal:
                    min_distance = distance
                    result = internal
        return result

    @staticmethod
    def get_complete_sentences(content, with_tags=False):
        """提取年报中的完整句子(即主谓结构的句子)"""
        return parse(content, with_tags)


if __name__ == '__main__':
    with open('data/2010txt/000001__2010_n.txt', encoding='utf-8') as f:
        content_ = f.read()
    Extractor.get_guanliceng(content_)
