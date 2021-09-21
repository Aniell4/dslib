from typing import Tuple, Union
import httpx, os, random, string, time, base64
from dataclasses import dataclass

@dataclass
class Response: # dataclasses are pretty cool imo, alr have __repr__ in them, so it will show Like <Response {code=200, text='blablabla', json={'gay': 'true'}}>
    code: int; text: str
    json: dict = None

class Client(httpx.Client):
    def __init__(s, Token: str):
        '''Discord REST API wrapper.'''
        super().__init__()
        s.headers = GetNewHeaders(Token)
    # https://discord.com/developers/docs/resources/user#get-current-user
    def GetCurrentUser(s):
        '''Argless User Profile Call'''
        return s.GET('/users/@me')
    # https://discord.com/developers/docs/resources/invite#get-invite
    def InviteInfo(s, Invite: str):
        '''Only accepts a sanitized code currently.'''
        return s.GET(f'/invites/{Invite}?with_counts=true&with_expiration=true')
    def JoinInvite(s, Invite: str):
        '''Only accepts a sanitized code currently.'''
        Overwrite = {'x-context-properties': 'eyJsb2NhdGlvbiI6Ik1hcmtkb3duIExpbmsifQ=='}
        return s.POST(f'/invites/{Invite}', headers = Overwrite)
    def SendMessage(s, Channel: str, **Message):
        '''Requires ChannelId, Use keyword args to pass in msg dict data.'''
        Payload = {"nonce": "".join(random.choice(string.digits) for _ in range(18)), "tts": False}
        Payload.update(Message); return s.POST(f'/channels/{Channel}/messages', json = 
            Payload, headers = {'referer': f'https://discord.com/channels/@me/{Channel}'})
    def CreateDM(s, User: str):
        '''Requires UserId'''
        return s.POST('/users/@me/channels', json = {'recipients': [User]})
    def AddUserById(s, UserId: str):
        '''Accepts UserIds as strings'''
        Overwrite = {'x-context-properties': 'eyJsb2NhdGlvbiI6IlVzZXIgUHJvZmlsZSJ9'}
        return s.PUT(f'/users/@me/relationships/{UserId}', json = {}, headers = Overwrite)
    def AddUserByTag(s, UserTag: str):
        '''Accepts usertags as strings'''
        Username, Tag = UserTag.split('#')
        Overwrite = {'x-context-properties': 'eyJsb2NhdGlvbiI6IkFkZCBGcmllbmQifQ=='}
        return s.POST(f'/users/@me/relationships', json = {"username": Username, 
            "discriminator": int(Tag)}, headers = Overwrite)
    def SetUsername(s, Username: str, Password: str): 
        '''Update Username, Requires Account Password'''
        return s.PATCH('/users/@me', json = {'username': Username, 'password': Password})
    def SetAvatar(s, Picture):
        '''Update User Avatar with either a Img URL or Local File Object'''
        return s.PATCH('/users/@me', json = {'avatar': ResolveImage(Picture)}, timeout = 100)
    def SetAboutMe(s, BioText):
        '''Update User About me'''
        return s.PATCH('/users/@me', json = {'bio': BioText})
    def SetHypesquad(s, HypesquadNum: int):
        '''Update Hypesquad, Accepts Values from 1 to 3'''
        return s.POST('/hypesquad/online', json = {'house_id': HypesquadNum})
    # Common Methods
    def GET(s, Path, *Args, **Kwargs):
        '''GET Request using GenReq. Returns Code, Data.'''
        return s.GenReq(s.get, Path, *Args, **Kwargs)
    def POST(s, Path, *Args, **Kwargs):
        '''POST Request using GenReq. Returns Code, Data.'''
        return s.GenReq(s.post, Path, *Args, **Kwargs)
    def PUT(s, Path, *Args, **Kwargs):
        '''PUT Request using GenReq. Returns Code, Data.'''
        return s.GenReq(s.put, Path, *Args, **Kwargs)
    def DELETE(s, Path, *Args, **Kwargs):
        '''DELETE Request using GenReq. Returns Code, Data.'''
        return s.GenReq(s.delete, Path, *Args, **Kwargs)
    def PATCH(s, Path, *Args, **Kwargs):
        '''PATCH Request using GenReq. Returns Code, Data.'''
        return s.GenReq(s.patch, Path, *Args, **Kwargs)
    def GenReq(s, Method, Path, *Args, **Kwargs) -> Response:
        '''General Purpose API Request Function. Requires a Method and Path. Returns the Status Code, Body.'''
        Y = Method(API(Path), *Args, **Kwargs)
        Code, Data = Y.status_code, Y.json() if Y.headers \
            ['content-type'] == 'application/json' else None
        if Code == 429:
            time.sleep(1 + Data['retry_after'] // 995)
            return s.GenReq(Method, Path, *Args, **Kwargs)
        elif Code >= 500:
            print('Server error!!')
        elif Code >= 400:
            print(f'Code ({Code}) on', Path, 'using Token:', s.headers['authorization'])
            if Data and 'message' in Data:
                print('\tInfo:', Data['message'])
            else:
                print('\tUnk:', Y.text)
        return Response(Code, Y.text, Data)

# Helper Functions
def API(URL) -> str:
    '''Resource Path -> Full Discord API URL'''
    return "https://discord.com/api/v9" + URL

def GetNewHeaders(Token, Referer='https://discord.com/channels/@me'):
    '''Returns Basic Session Headers'''
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
    '''Strings are resolved remotely, File objects locally. Base64 is returned.'''
    Body = httpx.get(Var).content if isinstance(Var, str) else Var.read()
    return "data:image/png;base64," + base64.b64encode(Body).decode('utf-8')

def RandomX(Length):
    '''Legacy Garbage Hex Function'''
    return os.urandom(Length).hex()[Length:]
# Run Stuff

TOKEN = "ODg5NjM3NzY1MDIzNjgyNjIy.YUkJvQ.d5L6ZxW8JlfEAjdJlYOPK4RhSBc"
# locked token ODg5NjM3NzU3MjcyNjE2OTYw.YUkJuw.hljp4-vZ7_ifhgmYcAllZbs3YoE

C = Client(TOKEN)
print(C.GetCurrentUser())
C.SetAboutMe('sussy baka')
print(C.GetCurrentUser())