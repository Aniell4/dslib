class Channel:
    def __init__(s, d):
        s.__id = d.get('id', None)
        s.__type = d.get('type', None)
        s.__guild_id = d.get('guild_id', None)
        s.__position = d.get('position', None)
        s.__permission_overwrites = d.get('permission_overwrites', None)
        s.__name = d.get('name', None)
        s.__topic = d.get('topic', None)
        s.__nsfw = d.get('nsfw', None)
        s.__last_message_id = d.get('last_message_id', None)
        s.__bitrate = d.get('bitrate', None)
        s.__user_limit = d.get('user_limit', None)
        s.__rate_limit_per_user = d.get('rate_limit_per_user', None)
        s.__recipients = d.get('recipients', None)
        s.__icon = d.get('icon', None)
        s.__owner_id = d.get('owner_id', None)
        s.__application_id = d.get('application_id', None)
        s.__parent_id = d.get('parent_id', None)
        s.__last_pin_timestamp = d.get('last_pin_timestamp', None)
        s.__rtc_region = d.get('rtc_region', None)
        s.__video_quality_mode = d.get('video_quality_mode', None)
        s.__message_count = d.get('message_count', None)
        s.__member_count = d.get('member_count', None)
        s.__thread_metadata = d.get('thread_metadata', None)
        s.__member = d.get('member', None)
        s.__default_auto_archive_duration = d.get('default_auto_archive_duration', None)
        s.__permissions = d.get('permissions', None)
    @property
    def id(s):
        '''The id of this channel'''
        return s.__id
    @id.setter
    def id(s, val):
        s.__id = val
    @property
    def type(s):
        '''The type of channel'''
        return s.__type
    @type.setter
    def type(s, val):
        s.__type = val
    @property
    def guild_id(s):
        '''The id of the guild (may be missing for some channel objects received over gateway guild dispatches)'''
        return s.__guild_id
    @guild_id.setter
    def guild_id(s, val):
        s.__guild_id = val
    @property
    def position(s):
        '''Sorting position of the channel'''
        return s.__position
    @position.setter
    def position(s, val):
        s.__position = val
    @property
    def permission_overwrites(s):
        '''Explicit permission overwrites for members and roles'''
        return s.__permission_overwrites
    @permission_overwrites.setter
    def permission_overwrites(s, val):
        s.__permission_overwrites = val
    @property
    def name(s):
        '''The name of the channel (1-100 characters)'''
        return s.__name
    @name.setter
    def name(s, val):
        s.__name = val
    @property
    def topic(s):
        '''The channel topic (0-1024 characters)'''
        return s.__topic
    @topic.setter
    def topic(s, val):
        s.__topic = val
    @property
    def nsfw(s):
        '''Whether the channel is nsfw'''
        return s.__nsfw
    @nsfw.setter
    def nsfw(s, val):
        s.__nsfw = val
    @property
    def last_message_id(s):
        '''The id of the last message sent in this channel (may not point to an existing or valid message)'''
        return s.__last_message_id
    @last_message_id.setter
    def last_message_id(s, val):
        s.__last_message_id = val
    @property
    def bitrate(s):
        '''The bitrate (in bits) of the voice channel'''
        return s.__bitrate
    @bitrate.setter
    def bitrate(s, val):
        s.__bitrate = val
    @property
    def user_limit(s):
        '''The user limit of the voice channel'''
        return s.__user_limit
    @user_limit.setter
    def user_limit(s, val):
        s.__user_limit = val
    @property
    def rate_limit_per_user(s):
        '''Amount of seconds a user has to wait before sending another message (0-21600); bots, as well as users with the permission manage_messages or manage_channel, are unaffected'''
        return s.__rate_limit_per_user
    @rate_limit_per_user.setter
    def rate_limit_per_user(s, val):
        s.__rate_limit_per_user = val
    @property
    def recipients(s):
        '''The recipients of the dm'''
        return s.__recipients
    @recipients.setter
    def recipients(s, val):
        s.__recipients = val
    @property
    def icon(s):
        '''Icon hash'''
        return s.__icon
    @icon.setter
    def icon(s, val):
        s.__icon = val
    @property
    def owner_id(s):
        '''Id of the creator of the group dm or thread'''
        return s.__owner_id
    @owner_id.setter
    def owner_id(s, val):
        s.__owner_id = val
    @property
    def application_id(s):
        '''Application id of the group dm creator if it is bot-created'''
        return s.__application_id
    @application_id.setter
    def application_id(s, val):
        s.__application_id = val
    @property
    def parent_id(s):
        '''For guild channels: id of the parent category for a channel (each parent category can contain up to 50 channels), for threads: id of the text channel this thread was created'''
        return s.__parent_id
    @parent_id.setter
    def parent_id(s, val):
        s.__parent_id = val
    @property
    def last_pin_timestamp(s):
        '''When the last pinned message was pinned. this may be null in events such as guild_create when a message is not pinned.'''
        return s.__last_pin_timestamp
    @last_pin_timestamp.setter
    def last_pin_timestamp(s, val):
        s.__last_pin_timestamp = val
    @property
    def rtc_region(s):
        '''Voice region id for the voice channel, automatic when set to null'''
        return s.__rtc_region
    @rtc_region.setter
    def rtc_region(s, val):
        s.__rtc_region = val
    @property
    def video_quality_mode(s):
        '''The camera video quality mode of the voice channel, 1 when not present'''
        return s.__video_quality_mode
    @video_quality_mode.setter
    def video_quality_mode(s, val):
        s.__video_quality_mode = val
    @property
    def message_count(s):
        '''An approximate count of messages in a thread, stops counting at 50'''
        return s.__message_count
    @message_count.setter
    def message_count(s, val):
        s.__message_count = val
    @property
    def member_count(s):
        '''An approximate count of users in a thread, stops counting at 50'''
        return s.__member_count
    @member_count.setter
    def member_count(s, val):
        s.__member_count = val
    @property
    def thread_metadata(s):
        '''Thread-specific fields not needed by other channels'''
        return s.__thread_metadata
    @thread_metadata.setter
    def thread_metadata(s, val):
        s.__thread_metadata = val
    @property
    def member(s):
        '''Thread member object for the current user, if they have joined the thread, only included on certain api endpoints'''
        return s.__member
    @member.setter
    def member(s, val):
        s.__member = val
    @property
    def default_auto_archive_duration(s):
        '''Default duration for newly created threads, in minutes, to automatically archive the thread after recent activity, can be set to: 60, 1440, 4320, 10080'''
        return s.__default_auto_archive_duration
    @default_auto_archive_duration.setter
    def default_auto_archive_duration(s, val):
        s.__default_auto_archive_duration = val
    @property
    def permissions(s):
        '''Computed permissions for the invoking user in the channel, including overwrites, only included when part of the resolved data received on a slash command interaction'''
        return s.__permissions
    @permissions.setter
    def permissions(s, val):
        s.__permissions = val
