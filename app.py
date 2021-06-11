import tidalapi, webbrowser, login, pywinauto, pprint, time, datetime, important
from pypresence import Presence

def openUrl(func):
    url = func.split(" ")[1]
    print("Waiting...")
    webbrowser.open('https://' + url)

def nowPlaying():
    while True:
        try:
            windows = pywinauto.Desktop(backend="uia").windows(process=20024)
            title, artist = windows[0].window_text().split(" - ")
            return title, artist
        except ValueError:
            time.sleep(0.1)
        except IndexError:
            time.sleep(0.1)

def getInfo(t, a):
    track = session.search('track', t, limit=50)
    for i in track.tracks:
        if a == i.artist.name:
            track = session.get_track(i.id)
            album = i.album
            return track, album

client_id = important.clientId
RPC = Presence(client_id)
RPC.connect()

session = tidalapi.Session()
session.load_oauth_session(login.sessionId, login.tokenType, login.accessToken)

if not session.check_login():
    session.login_oauth_simple(function=openUrl)    
    with open('login.py', 'w') as login:
        login.write(f'sessionId = "{session.session_id}"')
        login.write(f'tokenType = "{session.token_type}"')
        login.write(f'accessToken = "{session.access_token}"')


print("Welcome Back".center(20, "*"), end="\n\n")
title = ""
artist = ""

while True:
    try:
        if nowPlaying()[0] != title:
            title, artist = nowPlaying()
            playing = f"Now playing: {title} - {artist}"
            track, album = getInfo(title, artist)
            today = datetime.datetime.today()
            startTime = datetime.datetime.now().timestamp()
            endTime = startTime + track.duration
            print(playing)
            print("=" * len(playing), end="\n\n")
            RPC.update(pid=20024, state=artist, details=title, start=int(startTime), end=int(endTime), large_image="artasset1", buttons=important.buttons)
        else:
            time.sleep(1)
    except KeyboardInterrupt:
        exit("Goodbye".center(20, "*"))