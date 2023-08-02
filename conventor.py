# read html file and get table
import bs4
import re
import pandas as pd
import numpy as np
    
class fumen():
    def __init__(self):
        self.data = pd.DataFrame()
        self.note_map = {
            "0": 0,
            "37": 1,
            "51": 2,
            "65": 3,
            "79": 4,
            "93": 5,
            "107": 6,
            "121": 7
        }
    def read(self, file_path):
        read_file = open(file_path, 'r')
        soup = bs4.BeautifulSoup(read_file, 'html.parser')

        soup_table = soup.find_all('table')


        for table in soup_table[1:]: # 第一张表是原表
            len(table.find_all('tr'))
            for tr in table.find_all('tr'):
                df = pd.DataFrame(np.zeros((128, 10)), dtype=int)
                for notes in tr.find('div').contents:
                    print(notes)
                    
                    location = self.parse(notes)
                    print(self.parse(notes))

                    if location is None:
                        continue
                    else:
                        y, n, x = location
                        df.iloc[y, x] = n
                mes = tr.find('th').text
                df.iloc[:, 9] = int(mes)
                self.add(df)        

        return self.data
    def parse(self, content):
        # 0     1    2   3   4   5   6   7   8   9
        # 皿    1    2   3   4   5   6   7   BPM 小节
        if content.name == 'img':
            if content.get('src') == '../t.gif':    # BPM小节线
                reg = re.compile(r'top:\d+')
                top = reg.findall(content.get('style'))[0]
                pass
            elif content.get('src') == '../b.gif' or content.get('src') == '../w.gif': # 黑白键
                # print(content.get('style'))
                # use regex to get the two numbers
                reg = re.compile(r'\d+')
                top, left = reg.findall(content.get('style'))
                left = self.note_map[left]
                return(int(top) + 4, 1, int(left)) # +4 因为图片高度为4
            elif content.get('src') == '../s.gif': # 皿
                reg = re.compile(r'\d+')
                top, left = reg.findall(content.get('style'))
                left = self.note_map[left]
                return(int(top) + 4, 1, left) # +4 因为图片高度为4
            
            elif content.get('src') == '../hhs.gif': # HH皿
                reg = re.compile(r'\d+')
                top, left = reg.findall(content.get('style'))
                left = self.note_map[left]
                return(int(top) + 4, -1, left)
            
            elif content.get('src') == '../lb.gif' or content.get("src") == "../lm": # HH条
                reg = re.compile(r'\d+')
                top, left = reg.findall(content.get('style'))
                left = self.note_map[left]
                return(int(top) + 4, -1, left)
            elif content.get('src') == '../hw.gif' or content.get("src") == "../hb": # HH条
                reg = re.compile(r'\d+')
                top, left = reg.findall(content.get('style'))
                left = self.note_map[left]
                return(int(top) + 4, -1, left)

        elif content.name == 'span':    # BPM数字，top+5为小节线位置，理论上图片高度为2，但+1即offset到0-127，使变速线在中间
            print(content.text)
            reg = re.compile(r'top:\d+')
            top = int(reg.findall(content.get('style'))[0][4:])
            return(top+5+1, int(content.text), 8)
    def add(self, mes):
        self.data = self.data.append(mes)
