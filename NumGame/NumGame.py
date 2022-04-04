#Num_Game#
#Ver:A0.4#

# import part-----------------------------------------

import os
import random
import sys

from icecream import ic

# Def part-----------------------------------------

mv = [[1, 0], [-1, 0], [0, 1], [0, -1]]
lock = {0: {}, 1: {}, 2: {}}
cnt = 0
ok = 0


def dfs(x, y, step):
    global lock, ok
    lock[x][y] = 1
    if step == cnt:
        ok = 1
        return
    did = 0
    for i in mv:
        xx = x + i[0]
        yy = y + i[1]
        if xx < 0 or xx >= 3 or yy < 0 or yy >= 3 or a[xx][yy] == '*' or lock[xx].get(yy):
            continue
        dfs(xx, yy, step + 1)
        did = 1
        break
    # if not all(a[x][y] != '*' and lock[x].get(y) for x in range(3) for y in range(3)):
    #     return 99999
    # return step

num_map = [['7', '8', '9'], ['4', '5', '6'], ['1', '2', '3']]

def where_click(num):
    global click_row, click_column
    for i in range(3):
        for j in range(3):
            if num_map[i][j] == str(num):
                click_row = i
                click_column = j


def print_map():
    print("-------------------------------------------")
    for i in range(3):
        print(a[i][0], a[i][1], a[i][2])
    print("-------------------------------------------")

# main-----------------------------------------



# 简介
print("数字键盘游戏")
print("最好使用九宫格键盘进行游玩")
print("游戏会自动输出一个表格，“*”表明这个方格不能经过，数字表明这个方格可以经过")
print("你的任务就是把所有可以走的数字都走一遍，并且尽量用最少的步数，走过的数字会变成 = ")
print("每个方格的右边都会有一个数子，你需要输入这个数字以走过这个方格")
print("你不能跳过方格或者走不相邻你的方格")
print("-------------------------------------------")
print()


# 用户名
user_name_file_path = "game_name.txt"

if os.path.isfile(user_name_file_path):
    with open(user_name_file_path, mode='r', encoding='utf-8') as user_name:
        print("欢迎回来，", user_name.read(), "!")
else:
    with open(user_name_file_path, mode="w", encoding="utf-8") as user_name:
        user_name.write(input("请输入用户名："))
print("-------------------------------------------")
print()

# 读取模式
game_mode = int(input(("请选择游戏模式，0为内置，1为随机，选择后需重启游戏才可切换设置：")))

while(True):
    # 模式为内置
    if game_mode == 0:
        # ic()
        user_level_file_path = "user_level.txt"
        if os.path.isfile(user_level_file_path):
            # ic()
            with open(user_level_file_path, mode='r', encoding='utf-8') as user_level:
                userlevel = int(user_level.read())
                if userlevel > 10:
                    print("数值错误，请删除user_level.txt重置关卡关数")
                    sys.exit(0)
                print("你现在进行到：", userlevel, "关，总共10关")
        else:
            with open(user_level_file_path, mode="w", encoding="utf-8") as user_level:
                user_level.write(str(1))
                userlevel = 1
                print("你现在进行到第一关，总共10关")

        # 加载地图
        maps_file_path = "maps\\"+str(userlevel)+".txt"
        # ic(maps_file_path)
        a = [['', '', ''], ['', '', ''], ['', '', '']]
        with open(maps_file_path, mode='r', encoding='utf-8') as f:
            temp = f.read().split("\n")
            for i in range(3):
                t = temp[i].split(" ")
                # ic(t)
                for j in range(3):
                    a[i][j] = t[j]
                    if t[j] != '*':
                        cnt += 1
            # ic(a)
        # ic(cnt)
        # 函数跑最小步数
        ok_ps = []
        for i in range(3):
            for j in range(3):
                if a[i][j] == '*':
                    continue
                lock = {0: {}, 1: {}, 2: {}}
                ok = 0
                dfs(i, j, 1)
                if ok:
                    ok_ps.append([i, j])
        ic(cnt, ok_ps)
        # cnt为最少走的步数，ok_ps数组里面存了可以从某个点获胜的数据

        # ic(a)

        # rou 行
        # column 列
        
        last_click_row = -1
        last_click_column = -1
        click_row = -1
        click_column = -1
        first_click = bool(1)

        walk = 0

        while(True):
            print_map()
            where_click(int(input("请输入你下一步要走哪个数字：")))

            #ic(click_row,click_column)
            #ic(last_click_row,last_click_column)
            
            if(walk+1 != cnt or walk == cnt):
                if last_click_column == -1 and last_click_row == -1:
                    if a[click_row][click_column] != "*":
                        a[click_row][click_column] = "="
                        last_click_row = click_row
                        last_click_column = click_column
                        walk += 1
                    else:
                        print("输入错误")
                else:
                    if (abs(last_click_row-click_row)+abs(last_click_column-click_column)==1 and 
                    a[click_row][click_column] != "*" and a[click_row][click_column] != "="):
                        a[click_row][click_column] = "="
                        last_click_row = click_row
                        last_click_column = click_column
                        walk += 1
                    else:
                        print("输入错误")
            else:
                break
        print_map()
        print("恭喜通过第",userlevel,"关！正在保存……")
        userlevel += 1
        with open(user_level_file_path, mode="w", encoding="utf-8") as user_level:
            user_level.write(str(userlevel))
    
    # 模式为随机
    