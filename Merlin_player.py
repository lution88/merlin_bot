"""
*******************************************************************************************************************

날일 : 2022-03-11 金曜日 |  수정일     : 2022-04-13 水曜日
저자 : 윤정기            |  수정자     : 윤정기
제목 : Merlin_Player
내용 : 멀린 봇 플레이어 입니다. 

*******************************************************************************************************************
"""
# region 1) 멀린 봇 플레이어 section.  
import os
import time
import discord
from discord.ext import commands
import youtube_dl
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from discord_buttons_plugin import *

# endregion

client = commands.Bot(command_prefix ="!")
buttons = ButtonsClient(client)

user = []  # 유저가 입력한 노래 정보
musictitle = []  # 가공된 정보의 노래 제목
song_queue = []  # 가공된 정보의 노래 링크
musicnow = []  # 현재 출력되는 노래 배열

class youtube_player(commands.Cog):
    def __init__(self, client):
            self.client = client
            
    # title
    def title(self, msg):
        global music
        YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
        FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

        # Heroku 용 ChromeDriver 세팅
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
        driver.get("https://www.youtube.com/results?search_query="+msg+"+lyrics")
        source = driver.page_source
        bs = BeautifulSoup(source, 'lxml')
        entire = bs.find_all('a', {'id': 'video-title'})
        entireNum = entire[0]
        music = entireNum.text.strip()
        musictitle.append(music)
        musicnow.append(music)
        test1 = entireNum.get('href')
        url = 'https://www.youtube.com'+test1
        with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
        URL = info['formats'][0]['url']

        driver.quit()
        
        return music, URL
    # play
    def play(self, ctx):
        YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
        FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
        URL = song_queue[0]
        del user[0]
        del musictitle[0]
        del song_queue[0]
        if not ctx.voice_client.is_playing():
            ctx.voice_client.play(discord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS), after=lambda e: self.play_next(ctx)) 
            
    # play_next
    def play_next(self, ctx):
        if len(musicnow) - len(user) >= 2:
            for i in range(len(musicnow) - len(user) - 1):
                del musicnow[0]
        YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
        FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
        if len(user) >= 1:
            if not ctx.voice_client.is_playing():
                del musicnow[0]
                URL = song_queue[0]
                del user[0]
                del musictitle[0]
                del song_queue[0]
                ctx.voice_client.play(discord.FFmpegPCMAudio(URL,**FFMPEG_OPTIONS), after=lambda e: self.play_next(ctx))
            
        else:
            if not ctx.voice_client.is_playing():
                client.loop.create_task(ctx.voice_client.disconnect())
    
    @commands.command()
    async def join(self, ctx):
        if ctx.author.voice is None:
            await ctx.send("You're not in a voice channel!")
        voice_channel = ctx.author.voice.channel
        if ctx.voice_client is None:
            await voice_channel.connect()
            await ctx.send('마법사 멀린이 음성 채널에 접속했어요 ! 🔌💥 !')
        else:
            await ctx.voice_client.move_to(voice_channel)
    
    # 멀린 플레이어 연결 해제.
    @commands.command(name='dc')
    async def music_disconnect(self, ctx):
        await ctx.voice_client.disconnect()
        await ctx.send('멀린이 음성채널에서 떠났어요.. 다음에 봐요 ! 🔌💥 !')
    

    # 멀린 플레이어 바로 재생
    @commands.command(name='play')
    async def play_music(self, ctx, *, msg):
        # 사용자가 보이스 채널에 있는지 확인하는 구간, 없으면 You're not in a voice channel 메시지 보낸다.
        if ctx.author.voice is None:
            await ctx.send("You're not in a voice channel!")
        # 사용자가 있는 보이스채널 = voice_channel
        voice_channel = ctx.author.voice.channel
        
        if ctx.voice_client is None: # ctx.voice_client 가 None 이라면
            await voice_channel.connect() # 봇을 보이스채널에 접속시킨다.
            await ctx.send('마법사 멀린이 음성 채널에 접속했어요 ! 🔌💥 !') # 봇이 보이스채널에 접속되면 메세지 전송
        else: # ctx.voice_client 가 None 이 아니라면
            await ctx.voice_client.move_to(voice_channel)
        
        if ctx.voice_client.is_playing(): # 봇이 노래를 재생중이라면
            ctx.voice_client.stop() # 노래를 중단하고 셀레니움을 진행한다.
        
        # Heroku 용 ChromeDriver 세팅
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        
        
        
        global entireText
        
        #  크롬웹드라이버 및 FFMPEG 음원 기본 세팅
        FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
        YDL_OPTIONS = {'format': 'bestaudio'}  # 노래 재생을 위한 YDL 의 옵션 포맷 : bestaudio
        
        # 크롬웹드라이버 세팅
        chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
        driver.get("https://www.youtube.com/results?search_query="+msg+"+lyrics")   # 웹드라이버로 가져올 url 
        
        source = driver.page_source # 드라이버에서 가져온 html 중에서 page_source 만 가져온다.
        bs = BeautifulSoup(source, 'lxml')  # 가져온 source 를 lxml 로 파싱한다.
        
        entire = bs.find_all('a', {'id': 'video-title'})    # <a> 중 id 가 video-title 인 애들만 찾아서 entire 변수에 담는다 : 검색해서 가져온 결과들
        entireNum = entire[0]   # 검색해서 가져온 결과들 중 [0] 첫 번째 데이터만 가져온다.
        entireText = entireNum.text.strip() # 첫 번째 데이터의 text 를 가져오고 .strip 을 해서 여백을 삭제한다.
        musicurl = entireNum.get('href')    # 데이터 중에 href 만 가져와서 musicurl 에 담는다.
        
        thumbnail = bs.find_all('img', {'class':'style-scope yt-img-shadow'})   # 썸네일 img 태그 찾아오기
        thumbnail_img = thumbnail[1]    #
        thumbnail_img_src = thumbnail_img.get('src')    # 이미지 src 
        
        views = bs.find_all('span', {'class': 'style-scope ytd-video-meta-block'})  # 유튜브 views
        views_num = views[0].text

        channel = bs.find_all('a', {'class':'yt-simple-endpoint style-scope yt-formatted-string'}) # 노래 찾아온 유튜브 채널명
        channel_name = channel[0].text
        
        playtime = driver.find_element(by=By.XPATH, value=('//*[@id="video-title"]')).get_attribute('aria-label').split()
        sec = playtime[-4]
        min = playtime[-6]
        play_time = f'{min}분:{sec}초'
        

        url = 'https://www.youtube.com'+musicurl    # 실제 실행하게될 url 주소를 url 변수에 담는다.
        driver.quit()   # 크롬웹드라이버를 종료한다.
        musicnow.insert(0, entireText)
        with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:      # 위에서 정의한 YDL_OPTIONS 를 사용하여 youtube_dl 을 실행하고 앞으로 이름은 ydl 로 정의한다.
            info = ydl.extract_info(url, download=False)    # url 에서 정보를 추출해서 info 변수에 담는다.
            URL = info['formats'][0]['url']                 # 추출한 info 의 ['formats'] 의 첫 번째 정보의 ['url'] 정보를 URL 변수에 담는다.
            go = await discord.FFmpegOpusAudio.from_probe(URL,**FFMPEG_OPTIONS) # 추출한 URL 을 디스코드의 음원 포맷 기능을 사용하여 포맷 후 go 변수에 담는다.
            music_embed = discord.Embed(title= f"{entireText}\n",  description=f"검색어 [{msg}] 를 재생중입니다.", url=url, color = 0x00ff00) # 포맷이 생성되면 embed 출력
            music_embed.set_thumbnail(url=f'{thumbnail_img_src}')
            music_embed.add_field(name="CHANNEL", value=f'{channel_name}\n',inline=True )
            music_embed.add_field(name="VIEWS", value=f'{views_num}\n',inline=True )
            music_embed.add_field(name="PLAYTIME", value=f'{play_time}',inline=True )
            music_embed.set_footer(text="Information requested by : Merlin bot dev-team", icon_url="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2Ft4DU5%2Fbtrwl8gfHgn%2Flc2wGb9OU9Ms4al4clTRNk%2Fimg.png")
            
            await ctx.send(embed=music_embed)
            ctx.voice_client.play(go)       # 위에서 추출해 온 음악 정보인 go 를 보이스 채널에서 노래를 재생한다.
            
    # 지금 재생하는 노래
    @commands.command(name='now')
    async def music_now(self, ctx):
        if not ctx.voice_client.is_playing():
            await ctx.send("you're not listening to music now")
        else:
            await ctx.send(embed = discord.Embed(title = "지금노래", description = "현재 " + musicnow[0] + "을(를) 재생하고 있습니다.", color = 0x00ff00))

    # 멀린 플레이어 일시 중지.
    @commands.command(name='pause')
    async def music_pause(self, ctx):
        if ctx.voice_client.is_playing():
            ctx.voice_client.pause()
            await ctx.send('Your Youtube Music is Paused ⏸️ !')
        else:
            await ctx.send("you're not listening to music now")

    # 멀린 플레이어 다시 재생.
    @commands.command(name='resume')
    async def music_resume(self, ctx):
        if not ctx.voice_client.is_playing():
            ctx.voice_client.resume()
            await ctx.send('Your Youtube Music is re-play ➡️ !')
        else:
            await ctx.send("you're not listening to music now")
    
    # 멀린 플레이어 재생 종료.
    @commands.command(name='stop')
    async def music_stop(self, ctx):
        if ctx.voice_client.is_playing():
            ctx.voice_client.stop()
            await ctx.send('Your Youtube Music is stoped :stop_button:  !')
            ctx.voice_client.disconnect()
            
        else:
            await ctx.send("you're not listening to music now")

    # 멀린 플레이어 
    @commands.command(name="player.help")
    async def music_help(self, ctx):

        music_help_Embed = discord.Embed(
            title="Merlin Bot Music Player Commands Guide.", color=discord.Color.blue()
        )

        # 엠베딩 저자.
        music_help_Embed.set_author(
            name=ctx.author.display_name,
            url="https://www.google.com/",
            icon_url=ctx.author.avatar_url,
        )
        # 엠베딩 썸네일.
        music_help_Embed.set_thumbnail(url="https://i.imgur.com/axLm3p6.jpeg")

        # 엠베딩 내용.
        music_help_Embed.add_field(
            name="!player.help", value="멀린 봇 플레이어의 모든 명령어를 볼 수 있습니다.\n", inline=True
        )
        music_help_Embed.add_field(
            name="!join", value="멀린 봇을 내가 속한 음성 채널로 부릅니다.\n", inline=True
        )
        music_help_Embed.add_field(
            name="!dc", value="멀린 봇을 내가 속한 음성 채널에서 내보냅니다.", inline=True
        )
        music_help_Embed.add_field(
            name="!play", value="멀린 봇에게 유튜브 음악을 찾아 재생 시킵니다..", inline=True
        )
        music_help_Embed.add_field(
            name="!stop", value="멀린 봇에게 유튜브 음악 재생을 중지 시킵니다.", inline=True
        )
        music_help_Embed.add_field(
            name="!pause", value="멀린 봇에게 유튜브 음악을 일시중지 시킵니다.", inline=True
        )
        music_help_Embed.add_field(
            name="!resume", value="멀린 봇에게 일시중지된 음악을 재생 시킵니다.", inline=True
        )
        music_help_Embed.set_footer(
            text="Information requested by : {0}".format("Merlin bot dev-team")
        )
        await ctx.send(embed=music_help_Embed)

def setup(client):
    client.add_cog(youtube_player(client))
