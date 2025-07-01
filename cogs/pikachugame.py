import random

import discord
from discord import app_commands
from discord.ext import commands
from discord.ext import tasks
import cv2
import numpy as np
import requests
import sqlite3


map = cv2.imread("img/map.png")

events = [None for _ in range(91)]
events[3], events[6],   events[12],  events[13], events[18], events[21],  events[25], events[26], events[33],  events[39] =\
"Lapras",  "Passimian", "Exeggutor", "Koko",     "Cosmog",   "Passimian", "Lapras",   "Lele",     "Passimian", "Jigglypuff"

events[43], events[45], events[46], events[55], events[56], events[57],  events[70],   events[77],   events[78],   events[79] =\
"Popplio",  "Snorlax",  "Snorlax",  "Snorlax",  "Snorlax",  "Passimian", "Turtonator", "Jigglypuff", "Jigglypuff", "Jigglypuff"

events[83], events[86], events[87], events[89],  events[90] =\
"Pidgeot", "Rayquaza",  "Bewear",   "Dragonite", "Pikachu"



class Pikachugame(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.con = sqlite3.connect('pika.db')
        self.cursor = self.con.cursor()
        self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    pos INTEGER NOT NULL,
                    turn INTEGER NOT NULL,
                    sleep BOOLEAN DEFAULT 0,
                    boost BOOLEAN DEFAULT 0
                )''')
        self.con.commit()
        print("創建 users table (pika.db)")

    def __del__(self):
        self.con.close()

    def people_count(self):
        self.cursor.execute("SELECT COUNT(*) FROM users;")
        return self.cursor.fetchone()[0]

    def find_player_by_turn(self, turn):
        self.cursor.execute("SELECT id, name, pos, turn, sleep, boost FROM users WHERE turn = ?;", (turn,))
        return self.cursor.fetchone()[0]

    def gogo(self, channel, player, des):
        if events[des] == "Lapras":
            if des == 3:
                await channel.send(f"<@{player[0]}> 遇到了**拉普拉斯**，載著<@{player[0]}>游到了**17**！")
                self.cursor.execute("UPDATE users "
                                    "SET pos = 17, boost = 0 "
                                    "WHERE id = ?;", (player[0],))
            if des == 25:
                await channel.send(f"<@{player[0]}> 遇到了**拉普拉斯**，載著<@{player[0]}>游到了**37**！")
                self.cursor.execute("UPDATE users "
                                    "SET pos = 37, boost = 0 "
                                    "WHERE id = ?;", (player[0],))

        if events[des] == "Passimian":
            ls = [6, 21, 33, 57]
            ls.remove(des)
            new_des = ls[random.randint(0, 2)]
            await channel.send(f"<@{player[0]}> 遇到了**投擲猴**，將<@{player[0]}>丟給了其中一個同伴！")
            await channel.send(f"<@{player[0]}> 被丟到了 **{new_des}**！")
            self.cursor.execute("UPDATE users "
                                "SET pos = ?, boost = 0 "
                                "WHERE id = ?;", (new_des, player[0]))

        if events[des] == "Exeggutor":
            await channel.send(f"<@{player[0]}> 遇到了**阿羅拉椰蛋樹**，並且爬著他到了**52**！")
            self.cursor.execute("UPDATE users "
                                "SET pos = 52, boost = 0 "
                                "WHERE id = ?;", (player[0]))

        if events[des] == "Koko":
            await channel.send(f"<@{player[0]}> 遇到了守護神**卡璞•鳴鳴**，他給了<@{player[0]}>一個電Z純晶！")
            await channel.send(f"受到守護神的加持，下一輪<@{player[0]}>的移動步數變為兩倍！")
            self.cursor.execute("UPDATE users "
                                "SET boost = 1 "
                                "WHERE id = ?;", (player[0]))

        if events[des] == "Cosmog":
            await channel.send(f"<@{player[0]}> 遇到了小星雲**科斯莫古**！")
            new_des = random.randint(1, 60)
            await channel.send(f"小星雲將<@{player[0]}>瞬間移動傳送到了**{new_des}**！")
            self.cursor.execute("UPDATE users "
                                "SET pos = ?, boost = 0 "
                                "WHERE id = ?;", (new_des, player[0]))
            if events[new_des] is not None:
                self.gogo(channel, player, new_des)

        if events[des] == "Lele":
            await channel.send(f"<@{player[0]}> 遇到了守護神**卡璞•蝶蝶**，被戲耍了一番！")
            await channel.send(f"<@{player[0]}> 回到了**11**！")
            self.cursor.execute("UPDATE users "
                                "SET pos = 11,  boost = 0 "
                                "WHERE id = ?;", (player[0]))

        if events[des] == "Jigglypuff":
            await channel.send(f"<@{player[0]}> 遇到了在唱歌的**胖丁**，於是睡著了！")
            self.cursor.execute("UPDATE users "
                                "SET sleep = 1, boost = 0 "
                                "WHERE id = ?;", (player[0]))

        if events[des] == "Popplio":
            await channel.send(f"<@{player[0]}> 遇到了**球球海獅**，他吹泡泡將<@{player[0]}>吹到了**62**！")
            self.cursor.execute("UPDATE users "
                                "SET pos = 62,  boost = 0 "
                                "WHERE id = ?;", (player[0]))

        if events[des] == "Snorlax":
            await channel.send(f"<@{player[0]}> 撞到了正在睡覺的**卡比獸**而暈倒了！")
            await channel.send(f"<@{player[0]}> 接下來兩回合都會在睡眠狀態！")
            self.cursor.execute("UPDATE users "
                                "SET sleep = 2,  boost = 0 "
                                "WHERE id = ?;", (player[0]))

        if events[des] == "Turtonator":
            await channel.send(f"<@{player[0]}> 撞到了**爆焰龜獸**的刺而噴飛了！")
            await channel.send(f"<@{player[0]}> 回到了**30**！")
            self.cursor.execute("UPDATE users "
                                "SET pos = 30,  boost = 0 "
                                "WHERE id = ?;", (player[0]))

        if events[des] == "Pidgeot":
            await channel.send(f"<@{player[0]}> 遇到了在空中的**大比鳥**！")
            await channel.send(f"<@{player[0]}> 被吹飛了20格，回到了**63**！")
            if random.randint(0,100) > 50:
                await channel.send(f"<@{player[0]}> 被吹暈了！下回合無法行動。")
                self.cursor.execute("UPDATE users "
                                    "SET pos = 63 ,sleep = 1 , boost = 0 "
                                    "WHERE id = ?;", (player[0]))
            else:
                self.cursor.execute("UPDATE users "
                                    "SET pos = 63 , boost = 0 "
                                    "WHERE id = ?;", (player[0]))

        if events[des] == "Rayquaza":
            await channel.send(f"<@{player[0]}> 遇到了**烈空坐**，滑到了**66**！")
            self.cursor.execute("UPDATE users "
                                "SET pos = 66 , boost = 0 "
                                "WHERE id = ?;", (player[0]))

        if events[des] == "Bewear":
            await channel.send(f"# 熊！！！！！")
            await channel.send(file=discord.File("img/bewear.jpg"))
            await channel.send(f"<@{player[0]}> 被**穿著熊**抱回了原點！")
            await channel.send(f"好討厭的感覺啊！！！")
            self.cursor.execute("UPDATE users "
                                "SET pos = 0 , boost = 0 "
                                "WHERE id = ?;", (player[0]))

        if events[des] == "Dragonite":
            await channel.send(f"<@{player[0]}> 遇到**快龍**了！")
            rand = random.randint(1, 4)
            new_des = des - 10*rand
            await channel.send(f"<@{player[0]}> 被**快龍**揍飛了{10*rand}格，回到**{new_des}**！")
            self.cursor.execute("UPDATE users "
                                "SET pos = ? , boost = 0 "
                                "WHERE id = ?;", (new_des, player[0]))
            if events[new_des] is not None:
                self.gogo(channel, player, new_des)

        if events[des] == "Pikachu":
            await channel.send(f"<@{player[0]}> 終於見到**皮卡丘**了！")

    @app_commands.command(name="加入_拯救皮卡丘", description="加入遊戲")
    async def pika_join(self, interaction: discord.Interaction):

        await interaction.response.defer()
        name = interaction.user.name
        id = interaction.user.id

        with open('pika_playing.txt', 'r') as f:
            playing = f.read()

        if playing != "0":
            await interaction.followup.send("遊戲已經開始了唷！")
            return

        if self.people_count() >= 6:
            await interaction.followup.send("已經滿人了唷！")

        count = self.people_count()
        if count > 0:
            await interaction.followup.send(f"{interaction.user.mention} 己經在遊戲裡囉！")
            return

        try:
            self.cursor.execute('''INSERT INTO users (id, name, pos, turn, sleep, boost) VALUES (?, ?, ?, ?);''', (id, name, 0, count+1, 0, 0))

            # self.cursor.execute('''INSERT INTO users (name, pos) VALUES (?, ?) ON CONFLICT(name) DO UPDATE SET
            #                     name = EXCLUDED.name,
            #                     pos = EXCLUDED.pos
            #                     WHERE name = EXCLUDED.name;''', (name, 0))
        except Exception as e:
            await interaction.followup.send(e)
            return

        print(name, "加入拯救皮卡丘！")
        self.con.commit()
        await interaction.followup.send(f"{interaction.user.mention} 加入拯救皮卡丘！")

    @app_commands.command(name="開始_拯救皮卡丘", description="開始遊戲")
    async def pika_start(self, interaction: discord.Interaction):

        await interaction.response.defer()

        with open('pika_playing.txt', 'r') as f:
            playing = f.read()

        if playing != "0":
            await interaction.followup.send("遊戲已經開始了唷！")
            return

        if self.people_count() < 2:
            await interaction.followup.send("人數還不夠唷！")
            return

        with open('pika_playing.txt', 'w') as f:
            f.write("1")

        await interaction.followup.send("遊戲開始！")

        ls = [0, 0, 0, 0, 0, 0, 0]
        try:
            self.cursor.execute("SELECT id, name, pos, turn, sleep, boost FROM users;")
            players = self.cursor.fetchall()
            # print(players)
            for player in players:
                ls[ player[3] ] = player[0]  # ls[turn] = id
            # print(ls)
            msg = "順序： "
            for i in range(1,7):
                if ls[i] == 0:
                    break
                msg += f"<@{ls[i]}>({i}), "

            await interaction.channel.send(msg)
            await interaction.channel.send(f"先從<@{ls[1]}>開始， /移動 來丟骰子前進！")

        except Exception as e:
            await interaction.channel.send(e)

    @app_commands.command(name="移動_拯救皮卡丘", description="丟出一個骰子")
    async def pika_move(self, interaction: discord.Interaction):

        await interaction.response.defer()

        with open('pika_playing.txt', 'r') as f:
            now = f.read()

        if now == "0":
            await interaction.followup.send("遊戲還沒開始唷！")
            return

        player_now = self.find_player_by_turn(now)  # id, name, pos, turn, sleep, boost

        if player_now[0] != interaction.user.id:
            await interaction.followup.send(f"現在輪到 <@{player_now[0]}> 唷！")
            return

        step = random.randint(1, 6)

        if player_now[5] == 1:
            des = player_now[2] + step*2
            if des > 90:
                des = 180 - des
            await interaction.followup.send(f"骰子的結果是**{step}**，由於受到卡璞•鳴鳴的加持，移動了**{step*2}步**，來到**{des}**！  ({player_now[2]}->{des})")

        else:
            des = player_now[2] + step
            if des > 90:
                des = 180 - des
            await interaction.followup.send(f"骰子的結果是**{step}**，來到**{des}**！  ({player_now[2]}->{des})")

        if events[des] is None:
            self.cursor.execute("UPDATE users "
                                "SET pos = ?, boost = 0 "
                                "WHERE id = ?;", (des, player_now[0]))
        else:
            self.gogo(interaction.channel, player_now, des)

        while True:
            now += 1
            if now > self.people_count():
                now = 1

            player_now = self.find_player_by_turn(now)
            if player_now[4] > 0:
                await interaction.channel.send(f"<@{player_now[0]}> 還在睡覺！")
                self.cursor.execute("UPDATE users "
                                    "SET sleep = ? "
                                    "WHERE id = ?;", (player_now[4]-1, player_now[0]))
            else:
                await interaction.channel.send(f"輪到 <@{player_now[0]}> 了！")
                with open('pika_playing.txt', 'w') as f:
                    f.write(now)
                return

    @app_commands.command(name="頭像", description="取得頭像")
    async def head(self, interaction: discord.Interaction):

        await interaction.response.defer()
        name = interaction.user.name

        img = None
        # try:
        #     img = cv2.imread(f"img/user_avatar/{name}.png")
        #     print("read")
        # except:
        url = interaction.user.avatar.url
        head = requests.get(url)
        nparr = np.frombuffer(head.content, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        print("decode")

        if img is not None:
            print(f"成功從 URL 下載並解碼圖像，原始尺寸：{img.shape[:2]}")
            height, width = img.shape[:2]
            radius = min(height, width)//2
            mask = np.zeros((height, width), dtype=np.uint8)
            cv2.circle(mask, (width//2, height//2), radius, 255, -1)

            if img.shape[-1] == 3:
                img = cv2.cvtColor(img, cv2.COLOR_RGB2RGBA)
            elif img.shape[-1] == 1:  # 灰度圖
                img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGBA)

            img[:, :, 3] = cv2.bitwise_and(img[:, :, 3], mask)

            img = cv2.resize(img, (70, 70), interpolation=cv2.INTER_LANCZOS4)

            # # 使用 OpenCV 調整圖像大小
            # resized_img = cv2.resize(img, target_size)
            # print(f"調整後的圖像尺寸：{resized_img.shape[:2]}")

            # 使用 OpenCV 儲存調整大小後的圖像
            cv2.imwrite(f"img/user_avatar/{name}.png", img)

        else:
            print("無法解碼??")

        await interaction.followup.send(file=discord.File(f"img/user_avatar/{name}.png"))


async def setup(bot: commands.Bot):
    await bot.add_cog(Pikachugame(bot))