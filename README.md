# 디스코드 ERP 멀린 봇 AI-WEB development 앱 서버 

## 이 팀 프로젝트는 1조 성배를 찾아나서는 아서왕의 기사단들에게서 생성 되었습니다.

멀린 봇 장고 웹서버로 구현한 사이트  [멀린 웹 서버 링크!](https://merlindc.click/)

멀린봇 장고 웹서버 대외용 원격저장소 : [원격 저장소 링크!](https://github.com/joneheart/merlin_webserver)

멀린봇 디스코드 초대 링크 : [디스코드에 초대하기 링크!](https://discord.com/api/oauth2/authorize?client_id=950766027535421460&permissions=8&scope=applications.commands%20bot)

For a detailed description of the bot, see this [Video](https://youtu.be/vVbSRfmq_n8).



## 1조 멀린 개발 인원 (5명)

* Team Leader :
    - 조시욱 깃-허브 [Click](https://github.com/github01main)
    - 개발 업무 포지션 : 멀린앱 플레이어, 엑셀, 캘린더 초기 코드 작성 및 업무 전반 프로그레스 마일스톤 기획 및 보안 관련 이슈, 팀원들 교육.
    - ex) 소스코드 예제 작성 후 데모 버전 실행, 업무 효율성을 위해 장고 프로젝트용 자동화 파워쉘 작성 후 배포. 
* Team Members :
    - 윤정기 깃-허브 [Click](https://github.com/lution88)
    - 개발 업무 포지션 : 멀린앱 플레이어 개발 및 테스트 디버깅 후 디스코드 API 로우 코드 셀레니움 로우 코드 적용, 멀린 봇 배포 버전 패키징.
    - 이성호 깃-허브 [Click](https://github.com/Hosio123)
    - 개발 업무 포지션 : GCP(구글클라우드플랫폼)을 이용한 캘린더 공유 및 생성 삭제 리스트 등 calendar API, discord API 크로스플랫폼 데이터 전송 연동 및 배포 버전 패키징.
    - ex) JWT(jason web token)발행 후 멀린 봇이 업로드 되어있는 중간경로 헤로쿠 서버에 쿼리 헤로쿠 서버에서 브릿지를 통하여 GCP에 캘린더 데이터 쿼리 후 디스코드 채널로 재귀.
    - 정심일 깃-허브 [Click](https://github.com/joneheart)
    -
    - ex)
    - 김 &nbsp;&nbsp; 호 깃-허브 [Click](https://github.com/hopaom)
    -
    - ex)


### 개발의도 -

스파르타 코딩 교육 AI웹개발 파이널 프로젝트 전산형 관리 시스템 봇 '멀린'을 제작한 1조 성배를 찾아나서는 아서왕의 기사단들 입니다.
아이디어의 시작은 1~10명 정도의 사업장을 지닌 스타트업이나 마이크로 기업을 상대로 단순한 출퇴근관리나 사내 출입대장 명부, 직원 관리부를 
브라우저 데스크탑 모바일에서도 편하게 장소에 구애받지않고 받아볼수 없을까에서 시작하였습니다.

### 개발 이전 사전 조사 -

그 중 단연 눈에 먼저 띄게 된것은 '디스코드'였습니다. VOIP중 가장 낮은 LATENCY를 가지고 있으며,
젊은 세대층들이 자주 커뮤니티 서버나 게임을 할때 보이스 또는 텍스트채팅을 애용하고있는 시점이기 때문입니다.
'디스코드'에 대한 사전 시장 및 회사 이력을 조사하였고, 디스코드를 마케팅 및 사내 커뮤니티용으로 
애용하는 대표적인 회사 사례로 남녀노소 다 아시는 Youtube, Hammer & Chisel *(디스코드 유한회사로 변경전 이름), 
Epic Games(콘솔 및 PC용 전문 물리엔진 및 세계 잼민들의 마음을 사로잡은 포트나이트 제작 회사)가 있습니다.


### 개발 이전 심층 조사 -

Electron 베이스로 제작이되었으며 디스코드보다 먼저 제작된 동종 앱으로써는
피그마,노션,슬랙,트위치,스포티파이PC버전등이 있음으로 수명이 짧은 소프트웨어들 사이에서 베이스 프레임워크가 
기반이 탄탄하지 않나라는 생각하였으며, 유저 커뮤니티 기반으로 앱이 제작되었으니 장고웹 서버 또한 앱에 대한
공식 홈페이지 처럼 제작하면 되지 않을까란 생각하였고, 전산형 기능을 앱에 추가하고 그 내용을 웹사이트에
작성 후 피드백 및 후원계좌를 넣는 느낌으로 프로젝트의 방향성을 잡게되었습니다.

### 작업 프로그레스 -

이번 프로젝트를 진행하기 앞서 크로스 플랫폼 지향적인 데이터 협조방식을 바탕으로 전산형 관리 시스템 봇 제작에 도입을
해보자는 취지로 임하였습니다. 예를들어 1차로 데이터를 요청하는 장소는 디스코드 서버이며 디스코드 API로 유저가 원하는
데이터 형식을 AWS S3또는 GCP Calendar에서 디스코드 서버 채팅채널 공간안으로 가져와 보여주는 방식이였습니다.
