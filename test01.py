import requests
from datetime import datetime, timedelta
import json

BASE_URL_FB_API = "https://graph.facebook.com/v3.0"
ACCESS_TOKEN = "EAACEdEose0cBAJjz8LIxK6Kn3dgA8ngXT1sEvXq0fGx9bUOre5T1ZCQRvkWrB05hVvfwsr3fKFIcpLaEYujTLMnZBwmkFzxkmaI1JOa7CzpgHRV13OYr5nwuGsHSYZC8i5Afx6GeAJM4DAN3ApTaVCL0Bk6sZCl57axGfzBNTWKLvqhjHZCUIeiJ5nZCN0CdSRhIJBGavw9AZDZD"
LIMIT_REQUEST = 20
pagename = "chosun"
from_date = "2018-05-22"
to_date = "2018-05-23"

# url을 주면 json 리턴
def get_json_result(url):
    try:
        response = requests.get(url)

        if response.status_code == 200:
            return response.json()

    except Exception as e:
        return '%s : Error for request [%s]' % (datetime.now(), url)


# 페이스북 페이지 네임을 주면 페이지 id값을 리턴
def fb_name_to_id(pagename):

    base = BASE_URL_FB_API
    node = "/%s" % pagename
    params = "/?access_token=%s" % ACCESS_TOKEN
    url = base + node + params

    json_result = get_json_result(url)
    return json_result["id"]

# 페이스북 특정기간의 포스트를 json --> list형태로 가져오는 함수
def fb_get_post_list(pagename, from_date, to_date):
    page_id = fb_name_to_id(pagename)

    base = BASE_URL_FB_API
    node = "/%s/posts" % page_id
    fields = '/?fields=id,message,link,name,type,shares,' + \
             'created_time,comments.limit(0).summary(true),' + \
             'reactions.limit(0).summary(true)'
    duration = '&since=%s&until=%s' % (from_date, to_date)
    parameters = '&limit=%s&access_token=%s' % (LIMIT_REQUEST, ACCESS_TOKEN)

    url = base + node + fields + duration + parameters


    postList=[]

    isNext = True
    while isNext :
        tmpPostList = get_json_result(url)  # 포스트 정보를 딕션어리 형태로 리턴한다( data, paging)

        for post in tmpPostList["data"]:
            postVo = preprocess_post(post)
            postList.append(postVo)

        paging = tmpPostList.get("paging").get("next")
        # paging = tmpPostList["paging"][next]
        if paging != None:
            url = paging
        else:
            isNext = False

    # save results to file(json 형태로 파일 저장)
    with open("d:/javaStudy/facebook/" + pagename + ".json", 'w', encoding='utf-8') as outfile:
        json_string = json.dumps(postList, indent=4, sort_keys=True, ensure_ascii=False)
        outfile.write(json_string)

    return postList

# 원하는 데이터만을 취합하여 리턴
def preprocess_post(post):
    # 작성일 +9시간 해줘야 함
    created_time = post["created_time"]
    created_time = datetime.strptime(created_time, '%Y-%m-%dT%H:%M:%S+0000')
    created_time = created_time + timedelta(hours=+9)
    created_time = created_time.strftime('%Y-%m-%d %H:%M:%S')

    # 공유 수
    if "shares" not in post :
        shares_count = 0
    else :
        shares_count = post["shares"]["count"]

    # 리액션 수
    if "reactions" not in post :
        reactions_count = 0
    else :
        reactions_count = post["reactions"]["summary"]["total_count"]

    # 댓글 수
    if "comments" not in post :
        comments_count = 0
    else :
        comments_count = post["comments"]["summary"]["total_count"]

    # 메세지 수
    if "message" not in post :
        message_str = ""
    else :
        message_str = post["message"]

    postVo = {
        "shares_count": shares_count,
        "reactions_count": reactions_count,
        "comments_count": comments_count,
        "message_str": message_str,
        "created_time": created_time
    }

    return postVo

# url="http://192.168.1.14:8088/mysite4/api/gb/list2"
#
# result = get_json_result(url)
# print(result)

# result = fb_name_to_id("jtbcnews")
# print(result)

postList = fb_get_post_list(pagename,from_date,to_date)
for post in postList:
    print(post)

