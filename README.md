vimeo-wrapper
=============

A thin wrapper for vimeo activities with upload-capabilities

Usage:

    vimeo = Vimeo(access_token, access_token_secret, consumer_key, consumer_secret)

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
  
get vimeo info on a video

    info = vimeo.request('vimeo.videos.getInfo', data=dict(video_id=video_id))
