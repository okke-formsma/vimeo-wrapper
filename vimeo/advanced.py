from collections import OrderedDict
import os, requests
from requests.exceptions import ConnectionError
from requests_oauthlib import OAuth1


class Vimeo(object):
    VIMEO_ENDPOINT = 'http://vimeo.com/api/rest/v2/'
    client = None


    def __init__(self, auth_token, auth_token_secret, key, secret):
        self.auth = OAuth1(key, secret,auth_token, auth_token_secret)
        self.client = requests.session()

    def request(self, method, data=None, params=None, *args, **kwargs):
        """ Request `method` from Vimeo, using post-data data, get parameters params.
        All other parameters are directly passed to requests.post.
        """
        data = data or {}
        data['method'] = method
        params = params or {}
        params['format'] = 'json'

        response = self.client.post(self.VIMEO_ENDPOINT, params=params, data=data,auth=self.auth, *args, **kwargs)
        return response.json()

    def upload(self, file, chunk_size=1024 * 1024 * 128):
        """ Uploads the file through post. (not streaming! The whole file is loaded in memory!)
        arguments:
        file: absolute file path to file. (e.g. "/home/oformsma/media/movie.mov")
        max_retries: number of times a chunk should be retried for upload
        chunk_size: bytes. chunks of this size get loaded into memory and sent. Defaults to 128 MB.

        Returns the vimeo video id if the upload is successful. Lets any exceptions from the requests package through.
        """

        #todo: upfront file space check
        #create upload ticket
        ticket = self.request('vimeo.videos.upload.getTicket')['ticket']

        # Upload the file to vimeo.
        # The chunk_id and ticket_id need to be in the multipart-encoded form data.
        basename = os.path.basename(file)
        with open(file, 'rb') as fp:
            chunk_sizes = []
            chunk_id = 0
            while True:
                chunk = fp.read(chunk_size)
                if chunk == '':
                    break

                # data needs to be an OrderedDict!
                # Otherwise, the file data might come before the chunk_id parameter. The Vimeo API will then not recognize
                # the chunk_id.
                self.client.post(
                    ticket['endpoint'],
                    data=OrderedDict({'chunk_id': chunk_id}),
                    files={'file_data': (basename + '.' + str(chunk_id), chunk)},
                    )

                chunk_sizes.append(len(chunk))
                chunk_id += 1

        # Verify file upload size
        try:
            verify = self.request('vimeo.videos.upload.verifyChunks', data={'ticket_id': ticket['id']})
            if len(chunk_sizes) == 1:
                #@#T@($^@ VIMEO ONE CHUNK IS NOT A SPECIAL CASE
                #notice the missing [i] in the next line.
                if int(verify['ticket']['chunks']['chunk']['size']) != chunk_sizes[0]:
                    raise UploadException("The uploaded filesize and file size on disk are not the same")
            else:
                for i, size in enumerate(chunk_sizes):
                    if int(verify['ticket']['chunks']['chunk'][i]['size']) != size:
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