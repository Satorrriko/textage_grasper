# read html file and get table
import bs4
import re
import pandas as pd
import numpy as np
import random
 
class fumen():
    def __init__(self):
        self.data = pd.DataFrame()
        self.song_info = ''
        self.note_map = {
            "0": 0,
            "2": 0,
            "37": 1,
            "38": 1,
            "51": 2,
            "52": 2,
            "65": 3,
            "66": 3,
            "79": 4,
            "80": 4,
            "93": 5,
            "94": 5,
            "107": 6,
            "108": 6,
            "121": 7,
            "122": 7
        }
    def read(self, file_path):
        read_file = open(file_path, 'r', encoding='utf-8')
        soup = bs4.BeautifulSoup(read_file, 'html.parser', from_encoding='utf-8')

        # get song name and artist
        self.song_info = soup.find_all('nobr')[0].text
        soup_table = soup.find_all('table')


        for table in soup_table[1:]: # 第一张表是原表
            # print(len(table.find_all('tr')))
            for tr in table.find_all('tr'):
                reg = re.compile(r'height:(\d+)px')
                pic_height = reg.findall(tr.find('div').get('style'))[0]
                pic_height = int(pic_height)
                df = pd.DataFrame(np.zeros((128, 10)), dtype=int)
                for notes in tr.find('div').contents:
                    
                    # 0     1    2   3   4   5   6   7   8   9
                    # 皿    1    2   3   4   5   6   7   BPM 小节
                    if notes.name == 'img':
                        if notes.get('src') == '../t.gif':    # BPM小节线
                            reg = re.compile(r'top:\d+')
                            top = reg.findall(notes.get('style'))[0]
                            pass ## TODO
                        elif notes.get('src') == '../b.gif' or notes.get('src') == '../w.gif': # 黑白键
                            # print(content.get('style'))
                            # use regex to get the two numbers
                            reg = re.compile(r'-?\d+')
                            top, left = reg.findall(notes.get('style'))
                            left = self.note_map[left]
                            df.iloc[int((int(top) + 4)/pic_height*128), int(left)] = 1

                        elif notes.get('src') == '../hhb.gif' or notes.get('src') == '../hhw.gif': # LN键
                            # print(content.get('style'))
                            # use regex to get the two numbers
                            reg = re.compile(r'-?\d+')
                            top, left = reg.findall(notes.get('style'))
                            left = self.note_map[left]
                            df.iloc[int((int(top))/pic_height*128), int(left)] = -1

                        elif notes.get('src') == '../s.gif' or notes.get("src") == "../sm.gif": # 皿
                            reg = re.compile(r'-?\d+')
                            top, left = reg.findall(notes.get('style'))
                            left = self.note_map[left]
                            # print(top)
                            if int(top) < 0: top = -4
                            df.iloc[int((int(top) + 4)/pic_height*128), left] = 1
                            # return(int(top) + 4, 1, left) # +4 因为图片高度为4
                        elif notes.get('src') == '../hhs.gif': # h皿开头
                            reg = re.compile(r'-?\d+')
                            top, left = reg.findall(notes.get('style'))
                            left = self.note_map[left]
                            df.iloc[int((int(top) + 4)/pic_height*128), left] = -1
                            # return(int(top) + 4, 1, left) # +4 因为图片高度为4
                        elif notes.get('src') == '../hs.gif': # H皿条
                            reg = re.compile(r'-?\d+')
                            top, left, height, width = reg.findall(notes.get('style'))
                            top = int(top/pic_height*128)
                            height = int(height/pic_height*128)

                            if top<0: top = 0
                            if top+1+height>128: height = 128 - top - 1
                            left = self.note_map[left]
                            df.iloc[top+1:top + height, left] = -0.5
                            # return(int(top) + 4, 2, left) # +4 因为图片高度为4
                        
                        elif notes.get('src') == '../ls.gif': # 皿条
                            reg = re.compile(r'-?\d+')
                            top, left, height, width = reg.findall(notes.get('style'))
                            top = int(int(top)/pic_height*128)
                            height = int(int(height)/pic_height*128)

                            if top<0: top = 0
                            if top+1+height>128: height = 128 - top - 1
                            left = self.note_map[left]
                            df.iloc[top+1:top + height, left] = 0.5
                            
                        elif notes.get('src') == '../lw.gif' or notes.get("src") == "../lb.gif": # 键盘条
                            reg = re.compile(r'-?\d+')
                            top, left, height, width = reg.findall(notes.get('style'))
                            top = int(int(top)/pic_height*128)
                            height = int(int(height)/pic_height*128)

                            if top<0: top = 0
                            if top+1+height>128: height = 128 - top - 1
                            left = self.note_map[left]
                            df.iloc[top+1:top + height, left] = 0.5

                        elif notes.get('src') == '../hw.gif' or notes.get("src") == "../hb.gif": # H键盘条
                            reg = re.compile(r'-?\d+')
                            top, left, height, width = reg.findall(notes.get('style'))
                            top = int(int(top)/pic_height*128)
                            height = int(int(height)/pic_height*128)

                            if top<0: top = 0
                            if top+1+height>128: height = 128 - top - 1
                            left = self.note_map[left]
                            df.iloc[top+1:top + height, left] = -0.5

                    elif notes.name == 'span':    # BPM数字，top+5为小节线位置，理论上图片高度为2，但+1即offset到0-127，使变速线在中间
                        # print(notes.text)
                        reg = re.compile(r'top:\d+')
                        top = int(reg.findall(notes.get('style'))[0][4:])
                        df.iloc[int((int(top) + 5 + 1)/pic_height*128), 8] = int(notes.text)

                mes = tr.find('a').get('id')[3:]

                df.iloc[:, 9] = int(mes)
                self.add(df)        

        return self.data

    def add(self, mes):
        self.data = self.data.append(mes)

    def find_soflan(self):
        soflan_info = []

        if len(self.data.iloc[:,1].diff().value_counts())>1:
            for index, row in self.data.iterrows():
                if row[8] != 0:
                    soflan_info.append((index, row[9], str(int(row[8]))))
        return soflan_info 

    def find_long_press(self):

    # 存储每个小节每个轨道的长按信息
        long_press_info = []

        # 遍历每个小节的每个轨道
        for group_name, group_df in self.data.groupby([9]):
            for track in range(8):
                long_press_start = None
                long_press_height = 0

                for index, row in group_df.iterrows():
                    # 获取当前位置的轨道值
                    current_value = row[track]

                    # 判断是否为长按开始位置
                    if current_value == 0.5 or current_value == -0.5:
                        if long_press_start is None:
                            long_press_start = index
                            long_press_value = current_value

                    # 判断是否为长按结束位置
                    if long_press_start is not None and current_value != long_press_value:
                        long_press_height = index - long_press_start + 1
                        long_press_info.append((group_name, track, long_press_start, long_press_height, long_press_value))
                        long_press_start = None

        return long_press_info # 小节，轨道，长按开始位置，高度

    def random(self, random_code):
        # 随机
        # code: 1-7随机轨道
        # random_code = random.sample(range(1,8),7)
        random_code_list = []
        for i in range(7):
            random_code_list.append(int(random_code[i]))
        index = [0] + random_code_list + [8, 9]

        self.data = self.data.reindex(columns=index)
        self.data.columns = [0,1,2,3,4,5,6,7,8,9]