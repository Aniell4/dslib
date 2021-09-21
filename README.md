# D.S.P.L.
Discord Selfbot Python Library

# Docs
```python
C = Client(TOKEN) # Creates Client Istance with provided Token

C.GetCurrentUser() # Returnes Basic User Info (of Client Token)

C.InviteInfo(Code) # Returnes Information of the invite code provided

C.JoinInvite(Code) # Joins Guild With Token Provided in Client

C.SendMessage(ChannelID, Message) # Sends a Message to the specified ChannelID

C.CreateDM(UserID) # Creates DM With Specified UserID (Returns ChannelID of DM)

C.AddUserById(UserID) # Sends a Friend Request to the Specified UserID

C.AddUserByTag("User#0001") # Sends a Friend Request to the Specified User Tag

C.SetUsername(Username, Password) # Changes the Client Token Username to the Specified Username (Requires Password)

C.SetAvatar(URL) # Changes the Client Token Profile Picture to the Specified Photo URL

C.SetAvatar(FileObject) # Changes the Client Token Profile Picture to the Specified Bytes FileObject
```
