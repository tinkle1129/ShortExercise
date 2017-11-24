执行顺序：
包安装：
在文件路径下，输入
pip install -r requirements.txt

getstopwords.py (不用执行，加载停用词）
sentimentdict.py （不用执行，是把情感的词典加载进来）
PreProcessing.py 对原始数据进行处理，整理完存储到comments.csv中
display.py 生成词云
lda.py 对前10个热门歌手的热门歌曲计算lda，结果存储到song_lda.txt中
kmeans.py 从song_lda.txt中获取topics的内容，并对其进行k-means聚类，结果打印到控制台中