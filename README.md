vimeo-wrapper
=============

A thin python wrapper for the vimeo API with upload-capabilities.  It took me quite a while to get this figured out; the Vimeo 
API is rather PHP-centric.

Installation:
    
    pip install git+http://github.com/okke-formsma/vimeo-wrapper#egg=vimeo

Usage:

    vimeo = Vimeo(access_token, access_token_secret, consumer_key, consumer_secret)

get vimeo info on a video

    info = vimeo.request('vimeo.videos.getInfo', data=dict(video_id=video_id))
    
Perform any request like so: (the list of available requests can be found at [the vimeo api site](https://developer.vimeo.com/apis/advanced/methods))

    result = vimeo.request(method, data=...)
    
upload video file

    video_id = vimeo.upload(file="/home/okke-formsma/videos/test.mov")

set video metadata

    vimeo.request('vimeo.videos.setTitle', data={
        'video_id': video_id,
        'title': "Vimeo-wrapper video",
    })
    vimeo.request('vimeo.videos.setDescription', data={
        'video_id': video_id,
        'description': "It is the best!",
    })
    vimeo.request('vimeo.videos.setDownloadPrivacy', data={
        'video_id': video_id,
        'download': False
    })
  
