import httpx, os, random, string, time, base64

TOKEN = "ODg5NjM3NzY1MDIzNjgyNjIy.YUkJvQ.d5L6ZxW8JlfEAjdJlYOPK4RhSBc"
# locked token ODg5NjM3NzU3MjcyNjE2OTYw.YUkJuw.hljp4-vZ7_ifhgmYcAllZbs3YoE

def API(URL):
    return "https://discord.com/api/v9" + URL

class Client(httpx.Client):
    def __init__(s, Token):
        super().__init__()
        s.headers = GetNewHeaders(Token)
    # https://discord.com/developers/docs/resources/user#get-current-user
    def GetCurrentUser(s):
        return s.GET('/users/@me')
    # https://discord.com/developers/docs/resources/invite#get-invite
    def InviteInfo(s, Invite):
        return s.GET(f'/invites/{Invite}?with_counts=true&with_expiration=true')
    def JoinInvite(s, Invite):
        Overwrite = {'x-context-properties': 'eyJsb2NhdGlvbiI6Ik1hcmtkb3duIExpbmsifQ=='}
        return s.POST(f'/invites/{Invite}', headers = Overwrite)
    def SendMessage(s, Channel, **Message):
        Payload = {"nonce": "".join(random.choice(string.digits) for _ in range(18)), "tts": False}
        Payload.update(Message); return s.POST(f'/channels/{Channel}/messages', json = 
            Payload, headers = {'referer': f'https://discord.com/channels/@me/{Channel}'})
    def CreateDM(s, User):
        return s.POST('/users/@me/channels', json = {'recipients': [User]})
    def AddUserById(s, UserId):
        Overwrite = {'x-context-properties': 'eyJsb2NhdGlvbiI6IlVzZXIgUHJvZmlsZSJ9'}
        return s.PUT(f'/users/@me/relationships/{UserId}', json = {}, headers = Overwrite)
    def AddUserByTag(s, UserTag):
        Username, Tag = UserTag.split('#')
        Overwrite = {'x-context-properties': 'eyJsb2NhdGlvbiI6IkFkZCBGcmllbmQifQ=='}
        return s.POST(f'/users/@me/relationships', json = {"username": Username, 
            "discriminator": int(Tag)}, headers = Overwrite)
    def SetUsername(s, Username, Password):
        return s.PATCH('/users/@me', json = {'username': Username, 'password': Password})
    def SetAvatar(s, Picture):
        return s.PATCH('/users/@me', json = {'avatar': ResolveImage(Picture)}, timeout = 100)
    # Common Methods
    def GET(s, Path, *Args, **Kwargs):
        return s.GenReq(s.get, Path, *Args, **Kwargs)
    def POST(s, Path, *Args, **Kwargs):
        return s.GenReq(s.post, Path, *Args, **Kwargs)
    def PUT(s, Path, *Args, **Kwargs):
        return s.GenReq(s.put, Path, *Args, **Kwargs)
    def DELETE(s, Path, *Args, **Kwargs):
        return s.GenReq(s.delete, Path, *Args, **Kwargs)
    def PATCH(s, Path, *Args, **Kwargs):
        return s.GenReq(s.patch, Path, *Args, **Kwargs)
    def GenReq(s, Method, Path, *Args, **Kwargs):
        Y = Method(API(Path), *Args, **Kwargs)
        Code, Data = Y.status_code, Y.json() if Y.headers \
            ['content-type'] == 'application/json' else Y.text
        if Code == 429:
            time.sleep(1 + Data['retry_after'] // 995)
            return s.GenReq(Method, Path, *Args, **Kwargs)
        elif Code >= 500:
            print('Server error!!')
        elif Code >= 400:
            print(f'Code ({Code}) on', Path, 'using Token:', s.headers['authorization'])
            if 'message' in Data:
                print('\tInfo:', Data['message'])
        return Code, Data

def GetNewHeaders(Token, Referer='https://discord.com/channels/@me'):
    Cookies = [
        ('locale', 'en-GB'),
        ('__dcfduid', RandomX(43)), ('__sdcfduid', RandomX(96)),
        ('__stripe_mid', "-".join(map(RandomX, (18, 4, 4, 4, 18)))),
        ('__cfruid', RandomX(40)+'-'+"".join
            (random.choice(string.digits) for _ in range(10))),
    ]; return {
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate',
        'accept-language': 'en-GB',
        'origin': 'https://discord.com',
        'sec-fetch-dest': 'empty', 
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'authorization': Token, 'referer': Referer,
        'cookie': "; ".join(map("=".join, Cookies)),
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/0.1.9 Chrome/83.0.4103.122 Electron/9.4.4 Safari/537.36',
        'x-super-properties': 'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiRGlzY29yZCBDbGllbnQiLCJyZWxlYXNlX2NoYW5uZWwiOiJzdGFibGUiLCJjbGllbnRfdmVyc2lvbiI6IjAuMS45Iiwib3NfdmVyc2lvbiI6IjEwLjAuMTc3NjMiLCJvc19hcmNoIjoieDY0Iiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiY2xpZW50X2J1aWxkX251bWJlciI6OTM1NTQsImNsaWVudF9ldmVudF9zb3VyY2UiOm51bGx9',
        'x-debug-options': 'bugReporterEnabled',
    }

def ResolveImage(Var):
    Body = httpx.get(Var).content if isinstance(Var, str) else Var.read()
    return "data:image/png;base64," + base64.b64encode(Body).decode('utf-8')

def RandomX(Length):
	return os.urandom(Length).hex()[Length:]
# Run Stuff

C = Client(TOKEN)
#print(C.SetAvatar('https://cdn.discordapp.com/attachments/888212518437273671/889949943345856532/EbB8Y_aU8AMkI8m.png'))
#print(C.GetCurrentUser())
#print(C.SetUsername('Village Rapist', 'LmfaoFuckDiscord123!'))
# print(C.AddUserByTag('Aniell4#0429'))
# Code, Data = C.AddUserById('884763385483374662')
# code, data = C.CreateDM('884763385483374662')
# print(code, data)
C.SendMessage('889930594086162495', content = "Hi!")
# print(C.JoinInvite('5EYE7wap'))
