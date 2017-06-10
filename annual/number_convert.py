# coding:utf-8
chinese_numbers = {
    '零': 0,
    '一': 1,
    '二': 2,
    '三': 3,
    '四': 4,
    '五': 5,
    '六': 6,
    '七': 7,
    '八': 8,
    '九': 9,
    '十': 10,
    '百': 100,
    '千': 1000,
    '万': 10000,
    '亿': 100000000
}


def convert(s):
    """将中文数转换成阿拉伯数"""
    if len(s) > 1:
        pivot = 0
        for i, letter in enumerate(s):
            if convert(letter) > convert(s[pivot]):
                pivot = i
        value = convert(s[pivot])
        lhs = convert(s[:pivot])
        rhs = convert(s[pivot + 1:])
        if lhs > 0:
            value *= lhs
        value += rhs
        return value
    elif len(s) == 0:
        return 0
    return chinese_numbers[s]

if __name__ == '__main__':
    print(convert("三千五百六十一"))
    print(convert("零八"))
