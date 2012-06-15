import requests, json

class SimpleVimeo(object):
    """ Abstract base class """
    _base_url = 'http://vimeo.com/api/v2/%(domain)s/%(name)s/%(request)s.json'

    def __init__(self):
        self._default_args = {}

    def _request(self, **kwargs):
        kwargs.update(self._default_args) # No overlap between kwargs and base_args
        url = self._base_url % kwargs
        request = requests.get(url)
        return json.loads(request.text)

class User(SimpleVimeo):
    _base_url = 'http://vimeo.com/api/v2/%(username)s/%(request)s.json'

    def __init__(self, username):
        super(User, self).__init__()
        self._default_args['username'] = username

    @property
    def info(self):
        return self._request(request='info')

    @property
    def videos(self):
        return self._request(request='videos')

    @property
    def likes(self):
        return self._request(request='likes')

    @property
    def appears_in(self):
        return self._request(request='appears_in')

    @property
    def all_videos(self):
        return self._request(request='all_videos')

    @property
    def subscriptions(self):
        return self._request(request='subscriptions')

    @property
    def albums(self):
        return self._request(request='albums')

    @property
    def channels(self):
        return self._request(request='channels')

    @property
    def groups(self):
        return self._request(request='groups')

    def activity(self, scope='user_did'):
        """ Return the activity for this user. Scope can be any of 'user_did', 'happened_to_user', 'contacts_did' or 'everyone_did'
        """
        activity_url = 'http://vimeo.com/api/v2/activity/%(username)s/%(scope)s.json'
        return requests.get(activity_url % {
            'username': self.default_args['username'],
            'scope': scope,
        })

class Group(SimpleVimeo):
    def __init__(self, group_name):
        super(Group, self).__init__()
        self._default_args['domain'] = 'group'
        self._default_args['name'] = group_name

    @property
    def info(self):
        return self._request(request='info')

    @property
    def users(self):
        return self._request(request='users')

    @property
    def videos(self):
        return self._request(request='videos')


class Channel(SimpleVimeo):
    def __init__(self, channel_name):
        super(Channel, self).__init__()
        self._default_args['domain'] = 'channel'
        self._default_args['name'] = channel_name

    @property
    def info(self):
        return self._request(request='info')

    @property
    def videos(self):
        return self._request(request='videos')


class Album(SimpleVimeo):
    def __init__(self, album_name):
        super(Album, self).__init__()
        self._default_args['domain'] = 'album'
        self._default_args['name'] = album_name

    @property
    def info(self):
        return self._request(request='info')

    @property
    def videos(self):
        return self._request(request='videos')


class Video(SimpleVimeo):
    _base_url = 'http://vimeo.com/api/v2/video/%(video_id)s.json'

    def __init__(self, video_id):
        super(Video, self).__init__()
        self._default_args['video_id'] = video_id

    @property
    def info(self):
        return self._request()
