import codecs
from Node import Node
from NodeType import NodeType
from re import findall


def getType(string, char_set):
    if string.isdigit():
        return Node(NodeType["NUMERIC"], string)
    if 'ANY' == string:
        return Node(NodeType["STRING"], set([chr(char) for char in range(0, 256)]))
    if string.count('"') == 2:
        string = string.replace('\"', '')
        val = set([chr(ord(char)) for char in string])
        return Node(NodeType["STRING"], val)
    if string.count('\'') == 2:
        char = None
        if findall("'([^']*)'", string) and len(findall("'([^']*)'", string)) < 1:
            return str(findall("'([^']*)'", string)[0])
        try:
            char = codecs.decode(char, 'unicode_escape')
            ord_ = ord(char)
        except:
            raise Exception(f'char not in alphabet. Check: {string}')
        new_set = set(chr(ord_))
        return Node(NodeType["CHAR"], new_set)

    if 'CHR' in string:
        char = None
        if (
            char.find('(') != -1 and 
            char.find(')') != -1 and 
            char.count('(') == 1 and 
            char.count(')') == 1
            ):
            value = char[char.find('(')+1:char.find(')')]
        if value != None and value.isdigit():
            char = chr(int(value))
        return Node(NodeType["CHAR"], set(char ))
    
    try:
        return Node(NodeType["ID"], next(filter(lambda x: x.ident == string, char_set)).value, string)
    except StopIteration:
        pass