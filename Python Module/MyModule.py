from collections import OrderedDict


def hellowWorld():
    return "hello world!"


def distinct(seq):
    return list(OrderedDict.fromkeys(seq))


def boolean_to_string(b):
    return str(b)


def snail(array):
    OUT = []
    while array:
        if array:
            for i in array.pop(0):
                OUT.append(i)
        if array:
            for i in array:
                OUT.append(i.pop(-1))
        if array:
            for i in array.pop(-1)[::-1]:
                OUT.append(i)
        if array:
            for i in array[::-1]:
                OUT.append(i.pop(0))
    return OUT