# -*- coding: utf-8 -*-

import json

s = '{"list":[1, 2, 3, 4],\
        "string":"python 麦子学院",\
        "int":1,\
        "float":2.0,\
        "object":{},\
        "bool":true,\
        "null":null}'

j = json.loads(s, encoding = "utf-8")
for ele in j.values():
    print ele, type(ele)
    














# vim: set ts=4 sw=4 sts=4 tw=100 et:
