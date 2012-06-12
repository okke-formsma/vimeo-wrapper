import os, requests
from oauth_hook.hook import OAuthHook
from requests.exceptions import ConnectionError

class Vimeo:
    VIMEO_ENDPOINT = 'http://vimeo.com/api/rest/v2/'
    client = None

    def __init__(self, auth_token, auth_token_secret, key, secret):
        oauth_hook = OAuthHook(
            access_token=auth_token,
            access_token_secret=auth_token_secret,
            consumer_key=key,
            consumer_secret=secret,
            header_auth=True,
            )

        self.client = requests.session(hooks={'pre_request': oauth_hook})

    def request(self, method, data=None, params=None, *args, **kwargs):
        """ Request `method` from Vimeo, using post-data data, get parameters params.
        All other parameters are directly passed to requests.post.
        """
        data = data or {}
        data['method'] = method
        params = params or {}
        params['format'] = 'json'
        return self.client.post(self.VIMEO_ENDPOINT, params=params, data=data, *args, **kwargs).json

    def upload(self, file, max_retries=5):
        """ Uploads the file through post. (not streaming! The whole file is loaded in memory!)
        arguments:
        file: absolute file path to file. (e.g. "/home/oformsma/media/movie.mov")

        Returns the vimeo video id if the upload is successful.
        """

        #todo: upfront file space check
        #create upload ticket
        ticket = self.request('vimeo.videos.upload.getTicket')['ticket']

        # Upload the file to vimeo.
        # The chunk_id and ticket_id need to be in the multipart-encoded form data.
        basename = os.path.basename(file)

        try:
            multipart_data = {
                'ticket_id': ticket['id'],
                'chunk_id': '0',
                'file_data': (basename, open(file, 'rb')),
                }

            self.client.post(
                ticket['endpoint'],
                params={'format': 'json'},
                config={'max_retries': max_retries},
                files=multipart_data,
                )
        except ConnectionError as ex:
            raise UploadException(ex)

        # Verify file upload size
        try:
            verify = self.request('vimeo.videos.upload.verifyChunks', data={'ticket_id': ticket['id']})
            if int(verify['ticket']['chunks']['chunk']['size']) != os.path.getsize(file):
                raise UploadException("The uploaded filesize and file size on disk are not the same")
        except (KeyError, ValueError):
            raise UploadException("The uploaded file could not be verified.")

        # Let Vimeo know we the upload is OK.
        complete = self.request('vimeo.videos.upload.complete', data={
            'filename': basename,
            'ticket_id': ticket['id'],
            })

        return int(complete['ticket']['video_id'])


class VimeoException(Exception):
    """ Base class for all vimeo-wrapper exceptions.
    """
    pass

class UploadException(VimeoException, ConnectionError):
    pass