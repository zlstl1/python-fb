import json
import re
from konlpy.tag import Twitter
from collections import Counter

# json 파일명, key 값을 주면 문자열을 리턴한다.

def json_to_str(filename, key):
    jsonfile = open(filename,'r',encoding='utf-8')
    json_string = jsonfile.read() # str type
    json_data = json.loads(json_string) # list type

    # print(type(json_string))
    # print(json_string)
    #
    # print(type(json_data))
    # print(json_data)

    data = ''
    for item in json_data:
        value = item.get(key)
        if value is None:
            continue

        data += re.sub(r'[^\w]','', value) # 한글만 계속 붙여나간다.

    return data

# 명사를 추출해서 빈도수를 알려줌
def count_wordfreq(data):
    twitter = Twitter()
    nouns = twitter.nouns(data)

    count = Counter(nouns)
    # print(count)
    return count
