# coding:utf-8

import string

numbers = set(string.digits + u'一二三四五六七八九十')
fuzzy_match = set(u'、（） ．.')


def check_title_similarity(title_a, title_b):
    """检查两个标题的是否有同类型的序号，如一、二和1、2"""
    return title_a.index_prefix == title_b.index_prefix and title_a.index_suffix == title_b.index_suffix and title_a.index_type == title_b.index_type


def recognize(title_objects, handled_lines=None):
    """
    识别其中的标题序列,按序排好
    :param title_objects: 候选的标题
    :param handled_lines: 已经记录过的标题的行号
    :return: 标题序列
    """
    handled_lines = handled_lines or set()

    # 候选集存放候选小标题
    candidate_set = []
    # 栈存放子标题，只考虑一级子标题
    stack = []
    for i, title_object in enumerate(title_objects):
        index = title_object.index
        title = title_object.raw_title
        line_number = title_object.line_number

        # 跳过已经处理过的标题
        if line_number in handled_lines:
            continue

        if candidate_set:

            # 与栈顶标号连续，压栈
            if stack and index == stack[-1].index + 1 and check_title_similarity(title_object, stack[-1]):
                stack.append(title_object)

            # 标号为1则进盏
            elif index == 1:
                stack.append(title_object)

            # 若与候选集连续, 则加入候选集并清空盏
            elif index == candidate_set[-1].index + 1 and check_title_similarity(candidate_set[-1], title_object):
                candidate_set.append(title_object)
                handled_lines.add(title_object.line_number)
                stack.clear()

            elif stack:
                if stack[-1].index > candidate_set[-1].index and check_title_similarity(stack[-1], candidate_set[-1]):
                    tmp_l = []
                    while stack:
                        titles = stack.pop()
                        if title.index == candidate_set[-1].index:
                            while tmp_l:
                                candidate_set.append(tmp_l.pop())
                            break
                        tmp_l.append(titles)
                stack.clear()

        elif index == 1:
            candidate_set.append(title_object)
            handled_lines.add(title_object.line_number)

    if candidate_set:
        candidate_set += recognize(title_objects, handled_lines)

    return candidate_set
