'''
*******************************************************************************************************************

날일 : 2022-03-11 金曜日 |  수정일     : 2022-04-13 水曜日
저자 : 이성호            |  수정자     : 조시욱
제목 : Google_calendar
내용 : 멀린 봇 구글 캘린더 RDS 비설정 파일 입니다. 

*******************************************************************************************************************
'''

#region 1) 멀린 봇 캘린더 section.

from __future__ import print_function
# 구글 API 관련 패키지
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
# 시간 연산 패키지
import datetime
from discord.ext import commands
import discord
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os

# 구글 캘린더 권한 관련 코드
SCOPES = ['https://www.googleapis.com/auth/calendar']

#endregion

""" 2) Google_calendar category class.   

"""
class Google_calendar(commands.Cog):
      def __init__(self, client):
            self.client = client

       # 구글 캘린더 명령어 설명
      @commands.command()
      async def calendar(self, ctx):
        embed = discord.Embed(title="Calendar Command", description="", color = 0x00ff00)
        embed.add_field(name='Event specific list view', value='!list YYYY-MM-DD', inline=False)
        embed.add_field(name="Today event list view", value='!list today', inline=False)
        embed.add_field(name="This month event list view", value='!list month', inline=False)
        embed.add_field(name="Month specific event list view", value='!list month YYYY-MM', inline=False)
        embed.add_field(name="This year event list view", value='!list year', inline=False)
        embed.add_field(name="Year specific event list view", value='!list year YYYY', inline=False)
        embed.add_field(name='Event create(Year/Month/Date/Time)', value='!create YYYY-MM-DD(start date) HH:MM:SS(start time) YYYY-MM-DD(end date) HH:MM:SS(end time) EventTitle', inline=False)
        embed.add_field(name='Event create(Year/Month/Date)', value='!create YYYY-MM-DD(start date) YYYY-MM-DD(end date) EventTitle', inline=False)
        embed.add_field(name='Event create(Month/Date/Time)', value='!create MM-DD(start date) HH:MM:SS(start time) MM-DD(end date) HH:MM:SS(end time) EventTitle', inline=False)
        embed.add_field(name='Event create(Month/Date)', value='!create MM-DD(start date) MM-DD(end date) EventTitle', inline=False)
        embed.add_field(name='Event create(Today)', value='!create today EventTitle', inline=False)
        embed.add_field(name='Event update', value='!update YYYY-MM-DD IndexNumber EventTitle to update', inline=False)
        embed.add_field(name='Event delete', value='!delete YYYY-MM-DD IndexNumber', inline=False)
        await ctx.send(embed=embed)

      # 일정 생성
      @commands.command()
      async def create(self, ctx, *, msg):
          # 구글 API 인증 코드
          creds = None
          if os.path.exists('token.json'):
              creds = Credentials.from_authorized_user_file('token.json', SCOPES)
          # If there are no (valid) credentials available, let the user log in.
          if not creds or not creds.valid:
              if creds and creds.expired and creds.refresh_token:
                  creds.refresh(Request())
              else:
                  flow = InstalledAppFlow.from_client_secrets_file(
                      'credentials.json', SCOPES)
                  creds = flow.run_local_server(port=0)
              # Save the credentials for the next run
              with open('token.json', 'w') as token:
                  token.write(creds.to_json())
          service = build('calendar', 'v3', credentials=creds)
          # 메세지 입력받음
          input_data = (msg.split(' '))
          # 입력 메세지를 공백으로 구분해서 제목 입력
          if input_data[0] == 'today':
              title_list = input_data[1:]
              title = " ".join(title_list)
              # 시작/종료 날짜를 현재 시간의 날짜로 입력
              start_datetime = (datetime.date.today()) + datetime.timedelta(hours=9)
              start_datetime = datetime.date.today().strftime("%Y-%m-%d")
              end_datetime = (datetime.date.today()) + datetime.timedelta(hours=9)
              end_datetime = datetime.date.today().strftime("%Y-%m-%d")
              # 캘린더 이벤트 내용 입력
              event = {
                      'summary': title, # 일정 제목
                      # 'location': '게더캠프', # 일정 장소
                      # 'description': '캘린더 졸랭어렵군요', # 일정 설명
                      'start': { # 시작 날짜
                          'date': start_datetime,
                          'timeZone': 'Asia/Seoul',
                      },
                      'end': { # 종료 날짜
                          'date': end_datetime,
                          'timeZone': 'Asia/Seoul',
                      },
                      # 'recurrence': [ # 반복 지정
                      #     'RRULE:FREQ=DAILY;COUNT=1' # 일단위
                      # ],
                      # 'attendees': [ # 참석자
                      #     {'email': 'hopao159@gmail.com'},
                          # {'email': 'test@example.com'},
                      # ],
                      # 'reminders': { # 알림 설정
                      #     'useDefault': False,
                      #     'overrides': [
                      #         {'method': 'email', 'minutes': 24 * 60}, # 24 * 60분 = 하루 전 알림
                      #         {'method': 'popup', 'minutes': 10}, # 10분 전 알림
                      #     ],
                      # },
                  }
          # 년을 입력하지 않을 경우
          if input_data[0] != 'today':
              if len(input_data[0]) < 6:
                  # 시간 데이터를 입력하지 않을 경우
                  if ":" not in input_data[1]:
                      title_list = input_data[2:]
                      title = " ".join(title_list)
                      date_data = input_data[:2]
                      start_date_split = date_data[0].split('-')
                      end_date_split = date_data[1].split('-')
                      start_datetime = (datetime.datetime(datetime.date.today().year, int(start_date_split[0]), int(start_date_split[1]))) + datetime.timedelta(hours=9)
                      start_datetime = datetime.datetime(datetime.date.today().year, int(start_date_split[0]), int(start_date_split[1])).strftime("%Y-%m-%d")
                      end_datetime = (datetime.datetime(datetime.date.today().year, int(end_date_split[0]))) + datetime.timedelta(hours=9)
                      end_datetime = datetime.datetime(datetime.date.today().year, int(end_date_split[0]), int(end_date_split[1])).strftime("%Y-%m-%d")
                      event = {
                          'summary': title, # 일정 제목
                          'start': { # 시작 날짜
                              'date': start_datetime,
                              'timeZone': 'Asia/Seoul',
                          },
                          'end': { # 종료 날짜
                              'date': end_datetime,
                              'timeZone': 'Asia/Seoul',
                          },
                      }
                  # 시간 데이터를 입력 할 경우
                  else:
                      title_list = input_data[4:]
                      title = " ".join(title_list)
                      date_data = input_data[:4]
                      start_date_split = date_data[0].split("-")
                      start_time_split = date_data[1].split(":")
                      end_date_split = date_data[2].split("-")
                      end_time_split = date_data[3].split(":")
                      start_datetime = (datetime.datetime(datetime.date.today().year, int(start_date_split[0]), int(start_date_split[1]), int(start_time_split[0]), int(start_time_split[1]), 0)) + datetime.timedelta(hours=9)
                      start_datetime = datetime.datetime(datetime.date.today().year, int(start_date_split[0]), int(start_date_split[1]), int(start_time_split[0]), int(start_time_split[1]), 0).strftime("%Y-%m-%dT%H:%M:%S")
                      end_datetime = (datetime.datetime(datetime.date.today().year, int(end_date_split[0]), int(end_date_split[1]), int(end_time_split[0]), int(end_time_split[1]), 0)) + datetime.timedelta(hours=9)
                      end_datetime = datetime.datetime(datetime.date.today().year, int(end_date_split[0]), int(end_date_split[1]), int(end_time_split[0]), int(end_time_split[1]), 0).strftime("%Y-%m-%dT%H:%M:%S")
                      event = {
                          'summary': title, # 일정 제목
                          'start': { # 시작 날짜
                              'dateTime': start_datetime,
                              'timeZone': 'Asia/Seoul',
                          },
                          'end': { # 종료 날짜
                              'dateTime': end_datetime,
                              'timeZone': 'Asia/Seoul',
                          },
                      }
              # 년을 입력 할 경우
              else:
                  # 시간 데이터를 입력하지 않을 경우
                  if ":" not in input_data[1]:
                      title_list = input_data[2:]
                      title = " ".join(title_list)
                      date_data = input_data[:2]
                      start_date_split = date_data[0].split('-')
                      end_date_split = date_data[1].split('-')
                      start_datetime = (datetime.datetime(int(start_date_split[0]), int(start_date_split[1]), int(start_date_split[2]))) + datetime.timedelta(hours=9)
                      start_datetime = datetime.datetime(int(start_date_split[0]), int(start_date_split[1]), int(start_date_split[2])).strftime("%Y-%m-%d")
                      end_datetime = (datetime.datetime(int(end_date_split[0]), int(end_date_split[1]), int(end_date_split[2]))) + datetime.timedelta(hours=9)
                      end_datetime = datetime.datetime(int(end_date_split[0]), int(end_date_split[1]), int(end_date_split[2])).strftime("%Y-%m-%d")
                      event = {
                          'summary': title, # 일정 제목
                          'start': { # 시작 날짜
                              'date': start_datetime,
                              'timeZone': 'Asia/Seoul',
                          },
                          'end': { # 종료 날짜
                              'date': end_datetime,
                              'timeZone': 'Asia/Seoul',
                          },
                      }
                  # 시간 데이터를 입력 할 경우
                  else:
                      title_list = input_data[4:]
                      title = " ".join(title_list)
                      date_data = input_data[:4]
                      start_date_split = date_data[0].split("-")
                      start_time_split = date_data[1].split(":")
                      end_date_split = date_data[2].split("-")
                      end_time_split = date_data[3].split(":")
                      start_datetime = (datetime.datetime(int(start_date_split[0]), int(start_date_split[1]), int(start_date_split[2]), int(start_time_split[0]), int(start_time_split[1]), 0)) + datetime.timedelta(hours=9)
                      start_datetime = datetime.datetime(int(start_date_split[0]), int(start_date_split[1]), int(start_date_split[2]), int(start_time_split[0]), int(start_time_split[1]), 0).strftime("%Y-%m-%dT%H:%M:%S")
                      end_datetime = (datetime.datetime(int(end_date_split[0]), int(end_date_split[1]), int(end_date_split[2]), int(end_time_split[0]), int(end_time_split[1]), 0)) + datetime.timedelta(hours=9)
                      end_datetime = datetime.datetime(int(end_date_split[0]), int(end_date_split[1]), int(end_date_split[2]), int(end_time_split[0]), int(end_time_split[1]), 0).strftime("%Y-%m-%dT%H:%M:%S")
                      event = {
                          'summary': title, # 일정 제목
                          'start': { # 시작 날짜
                              'dateTime': start_datetime,
                              'timeZone': 'Asia/Seoul',
                          },
                          'end': { # 종료 날짜
                              'dateTime': end_datetime,
                              'timeZone': 'Asia/Seoul',
                          },
                      }
          # 구글 캘린더에 추가
          event = service.events().insert(calendarId='primary', body=event).execute()
          # 임베드에 표시할 이벤트 타이틀
          event_title = event.get('summary')
          # 임베드에 표시할 이벤트 기간
          value_data = f"{start_datetime} ~ {end_datetime}"
          # 임베드 생성
          embed = discord.Embed(title='Event created', description="", color = 0x00ff00)
          embed.add_field(name=event_title, value=value_data, inline=False)
          embed.add_field(name="Events Google Calendar Link", value=event.get('htmlLink'), inline=False)
          await ctx.send(embed=embed)

      # 일정 리스트 표시
      @commands.command()
      async def list(self, ctx, *, msg):
          # 구글 API 인증 코드
          creds = None
          if os.path.exists('token.json'):
              creds = Credentials.from_authorized_user_file('token.json', SCOPES)
          # If there are no (valid) credentials available, let the user log in.
          if not creds or not creds.valid:
              if creds and creds.expired and creds.refresh_token:
                  creds.refresh(Request())
              else:
                  flow = InstalledAppFlow.from_client_secrets_file(
                      'credentials.json', SCOPES)
                  creds = flow.run_local_server(port=0)
              # Save the credentials for the next run
              with open('token.json', 'w') as token:
                  token.write(creds.to_json())
          service = build('calendar', 'v3', credentials=creds)
          # 메세지 입력받음
          input_data = (msg.split(' '))
          # 입력값이 'today'일 경우
          if input_data[0] == 'today':
              # 반복문 결과를 저장 할 빈 리스트 선언
              event_list = []
              # 현재 시간의 년/월/일을 변수에 저장
              input_date = datetime.date.today().strftime("%Y-%m-%d")
              # 구글 캘린더에서 모든 이벤트를 불러 옴
              events_result = service.events().list(calendarId='primary', singleEvents=True, orderBy='startTime').execute()
              events = events_result.get('items', [])
              for event in events:
                  # 이벤트에서 이벤트의 시작 날짜를 가져옴
                  get_start_date = event.get('start').values()
                  # 이벤트에서 이벤트의 종료 날짜를 가져옴
                  get_end_date = event.get('end').values()
                  # 이벤트에서 가져온 날짜(사전형)를 문자열로 변환 후, 슬라이싱 해서 input_date와 형태를 맞춰줌(YYYY-MM-DD)
                  get_start_date_str = str(get_start_date)
                  start_date_str_slice = get_start_date_str[14:24]
                  get_end_date_str = str(get_end_date)
                  end_date_str_slice = get_end_date_str[14:24]
                  # input_date가 포함될 경우 실행
                  if start_date_str_slice <= input_date <= end_date_str_slice:
                      # 이벤트 시작 날짜/시간을 변수에 저장
                      start = event['start']
                      # 이벤트 종료 날짜/시간을 변수에 저장
                      end = event['end']
                      # 이벤트 시작/종료 날짜/시간을 문자열로 변환
                      start_date_str = str(start)
                      end_date_str = str(end)
                      # date와 dateTime일 경우 구분
                      # 이벤트가 date로 설정된 경우
                      if start_date_str[0:7] == "{'date'":
                          # 시간이 지정되어있지 않을 경우 시간은 표시하지 않음
                          start_date = start_date_str[10:-2]
                          start_time = '[time not set]'
                          # 시작 시간이 지정되어있지 않을 경우 종료 날짜 date와 datetime 구분
                          if end_date_str[0:7] == "{'date'":
                              end_date = end_date_str[10:-2]
                              end_time = '[time not set]'
                          else:
                              end_date = end_date_str[14:24]
                              end_time = end_date_str[25:33]
                      # 이벤트가 datetime으로 설정된 경우
                      else:
                          start_date = start_date_str[14:24]
                          start_time = start_date_str[25:33]
                          # 시작 시간이 지정되어있을 경우 종료 날짜 date와 datetime 구분
                          if end_date_str[0:7] == "{'date'":
                              end_date = end_date_str[10:-2]
                              end_time = '[time not set]'
                          else:
                              end_date = end_date_str[14:24]
                              end_time = end_date_str[25:33]
                      # 이벤트 시작 날짜, 시작 시간, 종료 날짜, 종료 시간, 이벤트명, 이벤트 아이디를 변수에 담아 리스트에 저장
                      dates = start_date, start_time, end_date, end_time, event['summary']
                      event_list.append(dates)
              # 이벤트가 없을 경우 메시지 출력
              if len(event_list) == 0:
                  # 임베드 생성
                  embed = discord.Embed(title='Event does not exist', description="", color = 0x00ff00)
              else:
                  # 임베드 생성
                  embed = discord.Embed(title='Event list', description="", color = 0x00ff00)
                  # 인덱스 번호 지정
                  for index, event in enumerate(event_list):
                      # 이벤트 이름 앞에 인덱스 번호 출력
                      event_title = f"{event[4]}"
                      # 이벤트 기간 표시
                      value_data = f"{event[0]} {event[1]} ~ {event[2]} {event[3]}"
                      # 임베드에 덧붙이기
                      embed.add_field(name=event_title, value=value_data, inline=False)

          # 입력값이 'month'일 경우
          if input_data[0] == 'month':
              # 반복문 결과를 저장 할 빈 리스트 선언
              event_list = []
              if len(input_data) == 2:
                  event_date = input_data[1].split('-')
                  input_date = datetime.datetime(int(event_date[0]), int(event_date[1]), 1).strftime("%Y-%m")
              else:
                  # 현재 시간의 년/월을 변수에 저장
                  input_date = datetime.date.today().strftime("%Y-%m")
              # 구글 캘린더에서 모든 이벤트를 불러 옴
              events_result = service.events().list(calendarId='primary', singleEvents=True, orderBy='startTime').execute()
              events = events_result.get('items', [])
              for event in events:
                  # 이벤트에서 이벤트의 시작 날짜를 가져옴
                  get_start_date = event.get('start').values()
                  # 이벤트에서 이벤트의 종료 날짜를 가져옴
                  get_end_date = event.get('end').values()
                  # 이벤트에서 가져온 날짜(사전형)를 문자열로 변환 후, 슬라이싱 해서 input_date와 형태를 맞춰줌(YYYY-MM)
                  get_start_date_str = str(get_start_date)
                  start_date_str_slice = get_start_date_str[14:21]
                  get_end_date_str = str(get_end_date)
                  end_date_str_slice = get_end_date_str[14:21]
                  # input date가 포함될 경우 실행
                  if start_date_str_slice <= input_date <= end_date_str_slice:
                      # 이벤트 시작 날짜/시간을 변수에 저장
                      start = event['start']
                      # 이벤트 종료 날짜/시간을 변수에 저장
                      end = event['end']
                      # 이벤트 시작/종료 날짜/시간을 문자열로 변환
                      start_date_str = str(start)
                      end_date_str = str(end)
                      # date와 dateTime일 경우 구분
                      # 이벤트가 date로 설정된 경우
                      if start_date_str[0:7] == "{'date'":
                          # 시간이 지정되어있지 않을 경우 시간은 표시하지 않음
                          start_date = start_date_str[10:-2]
                          start_time = '[time not set]'
                          # 시작 시간이 지정되어있지 않을 경우 종료 날짜 date와 datetime 구분
                          if end_date_str[0:7] == "{'date'":
                              end_date = end_date_str[10:-2]
                              end_time = '[time not set]'
                          else:
                              end_date = end_date_str[14:24]
                              end_time = end_date_str[25:33]
                      # 이벤트가 datetime으로 설정된 경우
                      else:
                          start_date = start_date_str[14:24]
                          start_time = start_date_str[25:33]
                          # 시작 시간이 지정되어있을 경우 종료 날짜 date와 datetime 구분
                          if end_date_str[0:7] == "{'date'":
                              end_date = end_date_str[10:-2]
                              end_time = '[time not set]'
                          else:
                              end_date = end_date_str[14:24]
                              end_time = end_date_str[25:33]
                      # 이벤트 시작 날짜, 시작 시간, 종료 날짜, 종료 시간, 이벤트명, 이벤트 아이디를 변수에 담아 리스트에 저장
                      dates = start_date, start_time, end_date, end_time, event['summary']
                      event_list.append(dates)
              # 이벤트가 없을 경우 메시지 출력
              if len(event_list) == 0:
                  # 임베드 생성
                  embed = discord.Embed(title='Event does not exist', description="", color = 0x00ff00)
              else:
                  # 임베드 생성
                  embed = discord.Embed(title='Event list', description="", color = 0x00ff00)
                  # 인덱스 번호 지정
                  for index, event in enumerate(event_list):
                      # 이벤트 이름 앞에 인덱스 번호 출력
                      event_title = f"{event[4]}"
                      # 이벤트 기간 표시
                      value_data = f"{event[0]} {event[1]} ~ {event[2]} {event[3]}"
                      # 임베드에 덧붙이기
                      embed.add_field(name=event_title, value=value_data, inline=False)

          # 입력값이 'year'일 경우
          if input_data[0] == 'year':
              # 반복문 결과를 저장 할 빈 리스트 선언
              event_list = []
              # 현재 시간의 년/월을 변수에 저장
              if len(input_data) == 2:
                  input_date = input_date = datetime.datetime(int(input_data[1]), 1, 1).strftime("%Y")
              else:
                  input_date = datetime.date.today().strftime("%Y")
              # 구글 캘린더에서 모든 이벤트를 불러 옴
              events_result = service.events().list(calendarId='primary', singleEvents=True, orderBy='startTime').execute()
              events = events_result.get('items', [])
              for event in events:
                  # 이벤트에서 이벤트의 시작 날짜를 가져옴
                  get_start_date = event.get('start').values()
                  # 이벤트에서 이벤트의 종료 날짜를 가져옴
                  get_end_date = event.get('end').values()
                  # 이벤트에서 가져온 날짜(사전형)를 문자열로 변환 후, 슬라이싱 해서 input_date와 형태를 맞춰줌(YYYY)
                  get_start_date_str = str(get_start_date)
                  start_date_str_slice = get_start_date_str[14:18]
                  get_end_date_str = str(get_end_date)
                  end_date_str_slice = get_end_date_str[14:18]
                  # input date가 포함될 경우 실행
                  if start_date_str_slice <= input_date <= end_date_str_slice:
                      # 이벤트 시작 날짜/시간을 변수에 저장
                      start = event['start']
                      # 이벤트 종료 날짜/시간을 변수에 저장
                      end = event['end']
                      # 이벤트 시작/종료 날짜/시간을 문자열로 변환
                      start_date_str = str(start)
                      end_date_str = str(end)
                      # date와 dateTime일 경우 구분
                      # 이벤트가 date로 설정된 경우
                      if start_date_str[0:7] == "{'date'":
                          # 시간이 지정되어있지 않을 경우 시간은 표시하지 않음
                          start_date = start_date_str[10:-2]
                          start_time = '[time not set]'
                          # 시작 시간이 지정되어있지 않을 경우 종료 날짜 date와 datetime 구분
                          if end_date_str[0:7] == "{'date'":
                              end_date = end_date_str[10:-2]
                              end_time = '[time not set]'
                          else:
                              end_date = end_date_str[14:24]
                              end_time = end_date_str[25:33]
                      # 이벤트가 datetime으로 설정된 경우
                      else:
                          start_date = start_date_str[14:24]
                          start_time = start_date_str[25:33]
                          # 시작 시간이 지정되어있을 경우 종료 날짜 date와 datetime 구분
                          if end_date_str[0:7] == "{'date'":
                              end_date = end_date_str[10:-2]
                              end_time = '[time not set]'
                          else:
                              end_date = end_date_str[14:24]
                              end_time = end_date_str[25:33]
                      # 이벤트 시작 날짜, 시작 시간, 종료 날짜, 종료 시간, 이벤트명, 이벤트 아이디를 변수에 담아 리스트에 저장
                      dates = start_date, start_time, end_date, end_time, event['summary']
                      event_list.append(dates)
              # 이벤트가 없을 경우 메시지 출력
              if len(event_list) == 0:
                  # 임베드 생성
                  embed = discord.Embed(title='Event does not exist', description="", color = 0x00ff00)
              else:
                  # 임베드 생성
                  embed = discord.Embed(title='Event list', description="", color = 0x00ff00)
                  # 인덱스 번호 지정
                  for index, event in enumerate(event_list):
                      # 이벤트 이름 앞에 인덱스 번호 출력
                      event_title = f"{event[4]}"
                      # 이벤트 기간 표시
                      value_data = f"{event[0]} {event[1]} ~ {event[2]} {event[3]}"
                      # 임베드에 덧붙이기
                      embed.add_field(name=event_title, value=value_data, inline=False)

          # 년/월/일 모두 입력할 경우
          # 입력값의 첫 번째 문자가 숫자일 경우 실행
          if input_data[0][0].isdigit() == True:
              # 반복문 결과를 저장 할 빈 리스트 선언
              event_list = []
              # 입력값을 datetime 형태로 변환하기 위해 int형으로 변환
              data_split = input_data[0].split('-')
              # 입력값을 datetime 형태로 변환
              input_date = datetime.datetime(int(data_split[0]), int(data_split[1]), int(data_split[2])).strftime("%Y-%m-%d")
              # 구글 캘린더에서 모든 이벤트를 불러 옴
              events_result = service.events().list(calendarId='primary', singleEvents=True, orderBy='startTime').execute()
              events = events_result.get('items', [])
              for event in events:
                  # 이벤트에서 이벤트의 시작 날짜를 가져옴
                  get_start_date = event.get('start').values()
                  # 이벤트에서 이벤트의 종료 날짜를 가져옴
                  get_end_date = event.get('end').values()
                  # 이벤트에서 가져온 날짜(사전형)를 문자열로 변환 후, 슬라이싱 해서 input_date와 형태를 맞춰줌(YYYY)
                  get_start_date_str = str(get_start_date)
                  start_date_str_slice = get_start_date_str[14:24]
                  get_end_date_str = str(get_end_date)
                  end_date_str_slice = get_end_date_str[14:24]
                  # input date가 포함될 경우 실행
                  if start_date_str_slice <= input_date <= end_date_str_slice:
                      # 이벤트 시작 날짜/시간을 변수에 저장
                      start = event['start']
                      # 이벤트 종료 날짜/시간을 변수에 저장
                      end = event['end']
                      # 이벤트 시작/종료 날짜/시간을 문자열로 변환
                      start_date_str = str(start)
                      end_date_str = str(end)
                      # date와 dateTime일 경우 구분
                      # 이벤트가 date로 설정된 경우
                      if start_date_str[0:7] == "{'date'":
                          # 시간이 지정되어있지 않을 경우 시간은 표시하지 않음
                          start_date = start_date_str[10:-2]
                          start_time = '[time not set]'
                          # 시작 시간이 지정되어있지 않을 경우 종료 날짜 date와 datetime 구분
                          if end_date_str[0:7] == "{'date'":
                              end_date = end_date_str[10:-2]
                              end_time = '[time not set]'
                          else:
                              end_date = end_date_str[14:24]
                              end_time = end_date_str[25:33]
                      # 이벤트가 datetime으로 설정된 경우
                      else:
                          start_date = start_date_str[14:24]
                          start_time = start_date_str[25:33]
                          # 시작 시간이 지정되어있을 경우 종료 날짜 date와 datetime 구분
                          if end_date_str[0:7] == "{'date'":
                              end_date = end_date_str[10:-2]
                              end_time = '[time not set]'
                          else:
                              end_date = end_date_str[14:24]
                              end_time = end_date_str[25:33]
                      # 이벤트 시작 날짜, 시작 시간, 종료 날짜, 종료 시간, 이벤트명, 이벤트 아이디를 변수에 담아 리스트에 저장
                      dates = start_date, start_time, end_date, end_time, event['summary']
                      event_list.append(dates)        
              # 이벤트가 없을 경우 메시지 출력
              if len(event_list) == 0:
                  # 임베드 생성
                  embed = discord.Embed(title='Event does not exist', description="", color = 0x00ff00)
              else:
                  # 임베드 생성
                  embed = discord.Embed(title='Event list', description="", color = 0x00ff00)
                  # 인덱스 번호 지정
                  for index, event in enumerate(event_list):
                      # 이벤트 이름 앞에 인덱스 번호 출력
                      event_title = f"{index+1}. {event[4]}"
                      # 이벤트 기간 표시
                      value_data = f"{event[0]} {event[1]} ~ {event[2]} {event[3]}"
                      # 임베드에 덧붙이기
                      embed.add_field(name=event_title, value=value_data, inline=False)
          # 임베드 전송
          await ctx.send(embed=embed)

      # 일정 업데이트
      @commands.command()
      async def update(self, ctx, *, msg):
          # 구글 API 인증 코드
          creds = None
          if os.path.exists('token.json'):
              creds = Credentials.from_authorized_user_file('token.json', SCOPES)
          # If there are no (valid) credentials available, let the user log in.
          if not creds or not creds.valid:
              if creds and creds.expired and creds.refresh_token:
                  creds.refresh(Request())
              else:
                  flow = InstalledAppFlow.from_client_secrets_file(
                      'credentials.json', SCOPES)
                  creds = flow.run_local_server(port=0)
              # Save the credentials for the next run
              with open('token.json', 'w') as token:
                  token.write(creds.to_json())
          service = build('calendar', 'v3', credentials=creds)
          # 메세지 입력받음
          input_data = (msg.split(' '))
          # 입력 메세지를 공백으로 구분
          start_year = int(input_data[0].split('-')[0])
          start_month = int(input_data[0].split('-')[1])
          start_date = int(input_data[0].split('-')[2])
          # 반복문 결과를 저장 할 빈 리스트 선언
          event_list = []
          # index 번호
          num = int(input_data[1])
          # 업데이트 할 이벤트 타이틀
          update_title_list = input_data[2:]
          # title_list에 담긴 문자열들을 합침
          update_title = " ".join(update_title_list)
          # 입력값을 datetime 형태로 변환
          input_date = datetime.date(start_year, start_month, start_date).strftime("%Y-%m-%d")
          # 캘린더에서 이벤트 리스트를 불러옴
          events_result = service.events().list(calendarId='primary', singleEvents=True, orderBy='startTime').execute()
          events = events_result.get('items', [])
          for event in events:
              # 이벤트에서 이벤트의 시작 날짜를 가져옴
              get_start_date = event.get('start').values()
              # 이벤트에서 이벤트의 종료 날짜를 가져옴
              get_end_date = event.get('end').values()
              # 이벤트에서 가져온 날짜(사전형)를 문자열로 변환 후, 슬라이싱 해서 input_date와 형태를 맞춰줌(YYYY-MM-DD)
              get_start_date_str = str(get_start_date)
              start_date_str_slice = get_start_date_str[14:24]
              get_end_date_str = str(get_end_date)
              end_date_str_slice = get_end_date_str[14:24]
              # input date가 포함될 경우 실행
              if start_date_str_slice <= input_date <= end_date_str_slice:
                  # 이벤트 시작 날짜/시간을 변수에 저장
                  start = event['start']
                  # 이벤트 종료 날짜/시간을 변수에 저장
                  end = event['end']
                  # 이벤트 시작/종료 날짜/시간을 문자열로 변환
                  start_date_str = str(start)
                  end_date_str = str(end)
                  # date와 dateTime일 경우 구분
                  # 이벤트가 date로 설정된 경우
                  if start_date_str[0:7] == "{'date'":
                      # 시간이 지정되어있지 않을 경우 시간은 표시하지 않음
                      start_date = start_date_str[10:-2]
                      start_time = '[time not set]'
                      # 시작 시간이 지정되어있지 않을 경우 종료 날짜 date와 datetime 구분
                      if end_date_str[0:7] == "{'date'":
                          end_date = end_date_str[10:-2]
                          end_time = '[time not set]'
                      else:
                          end_date = end_date_str[14:24]
                          end_time = end_date_str[25:33]
                  # 이벤트가 datetime으로 설정된 경우
                  else:
                      start_date = start_date_str[14:24]
                      start_time = start_date_str[25:33]
                      # 시작 시간이 지정되어있을 경우 종료 날짜 date와 datetime 구분
                      if end_date_str[0:7] == "{'date'":
                          end_date = end_date_str[10:-2]
                          end_time = '[time not set]'
                      else:
                          end_date = end_date_str[14:24]
                          end_time = end_date_str[25:33]
                  # 이벤트 시작 날짜, 시작 시간, 종료 날짜, 종료 시간, 이벤트명, 이벤트 아이디를 변수에 담아 리스트에 저장
                  dates = start_date, start_time, end_date, end_time, event['summary'], event['id']
                  event_list.append(dates)
          # 임베드에 표시 할 인덱스 번호, 업데이트 전 이벤트명, 업데이트 후 이벤트명, 이벤트 시간을 선언(코드 추가를 통해 업데이트 가능한 내용을 추가할 경우 해당 내용도 임베드에 표시)
          embed_start_date = event_list[num-1][0]
          embed_start_time = event_list[num-1][1]
          embed_end_date = event_list[num-1][2]
          embed_end_time = event_list[num-1][3]
          value_data = f"{embed_start_date} {embed_start_time} ~ {embed_end_date} {embed_end_time}"
          event_title = f"{num}. {event_list[num-1][4]}"
          updated_title = f"{num}. {update_title}"

          events = event_list
          # 사용자가 입력한 번호에 맞는 인덱스 번호의 이벤트 아이디를 변수에 저장
          event_id = (events[num-1])[5]
          # 변수에 저장된 이벤트 아이디를 통해 해당 이벤트를 불러옴
          event = service.events().get(calendarId='primary', eventId=event_id).execute()
          # 불러온 이벤트에서 수정 항목을 설정
          event['summary'] = update_title
          # 수정된 항목을 body에 넣고 수정
          service.events().update(calendarId='primary', eventId=event_id, body=event).execute()
          # 임베드 생성
          embed = discord.Embed(title='Event updated', description="", color = 0x00ff00)
          # 변경 전 이벤트 내용
          embed.add_field(name=event_title, value=value_data, inline=False)
          embed.add_field(name='is updated to', value='\b', inline=False)
          # 변경 후 이벤트 내용
          embed.add_field(name=updated_title, value=value_data, inline=False)
          # 임베드 전송
          await ctx.send(embed=embed)

      # 일정 삭제
      @commands.command()
      async def delete(self, ctx, msg1, msg2):
          # 구글 API 인증 코드
          creds = None
          if os.path.exists('token.json'):
              creds = Credentials.from_authorized_user_file('token.json', SCOPES)
          # If there are no (valid) credentials available, let the user log in.
          if not creds or not creds.valid:
              if creds and creds.expired and creds.refresh_token:
                  creds.refresh(Request())
              else:
                  flow = InstalledAppFlow.from_client_secrets_file(
                      'credentials.json', SCOPES)
                  creds = flow.run_local_server(port=0)
              # Save the credentials for the next run
              with open('token.json', 'w') as token:
                  token.write(creds.to_json())
          service = build('calendar', 'v3', credentials=creds)
          # 삭제 할 이벤트가 포함 된 날짜(년/월/일) 입력
          start_year, start_month, start_date = map(int, msg1.split('-'))
          # 반복문 결과를 저장 할 빈 리스트 선언
          event_list = []
          # index 번호를 선택할 변수 num 선언 후 int형으로 변환
          num = int(msg2)
          # 입력값을 datetime 형태로 변환
          input_date = datetime.date(start_year, start_month, start_date).strftime("%Y-%m-%d")
          # 캘린더에서 이벤트 리스트를 불러옴
          events_result = service.events().list(calendarId='primary', singleEvents=True, orderBy='startTime').execute()
          events = events_result.get('items', [])
          for event in events:
              # 이벤트에서 이벤트의 시작 날짜를 가져옴
              get_start_date = event.get('start').values()
              # 이벤트에서 이벤트의 종료 날짜를 가져옴
              get_end_date = event.get('end').values()
              # 이벤트에서 가져온 날짜(사전형)를 문자열로 변환 후, 슬라이싱 해서 input_date와 형태를 맞춰줌(YYYY-MM-DD)
              get_start_date_str = str(get_start_date)
              start_date_str_slice = get_start_date_str[14:24]
              get_end_date_str = str(get_end_date)
              end_date_str_slice = get_end_date_str[14:24]
              # input date가 포함될 경우 실행
              if start_date_str_slice <= input_date <= end_date_str_slice:
                  # 이벤트 시작 날짜/시간을 변수에 저장
                  start = event['start']
                  # 이벤트 종료 날짜/시간을 변수에 저장
                  end = event['end']
                  # 이벤트 시작/종료 날짜/시간을 문자열로 변환
                  start_date_str = str(start)
                  end_date_str = str(end)
                  # date와 dateTime일 경우 구분
                  # 이벤트가 date로 설정된 경우
                  if start_date_str[0:7] == "{'date'":
                      # 시간이 지정되어있지 않을 경우 시간은 표시하지 않음
                      start_date = start_date_str[10:-2]
                      start_time = '[time not set]'
                      # 시작 시간이 지정되어있지 않을 경우 종료 날짜 date와 datetime 구분
                      if end_date_str[0:7] == "{'date'":
                          end_date = end_date_str[10:-2]
                          end_time = '[time not set]'
                      else:
                          end_date = end_date_str[14:24]
                          end_time = end_date_str[25:33]
                  # 이벤트가 datetime으로 설정된 경우
                  else:
                      start_date = start_date_str[14:24]
                      start_time = start_date_str[25:33]
                      # 시작 시간이 지정되어있을 경우 종료 날짜 date와 datetime 구분
                      if end_date_str[0:7] == "{'date'":
                          end_date = end_date_str[10:-2]
                          end_time = '[time not set]'
                      else:
                          end_date = end_date_str[14:24]
                          end_time = end_date_str[25:33]
                  # 이벤트 시작 날짜, 시작 시간, 종료 날짜, 종료 시간, 이벤트명, 이벤트 아이디를 변수에 담아 리스트에 저장
                  dates = start_date, start_time, end_date, end_time, event['summary'], event['id']
                  event_list.append(dates)
          # 임베드에 표시 할 삭제 된 이벤트의 인덱스 번호와 이벤트명, 이벤트 시간
          event_title = f"{num}. {event_list[num-1][4]}"
          embed_start_date = event_list[num-1][0]
          embed_start_time = event_list[num-1][1]
          embed_end_date = event_list[num-1][2]
          embed_end_time = event_list[num-1][3]
          value_data = f"{embed_start_date} {embed_start_time} ~ {embed_end_date} {embed_end_time}"
          events = event_list
          # 사용자가 입력한 번호에 맞는 인덱스 번호의 이벤트 아이디를 변수에 저장
          event_id = (events[num-1])[5]
          # 변수에 저장된 이벤트 아이디를 통해 해당 이벤트를 삭제
          service.events().delete(calendarId='primary', eventId=event_id).execute()
          # 임베드 생성
          embed = discord.Embed(title='Event deleted', description="", color = 0x00ff00)
          embed.add_field(name=event_title, value=value_data, inline=False)
          # 임베드 전송
          await ctx.send(embed=embed)

def setup(client):
      client.add_cog(Google_calendar(client))
