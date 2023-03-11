# step1:导入相关库

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
import re
from wordcloud import WordCloud
import warnings
warnings.filterwarnings('ignore')

# step2:加载数据集

data = pd.read_excel(r'taifeng.xlsx')      # 加载数据

# print(data.shape)      # 数据规格——输出：（715，7）

# step3:查看数据集

# print(data.tail(10))       # 查看后10行（查看前10行用head）

# step4:数据整理
data['省'] = data['登陆地点'].apply(lambda x: x[:2])
data['市'] = data['登陆地点'].apply(lambda x: x[3:6])
data['区县'] = data['登陆地点'].apply(lambda x: x[6:])

# 新建data_1
data_1 = data[['登陆时间','登陆强度','巅峰强度','省']].dropna()      #去掉data中的NaN
data_1['登陆等级'] = data_1['登陆强度'].apply(lambda x:int(re.match('\d+',str(x).split('，')[0]).group()))       #这边用了两次正则
data_1['巅峰等级'] = data_1['巅峰强度'].apply(lambda x:int(re.match('\d+',str(x).split('，')[0]).group()))
data_1['登陆年份'] = data_1['登陆时间'].apply(lambda x:x.year)
data_1['登陆月份'] = data_1['登陆时间'].apply(lambda x:x.month)

# step5:定义图像处理函数
def open():
    plt.ion()  # 打开交互模式
    plt.figure(figsize=(10,5))
    mngr = plt.get_current_fig_manager()  # 获取当前figure manager
    mngr.window.wm_geometry("+20+20")  # 调整窗口在屏幕上弹出的位置

def close():
    plt.show()
    plt.pause(3)  # 该句显示图片3秒
    plt.ioff()  # 显示完后一定要配合使用plt.ioff()关闭交互模式，否则可能出奇怪的问题
    plt.clf()  # 清空图片
    plt.close()  # 清空窗口

#step6:数据可视化分析

matplotlib.rcParams['font.family'] = 'SimHei'       # 使得图中的中文字符能够正常显示

# 各省台风等级分类散点图
open()
sns.swarmplot(x='省', y='登陆等级', data=data_1, palette='Set1')
plt.title('1945-2015 各省台风登陆等级分类散点图（点数多少代表台风数量）', size=20)
fig = plt.gcf()
fig.savefig('1945-2015 各省台风登陆等级分类散点图.jpg', dpi=1000, transparent=True, pad_inches=0, bbox_inches='tight')
close()

# 1945～2015每年登陆台风数量变化（折线图）
open()
year_counts = data['登陆时间'].apply(lambda x:x.year).value_counts().sort_index()
plt.plot(year_counts, lw=2)
plt.plot(year_counts, 'ro', color='b')
x = year_counts.index.tolist()
y_mean = [year_counts.mean()] * year_counts.shape[0]
plt.plot(x, y_mean, '--')
plt.xlabel('年份')
plt.ylabel('次数')
plt.rc('font', family='SimHei', size=18) 
plt.title('1945-2015 全国每年台风登陆数量', size=20)
plt.grid(c='y')
fig = plt.gcf()
fig.savefig('1945-2015 全国每年台风登陆数量.jpg', dpi=1000, transparent=True, pad_inches=0, bbox_inches='tight')
close()

# 台风登陆次数热力图（按月份—登陆等级）
open()
data_3 = data_1.groupby(['登陆月份', '登陆等级'], as_index=False)['登陆时间'].count()
data_3 = data_3.rename(columns={'登陆时间': '登陆次数'})
data_3_pivot = data_3.pivot('登陆等级', '登陆月份', '登陆次数')
sns.heatmap(data_3_pivot)
plt.title('1945-2015 全国台风登陆次数热力图（按月份-登陆等级）', size=20)
fig = plt.gcf()
fig.savefig('1945-2015 全国台风登陆次数热力图（按月份-登陆等级）.jpg', dpi=1000, transparent=True, pad_inches=0, bbox_inches='tight')
close()

# 台风登陆等级箱图
open()
sns.boxplot(x='登陆月份', y='登陆等级', data=data_3)
plt.title('1945-2015 全国台风登陆等级分布箱图', size=20)
fig = plt.gcf()
fig.savefig('1945-2015 全国台风登陆等级分布箱图.jpg', dpi=1000, transparent=True, pad_inches=0, bbox_inches='tight')
close()

# 台风登陆次数热力图（按月份—巅峰等级）
open()
data_2 = data_1.groupby(['登陆月份','巅峰等级'],as_index=False)['登陆时间'].count()
data_2 = data_2.rename(columns={'登陆时间':'登陆次数'})
data_2_pivot = data_2.pivot('巅峰等级','登陆月份','登陆次数')
sns.heatmap(data_2_pivot)
plt.title('1945-2015 全国台风登陆次数热力图（按月份-巅峰等级）', size=20)
fig = plt.gcf()
fig.savefig('1945-2015 全国台风登陆次数热力图（按月份-巅峰等级）.jpg', dpi=1000, transparent=True, pad_inches=0, bbox_inches='tight')
close()

# 台风巅峰等级箱图
open()
sns.boxplot(x='登陆月份', y='巅峰等级', data=data_2)
plt.title('1945-2015 全国台风巅峰等级箱图', size=20)
fig = plt.gcf()
fig.savefig('1945-2015 全国台风巅峰等级箱图.jpg', dpi=1000, transparent=True, pad_inches=0, bbox_inches='tight')
close()

# step7:台风登陆地点词云展示
 
# 词云展示 台风登陆的省份分布
words_1 = ','.join(data['省'].values.tolist())
open()
my_wordcloud_1 = WordCloud(
    background_color="white",   # 背景颜色
    max_words=20,  # 显示最大词数
    font_path='./fonts/simhei.ttf', # 显示中文
    min_font_size=5,
    max_font_size=100,
    width=500   # 图幅宽度
    ).generate(words_1)
plt.axis('off')
plt.imshow(my_wordcloud_1)
fig = plt.gcf()
fig.savefig('词云 省份.jpg', dpi=1200, transparent=True, pad_inches=0, bbox_inches='tight')
close()

# 词云展示 台风登陆的城市分布
words_2 = ','.join(data['市'].values.tolist())
open()
my_wordcloud_2 = WordCloud(background_color="white", max_words=20,font_path='./fonts/simhei.ttf', min_font_size=5, max_font_size=100,width=500).generate(words_2)
plt.axis('off')
plt.imshow(my_wordcloud_2)
fig = plt.gcf()
fig.savefig('词云 地级市.jpg', dpi=1200, transparent=True, pad_inches=0, bbox_inches='tight')
close()

# 词云展示 台风登陆的区县分布
words_3 = ','.join(data['区县'].values.tolist())
open()
my_wordcloud_3 = WordCloud(background_color="white", max_words=20,font_path='./fonts/simhei.ttf', min_font_size=5, max_font_size=100,width=500).generate(words_3)
plt.axis('off')
plt.imshow(my_wordcloud_3)
fig = plt.gcf()
fig.savefig('词云 区县.jpg', dpi=1200, transparent=True, pad_inches=0, bbox_inches='tight')
close()
