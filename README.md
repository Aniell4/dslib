# D.S.P.L.
Discord Selfbot Python Library

# Docs
```python
from dspl import Client

C = Client(TOKEN) # Creates Client Istance with provided Token

C.GetCurrentUser() # Returns Basic User Info (of Client Token)

C.GetUserInfo(UserID) # Returns Basic User Info of Profived UserID (Works ONLY if Provided User and Client Token are Friends and/or have a guild in common)

C.InviteInfo(Code) # Returns Information of the invite code provided

C.JoinInvite(Code) # Joins Guild With Token Provided in Client

C.LeaveGuild(GuildID) # Leaves Guild from Provided GuildID

C.SendMessage(ChannelID, Message) # Sends a Message to the specified ChannelID

C.IterMessages(ChannelID) # Iterator Object For Messages in ChannelID 

C.CreateDM(UserID) # Creates DM With Specified UserID (Returns ChannelID of DM)

C.AddUserById(UserID) # Sends a Friend Request to the Specified UserID

C.AddUserByTag("User#0001") # Sends a Friend Request to the Specified User Tag

C.SetUsername(Username, Password) # Changes the Client Token Username to the Specified Username (Requires Password)

C.SetAvatar(URL) # Changes the Client Token Profile Picture to the Specified Photo URL

C.SetAvatar(FileObject) # Changes the Client Token Profile Picture to the Specified Bytes FileObject

C.SetAboutMe("Text") # Changes the Client Token About Me

C.SetHypesquad(1) # Changes the Client Token Hypesquad (Accepts Values from 1 to 3)
```
