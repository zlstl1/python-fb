from collect import crawler
from analysis import analizer
from visualize import visualizer

# pagename = "jtbcnews"
pagename = "chosun"
from_date = "2018-10-30"
to_date = "2018-10-31"

if __name__ == "__main__":
    # 데이터 수집
    postList = crawler.fb_get_post_list(pagename,from_date,to_date)
    print(postList)

    # 데이터 분석(명사 개수)
    dataString = analizer.json_to_str("D:/javaStudy/facebook/jtbcnews.json", "message_str")
    count_data = analizer.count_wordfreq(dataString)
    print(count_data)
    dictWord = dict(count_data.most_common(20))

    # 데이터 시각화(그래프)
    visualizer.show_graph_bar(dictWord,pagename)
    visualizer.wordcloud(dictWord,pagename)