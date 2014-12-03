#!/usr/bin/python

import os
import json
import shlex
from subprocess import Popen, PIPE
from sys import argv

from upload import upload_post


def run_command(cmd, context):
    script_bin = os.path.expanduser('~/.config/wmup/scripts/')
    args = shlex.split(cmd)
    args[0] = script_bin + args[0]

    for i, arg in enumerate(args[1:]):
        try:
            args[i + 1] = arg.format(**context)
        except KeyError:
            args[i + 1] = ''

    proc = Popen(args)
    code = proc.wait()

    if code:
        print('{}: exited with code: {}'.format(args[0], code))


def run_commands(cmds, context):
    for cmd in cmds:
        if '../' in cmd:
            raise SyntaxError('"../" is not allowed in commands')

        print('Starting command: {}'.format(cmd))
        run_command(cmd, context)


def parse_item(item):
    data = {
        'before': [],
        'after': [],
        'upload': True,
        'publish': True,
    }

    terms = {}

    for key, value in item.items():
        if key.startswith('@'):
            terms[key] = value

        elif key.startswith('!'):
            pass  # Comment

        elif key == 'before':
            if type(value) is str:
                value = [value]
            data['before'] = value

        elif key == 'after':
            if type(value) is str:
                value = [value]
            data['after'] = value

        else:
            data[key] = value

    data['path']

    try:
        data['title']
    except KeyError:
        data['title'] = os.path.basename(os.path.splitext(data['path'])[0])

    ctx = dict(data)
    ctx.update(terms)
    for key, value in data.items():
        try:
            data[key] = value.format(**ctx)
        except KeyError:
            data[key] = ''

        except AttributeError:
            pass

    return (data, terms)

if __name__ == '__main__':
    config_file = os.path.expanduser('~/.config/wmup/config.json')
    config = json.load(open(config_file, 'r'))

    for item in config['items']:
        data, terms = parse_item(item)
        ctx = dict(data)
        ctx.update(terms)

        args = dict(data)
        args['terms'] = {key[1:]: value for key, value in terms.items()}

        run_commands(data['before'], ctx)

        if data['upload']:
            upload_post(config['auth'], **args)

        run_commands(data['after'], ctx)
