#!/usr/bin/python

from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.compat import xmlrpc_client
from wordpress_xmlrpc.methods import posts, taxonomies, media

from os import stat
from datetime import datetime, timedelta


def gen_datetime(date, style=None, zone=0):
    style = style or '%Y-%m-%d'
    t = datetime.strptime(date, style)
    d = timedelta(hours=zone)
    return t + d


def uploadMedia(path, wp):
    mp3 = open(path, 'rb')
    data = {'name': path.split('/')[-1],
            'type': 'audio/mpeg',
            'bits': xmlrpc_client.Binary(mp3.read())}

    response = wp.call(media.UploadFile(data))
    url = response['url']
    size = str(stat(path).st_size)
    return url+'\n'+size+'\n'+'audio/mpeg'


def uploadPost(auth, **args):
    wp = Client(auth['site'], auth['user'], auth['pass'])

    post = WordPressPost()

    post.post_type = args.get('type', None)
    post.title = args.get('title', None)
    post.content = args.get('content', None)
    post.date = gen_datetime(args['date'], args.get('date-format', None),
                             args.get('zone', 0))

    terms = { key: [value] for key, value in args.get('terms', {}).items() }
    post.terms_names = terms

    if args.get('path', None) is not None:
        post.custom_fields = [{'key': 'enclosure',
                               'value': uploadMedia(args['path'], wp)
                               }]

    if args.get('publish', False):
        post.post_status = 'publish'

    post.id = wp.call(posts.NewPost(post))
