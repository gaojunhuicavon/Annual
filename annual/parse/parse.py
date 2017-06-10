# coding:utf-8
from jieba import posseg as pseg


def _clear(content):
    """
    :param content :待清理表格的长文本
    :return :清理后的文本,返回字符串
    """
    t_symbol = [u'。', u'！', u'？', u'；', u'，']
    result = []
    lines = content.split('\n')
    for line in lines:
        line = line.strip()
        # L字符串长 s空格数量 n数字数量 p终止符
        count_dist = {'l': len(line) + 1.0, 's': line.count(' '), 'n': 0, 'p': 0}
        for n in line:
            if n.isdigit():
                count_dist['n'] += 1
            if n in t_symbol:
                count_dist['p'] += 1
        l, s, n, p = count_dist['l'], count_dist['s'], count_dist['n'], count_dist['p']
        if (n + s) / l >= 0.4 and p == 0 and count_dist['s'] != 0:
            continue
        elif n + 1 == l:
            result.append('\n')
            continue
        elif s >= 2 and p == 0:
            continue
        elif l <= 20 and p == 0:
            continue
        else:
            result.append(line)
    return result


def _format_result_with_tags(sent):
    result = ''
    for word, tag in sent:
        result += word + tag
    return result


def _format_result(sent):
    result = ''
    for word, tag in sent:
        result += word
    return result


def parse(content, with_tags=False):
    """
    :param content: 清理表格前的长文本
    :param with_tags: 返回的结果是否在体现句子主谓结构的词后添加词性标注
    :return: 句子列表
    """
    content = ''.join(_clear(content)).replace('\n', '')
    # 根据中文的句号，叹号，问号作为句子的终止符，尽可能地还原文章句子
    t_symbol = [u'。', u'！', u'？']
    result = []
    #  代表主语
    subject = ['n', 'nr', 'ns', 'nt', 'nz', 'r', '']
    #  代表谓语
    predicate = ['v', 'vd', 'vn']
    #  主谓结构
    sub_pres = []
    for sub in subject:
        for pre in predicate:
            sub_pres.append((sub, pre))
    start = 0
    format_func = _format_result_with_tags if with_tags else _format_result
    for index, item in enumerate(content):
        if item in t_symbol:
            sent = content[start:index + 1]
            start = index + 1
            token = list(pseg.cut(sent))
            for i in range(len(token) - 1):
                word, tag = token[i]
                next_word, next_tag = token[i + 1]
                if (tag, next_tag) in sub_pres:
                    sent = format_func(token)
                    result.append(sent)
                    break
    return result
