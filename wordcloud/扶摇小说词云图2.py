import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import jieba
from wordcloud import WordCloud, ImageColorGenerator

#文件地址,默认程序和txt文件放在同一文件夹下
filename = "扶摇.txt"
txt = open(filename, "r", encoding="utf8", errors="ignore").read()

#停用词（可以用在jieba分词时，也可以使用在词云图作图时）
stopwords = ["一个", "一样", "那些", "起来", "早已", "然后", "知道", "便是", "今日", "这个", "像是", "身子", "如今","出去","居然","有点","只有","回来","身体","一句","别人","再次","动作","为了","之下","一只","一半", "这个","便是","倘若","突然","只是","不敢","他们","我们","见到","声音","心想","如此","只见","之中","不能","一个", "知道", "什么", "不想", "不是", "甚么", "一声", "咱们", "别人", "一句", "不知"]

#使用jieba分词
segmentDFs=[]
segs=jieba.cut(txt)
for seg in segs:
    if  len(seg) > 1:
        segmentDFs.append(seg)
segmentDF = pd.DataFrame({'segmentDFs': segmentDFs})
#print(segmentDF)

# 按文章进行词频统计
segStat_wc = segmentDF.groupby(by=['segmentDFs'])['segmentDFs'].agg({'计数': len}).reset_index().sort_values('计数',ascending=False)
#获取排序在前1000的词语
wc_dict=segStat_wc[:1000].set_index('segmentDFs').to_dict()


# 初始化自定义背景图片
bg_img = "fuyao.jpg" #注图片背景ps成白色
image = Image.open(bg_img)
graph = np.array(image)

# wordcloud配置
wc = WordCloud(
    font_path="simhei.ttf",  # 设置字体
    background_color='white',  # 背景颜色
    width=image.size[0],  # 设置宽，我这里设置和背景图片宽一样
    height=image.size[1],  # 设置高，我这里设置和背景图片高一样
    max_font_size=70, min_font_size=10,  # 字体最大/最小值
    stopwords=stopwords,  # 设置停用词，不在词云图中显示
    max_words=2000,  # 设置最大显示的字数
    mode='RGBA'
)
#有频数统计时，画词云图使用generate_from_frequencies函数，而只有明细数据时，使用generate
wc.generate_from_frequencies(wc_dict['计数'])
#wc.to_file(r"wordcloud1.png")

# 绘制文字的颜色以背景图颜色为参考
image_color = ImageColorGenerator(graph)  # 从背景图片生成颜色值
wc.recolor(color_func=image_color)
# 保存图片的名字
img_name = filename[:filename.rfind("."):] + "_词云图2" + ".png"
# 生成图片
wc.to_file(img_name)
# 4、显示图片
plt.figure("词云图")  # 指定所绘图名称
plt.imshow(wc)       # 以图片的形式显示词云
plt.axis("off")      # 关闭图像坐标系
plt.show()
