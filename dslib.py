from typing import Tuple, Union
import httpx, os, random, string, time, base64
from dataclasses import dataclass

@dataclass
class Response: # dataclasses are pretty cool imo, alr have __repr__ in them, so it will show Like <Response {code=200, text='blablabla', json={'gay': 'true'}}>
    code: int; text: str
    json: dict = None

import structs.channel as channel
class Channel(channel.Channel):
    Store = {}
    def __init__(s, obj):
        super().__init__(obj)
        Channel.Store[s.id] = s
    def get_messages(s, Before: str = '', Prev = None):
        Params = {'limit': 100}
        if Before:
                Params['before'] = Before
        R = Client.Instance.GET(f'/channels/{s.id}/messages', params = Params)
        First = None
        for Msg in R.json:
            Obj = Message(Msg)
            Obj.channel = s
            if Prev:
                Prev._nextMsgPtr_ = Obj
            else:
                First = Obj
            Prev = Obj
        if len(R.json) < 100:
            Prev._nextMsgPtr_ = None
        return First
    def send_message(s, **MsgData):
        Payload = {"nonce": "".join(random.choice(string.digits) for _ in range(18)), "tts": False}
        Payload.update(MsgData); res = Client.Instance.POST \
            (f'/channels/{s.id}/messages', json = Payload, headers = 
            {'referer': f'https://discord.com/channels/@me/{s.id}'})
        if res.code == 200:
            return Message(res.json)
        raise Exception("Unable to Create Message")

import structs.message as message
class Message(message.Message):
    def __init__(s, obj):
        super().__init__(obj)
        s._nextMsgPtr_ = -1
    def next_message(s):
        if s._nextMsgPtr_:
            if s._nextMsgPtr_ != -1:
                return s._nextMsgPtr_
            else:
                return s.channel.get_messages(s.id, s)
    def delete(s):
        return Client.Instance.DELETE \
            (f'/channels/{s.channel_id}/messages/{s.id}')

class Client(httpx.Client):
    def __init__(s, Token: str):
        '''Discord REST API wrapper.'''
        super().__init__()
        s.headers = GetNewHeaders(Token)
        Client.Instance = s

    def GetClientToken(s):
        return s.headers['authorization']

    # https://discord.com/developers/docs/resources/user#get-current-user
    def GetCurrentUser(s):
        '''Argless User Profile Call'''
        return s.GET('/users/@me')

    def GetUserInfo(s, UserID):
        '''User Profile Call using UserID'''
        return s.GET(f'/users/{UserID}/profile?with_mutual_guilds=true')

    def GetUserAffinities(s):
        '''Argless Users Affinities Call'''
        return s.GET('/users/@me/affinities/users')
    
    def GetGuildAffinities(s):
        '''Argless Guilds Affinities Call'''
        return s.GET('/users/@me/affinities/guilds')

    def GetUserGuilds(s):
        '''Argless User Guilds Call'''
        return s.GET('/users/@me/guilds')
    
    def SetUserStatus(s, status):
        '''Accepts online, idle, dnd, invisible. Will Show only if connected to WebSocket'''
        assert status in ("online", "idle", "dnd", "invisible")
        return s.PATCH('/users/@me/settings', json={"status": status})

    # https://discord.com/developers/docs/resources/invite#get-invite
    def InviteInfo(s, Invite: str):
        '''Only accepts a sanitized code currently.'''
        return s.GET(f'/invites/{Invite}?with_counts=true&with_expiration=true')

    def JoinInvite(s, Invite: str):
        '''Only accepts a sanitized code currently.'''
        Overwrite = {'x-context-properties': 'eyJsb2NhdGlvbiI6Ik1hcmtkb3duIExpbmsifQ=='}
        return s.POST(f'/invites/{Invite}', headers = Overwrite)

    def LeaveGuild(s, GuildID: str):
        '''Requires GuildID'''
        return s.DELETE(f'/users/@me/guilds/{GuildID}', data = {"lurking": False})

    def SendMessage(s, ChannelID: str, **Message):
        '''Requires ChannelId, Use keyword args to pass in msg dict data.'''
        Payload = {"nonce": "".join(random.choice(string.digits) for _ in range(18)), "tts": False}
        Payload.update(Message); return s.POST(f'/channels/{ChannelID}/messages', json = 
            Payload, headers = {'referer': f'https://discord.com/channels/@me/{ChannelID}'})

    def Greet(s, ChannelID: str, StickerID = '749054660769218631'):
    	'''Requires ChannelID, Optional StickerID'''
    	return s.POST(f'/channels/{ChannelID}/greet', json={"sticker_ids":[StickerID]})

    def IterMessages(s, ChannelID: str, Before: str = ''):
        '''Requires ChannelId'''
        Params = {'limit': 100}
        while True:
            if Before:
                Params['before'] = Before
            R = s.GET(f'/channels/{ChannelID}/messages', params = Params)
            yield from R.json
            if not len(R.json):
                return
            Before = R.json[-1]['id']

    def CreateDM(s, User: str):
        '''Requires UserId'''
        return s.POST('/users/@me/channels', json = {'recipients': [User]})

    def CloseDM(s, ChannelID: str):
        '''Requires ChannelId'''
        return s.DELETE(f'/channels/{ChannelID}')

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
        return s.GenReq("GET", Path, *Args, **Kwargs)

    def POST(s, Path, *Args, **Kwargs):
        '''POST Request using GenReq. Returns Code, Data.'''
        return s.GenReq('POST', Path, *Args, **Kwargs)

    def PUT(s, Path, *Args, **Kwargs):
        '''PUT Request using GenReq. Returns Code, Data.'''
        return s.GenReq('PUT', Path, *Args, **Kwargs)

    def DELETE(s, Path, *Args, **Kwargs):
        '''DELETE Request using GenReq. Returns Code, Data.'''
        return s.GenReq('DELETE', Path, *Args, **Kwargs)

    def PATCH(s, Path, *Args, **Kwargs):
        '''PATCH Request using GenReq. Returns Code, Data.'''
        return s.GenReq("PATCH", Path, *Args, **Kwargs)

    def GenReq(s, Method, Path, *Args, **Kwargs) -> Response:
        '''General Purpose API Request Function. Requires a Method and Path. Returns the Status Code, Body.'''
        Y = s.request(Method, API(Path), *Args, **Kwargs)
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


