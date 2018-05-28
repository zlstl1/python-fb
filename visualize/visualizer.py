import matplotlib.pyplot as plt
from matplotlib import font_manager
import pytagcloud
import webbrowser

# matplotlib 그래프
def show_graph_bar(dictWords, pagename):

    # 한글처리
    font_filename = 'c:/Windows/fonts/malgun.ttf'
    font_name = font_manager.FontProperties(fname=font_filename).get_name()
    plt.rc('font', family=font_name)

    # 라벨처리(x축, y축, 눈금)
    plt.xlabel("주요단어")
    plt.ylabel("빈도수")
    plt.grid(True)

    # 데이터 대입
    dict_keys = dictWords.keys()
    dict_values = dictWords.values()

    plt.bar(range(len(dictWords)), dict_values, align='center')
    plt.xticks(range(len(dictWords)),list(dict_keys), rotation=70)

    # 그래프 이미지 저장
    save_filename = "D:/javaStudy/facebook/%s_bar_graph.png" % pagename
    plt.savefig(save_filename, dpi=400, bbox_inches='tight')

    # 그래프 팝업
    plt.show()


# 워드크라우드
def wordcloud(dictWords, pagename):
    taglist = pytagcloud.make_tags(dictWords.items(), maxsize=80)

    save_filename = "D:/javaStudy/facebook/%s_wordcloud.jpg" % pagename
    pytagcloud.create_tag_image(
        taglist,
        save_filename,
        size=(800, 600),
        fontname='korean',
        rectangular=False
    )
    webbrowser.open(save_filename)