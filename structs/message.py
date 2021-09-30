class Message:
    def __init__(s, d):
        s.__id = d.get('id', None)
        s.__channel_id = d.get('channel_id', None)
        s.__guild_id = d.get('guild_id', None)
        s.__author = d.get('author', None)
        s.__member = d.get('member', None)
        s.__content = d.get('content', None)
        s.__timestamp = d.get('timestamp', None)
        s.__edited_timestamp = d.get('edited_timestamp', None)
        s.__tts = d.get('tts', None)
        s.__mention_everyone = d.get('mention_everyone', None)
        s.__mentions = d.get('mentions', None)
        s.__mention_roles = d.get('mention_roles', None)
        s.__mention_channels = d.get('mention_channels', None)
        s.__attachments = d.get('attachments', None)
        s.__embeds = d.get('embeds', None)
        s.__reactions = d.get('reactions', None)
        s.__nonce = d.get('nonce', None)
        s.__pinned = d.get('pinned', None)
        s.__webhook_id = d.get('webhook_id', None)
        s.__type = d.get('type', None)
        s.__activity = d.get('activity', None)
        s.__application = d.get('application', None)
        s.__application_id = d.get('application_id', None)
        s.__message_reference = d.get('message_reference', None)
        s.__flags = d.get('flags', None)
        s.__referenced_message = d.get('referenced_message', None)
        s.__interaction = d.get('interaction', None)
        s.__thread = d.get('thread', None)
        s.__components = d.get('components', None)
        s.__sticker_items = d.get('sticker_items', None)
        s.__stickers = d.get('stickers', None)
    @property
    def id(s):
        '''Id of the message'''
        return s.__id
    @id.setter
    def id(s, val):
        s.__id = val
    @property
    def channel_id(s):
        '''Id of the channel the message was sent in'''
        return s.__channel_id
    @channel_id.setter
    def channel_id(s, val):
        s.__channel_id = val
    @property
    def guild_id(s):
        '''Id of the guild the message was sent in'''
        return s.__guild_id
    @guild_id.setter
    def guild_id(s, val):
        s.__guild_id = val
    @property
    def author(s):
        '''The author of this message (not guaranteed to be a valid user, see below)'''
        return s.__author
    @author.setter
    def author(s, val):
        s.__author = val
    @property
    def member(s):
        '''Member properties for this message's author'''
        return s.__member
    @member.setter
    def member(s, val):
        s.__member = val
    @property
    def content(s):
        '''Contents of the message'''
        return s.__content
    @content.setter
    def content(s, val):
        s.__content = val
    @property
    def timestamp(s):
        '''When this message was sent'''
        return s.__timestamp
    @timestamp.setter
    def timestamp(s, val):
        s.__timestamp = val
    @property
    def edited_timestamp(s):
        '''When this message was edited (or null if never)'''
        return s.__edited_timestamp
    @edited_timestamp.setter
    def edited_timestamp(s, val):
        s.__edited_timestamp = val
    @property
    def tts(s):
        '''Whether this was a tts message'''
        return s.__tts
    @tts.setter
    def tts(s, val):
        s.__tts = val
    @property
    def mention_everyone(s):
        '''Whether this message mentions everyone'''
        return s.__mention_everyone
    @mention_everyone.setter
    def mention_everyone(s, val):
        s.__mention_everyone = val
    @property
    def mentions(s):
        '''Users specifically mentioned in the message'''
        return s.__mentions
    @mentions.setter
    def mentions(s, val):
        s.__mentions = val
    @property
    def mention_roles(s):
        '''Roles specifically mentioned in this message'''
        return s.__mention_roles
    @mention_roles.setter
    def mention_roles(s, val):
        s.__mention_roles = val
    @property
    def mention_channels(s):
        '''Channels specifically mentioned in this message'''
        return s.__mention_channels
    @mention_channels.setter
    def mention_channels(s, val):
        s.__mention_channels = val
    @property
    def attachments(s):
        '''Any attached files'''
        return s.__attachments
    @attachments.setter
    def attachments(s, val):
        s.__attachments = val
    @property
    def embeds(s):
        '''Any embedded content'''
        return s.__embeds
    @embeds.setter
    def embeds(s, val):
        s.__embeds = val
    @property
    def reactions(s):
        '''Reactions to the message'''
        return s.__reactions
    @reactions.setter
    def reactions(s, val):
        s.__reactions = val
    @property
    def nonce(s):
        '''Used for validating a message was sent'''
        return s.__nonce
    @nonce.setter
    def nonce(s, val):
        s.__nonce = val
    @property
    def pinned(s):
        '''Whether this message is pinned'''
        return s.__pinned
    @pinned.setter
    def pinned(s, val):
        s.__pinned = val
    @property
    def webhook_id(s):
        '''If the message is generated by a webhook, this is the webhook's id'''
        return s.__webhook_id
    @webhook_id.setter
    def webhook_id(s, val):
        s.__webhook_id = val
    @property
    def type(s):
        '''Type of message'''
        return s.__type
    @type.setter
    def type(s, val):
        s.__type = val
    @property
    def activity(s):
        '''Sent with rich presence-related chat embeds'''
        return s.__activity
    @activity.setter
    def activity(s, val):
        s.__activity = val
    @property
    def application(s):
        '''Sent with rich presence-related chat embeds'''
        return s.__application
    @application.setter
    def application(s, val):
        s.__application = val
    @property
    def application_id(s):
        '''If the message is a response to an interaction, this is the id of the interaction's application'''
        return s.__application_id
    @application_id.setter
    def application_id(s, val):
        s.__application_id = val
    @property
    def message_reference(s):
        '''Data showing the source of a crosspost, channel follow add, pin, or reply message'''
        return s.__message_reference
    @message_reference.setter
    def message_reference(s, val):
        s.__message_reference = val
    @property
    def flags(s):
        '''Message flags combined as a bitfield'''
        return s.__flags
    @flags.setter
    def flags(s, val):
        s.__flags = val
    @property
    def referenced_message(s):
        '''The message associated with the message_reference'''
        return s.__referenced_message
    @referenced_message.setter
    def referenced_message(s, val):
        s.__referenced_message = val
    @property
    def interaction(s):
        '''Sent if the message is a response to an interaction'''
        return s.__interaction
    @interaction.setter
    def interaction(s, val):
        s.__interaction = val
    @property
    def thread(s):
        '''The thread that was started from this message, includes thread member object'''
        return s.__thread
    @thread.setter
    def thread(s, val):
        s.__thread = val
    @property
    def components(s):
        '''Sent if the message contains components like buttons, action rows, or other interactive components'''
        return s.__components
    @components.setter
    def components(s, val):
        s.__components = val
    @property
    def sticker_items(s):
        '''Sent if the message contains stickers'''
        return s.__sticker_items
    @sticker_items.setter
    def sticker_items(s, val):
        s.__sticker_items = val
    @property
    def stickers(s):
        '''Deprecated the stickers sent with the message'''
        return s.__stickers
    @stickers.setter
    def stickers(s, val):
        s.__stickers = val