class AsyncClient(httpx.AsyncClient):
    def __init__(s, Token: str):
        '''Discord REST API wrapper.'''
        super().__init__()
        s.headers = GetNewHeaders(Token)
        Client.Instance = s

    async def GetClientToken(s):
        return s.headers['authorization']

    # https://discord.com/developers/docs/resources/user#get-current-user
    async def GetCurrentUser(s):
        '''Argless User Profile Call'''
        return await s.GET('/users/@me')

    async def GetUserInfo(s, UserID):
        '''User Profile Call using UserID'''
        return await s.GET(f'/users/{UserID}/profile?with_mutual_guilds=true')

    async def GetUserAffinities(s):
        '''Argless Users Affinities Call'''
        return await s.GET('/users/@me/affinities/users')
    
    async def GetGuildAffinities(s):
        '''Argless Guilds Affinities Call'''
        return await s.GET('/users/@me/affinities/guilds')

    async def GetUserGuilds(s):
        '''Argless User Guilds Call'''
        return await s.GET('/users/@me/guilds')
    
    async def SetUserStatus(s, status):
        '''Accepts online, idle, dnd, invisible. Will Show only if connected to WebSocket'''
        assert status in ("online", "idle", "dnd", "invisible")
        return await s.PATCH('/users/@me/settings', json={"status": status})

    # https://discord.com/developers/docs/resources/invite#get-invite
    async def InviteInfo(s, Invite: str):
        '''Only accepts a sanitized code currently.'''
        return await s.GET(f'/invites/{Invite}?with_counts=true&with_expiration=true')

    async def JoinInvite(s, Invite: str):
        '''Only accepts a sanitized code currently.'''
        Overwrite = {'x-context-properties': 'eyJsb2NhdGlvbiI6Ik1hcmtkb3duIExpbmsifQ=='}
        return await s.POST(f'/invites/{Invite}', headers = Overwrite)

    async def LeaveGuild(s, GuildID: str):
        '''Requires GuildID'''
        return await s.DELETE(f'/users/@me/guilds/{GuildID}', data = {"lurking": False})

    async def SendMessage(s, Channel: str, **Message):
        '''Requires ChannelId, Use keyword args to pass in msg dict data.'''
        Payload = {"nonce": "".join(random.choice(string.digits) for _ in range(18)), "tts": False}
        Payload.update(Message); return await s.POST(f'/channels/{Channel}/messages', json = 
            Payload, headers = {'referer': f'https://discord.com/channels/@me/{Channel}'})

    def IterMessages(s, ChannelID: str, Before: str = ''):
        '''Requires ChannelId'''
        Params = {'limit': 100}
        while True:
            if Before:
                Params['before'] = Before
            R = s.GET(f'/channels/{ChannelID}/messages', params = Params)
            yield from R.json
            if not len(R.json):
                return
            Before = R.json[-1]['id']

    async def CreateDM(s, User: str):
        '''Requires UserId'''
        return await s.POST('/users/@me/channels', json = {'recipients': [User]})

    async def CloseDM(s, ChannelID: str):
        '''Requires ChannelId'''
        return await s.DELETE(f'/channels/{ChannelID}')

    async def AddUserById(s, UserId: str):
        '''Accepts UserIds as strings'''
        Overwrite = {'x-context-properties': 'eyJsb2NhdGlvbiI6IlVzZXIgUHJvZmlsZSJ9'}
        return await s.PUT(f'/users/@me/relationships/{UserId}', json = {}, headers = Overwrite)

    async def AddUserByTag(s, UserTag: str):
        '''Accepts usertags as strings'''
        Username, Tag = UserTag.split('#')
        Overwrite = {'x-context-properties': 'eyJsb2NhdGlvbiI6IkFkZCBGcmllbmQifQ=='}
        return await s.POST(f'/users/@me/relationships', json = {"username": Username, 
            "discriminator": int(Tag)}, headers = Overwrite)

    async def SetUsername(s, Username: str, Password: str): 
        '''Update Username, Requires Account Password'''
        return await s.PATCH('/users/@me', json = {'username': Username, 'password': Password})

    async def SetAvatar(s, Picture):
        '''Update User Avatar with either a Img URL or Local File Object'''
        return await s.PATCH('/users/@me', json = {'avatar': ResolveImage(Picture)}, timeout = 100)

    async def SetAboutMe(s, BioText):
        '''Update User About me'''
        return await s.PATCH('/users/@me', json = {'bio': BioText})

    async def SetHypesquad(s, HypesquadNum: int):
        '''Update Hypesquad, Accepts Values from 1 to 3'''
        return await s.POST('/hypesquad/online', json = {'house_id': HypesquadNum})

    # Common Methods
    async def GET(s, Path, *Args, **Kwargs):
        '''GET Request using GenReq. Returns Code, Data.'''
        return await s.GenReq("GET", Path, *Args, **Kwargs)

    async def POST(s, Path, *Args, **Kwargs):
        '''POST Request using GenReq. Returns Code, Data.'''
        return await s.GenReq('POST', Path, *Args, **Kwargs)

    async def PUT(s, Path, *Args, **Kwargs):
        '''PUT Request using GenReq. Returns Code, Data.'''
        return await s.GenReq('PUT', Path, *Args, **Kwargs)

    async def DELETE(s, Path, *Args, **Kwargs):
        '''DELETE Request using GenReq. Returns Code, Data.'''
        return await s.GenReq('DELETE', Path, *Args, **Kwargs)

    async def PATCH(s, Path, *Args, **Kwargs):
        '''PATCH Request using GenReq. Returns Code, Data.'''
        return await s.GenReq("PATCH", Path, *Args, **Kwargs)

    async def GenReq(s, Method, Path, *Args, **Kwargs) -> Response:
        '''General Purpose API Request Function. Requires a Method and Path. Returns the Status Code, Body.'''
        Y = await s.request(Method, API(Path), *Args, **Kwargs)
        Code, Data = Y.status_code, Y.json() if Y.headers \
            ['content-type'] == 'application/json' else None
        if Code == 429:
            time.sleep(1 + Data['retry_after'] // 995)
            return await s.GenReq(Method, Path, *Args, **Kwargs)
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
    


