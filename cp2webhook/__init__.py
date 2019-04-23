'COOPER to Webhook'

import click
import datetime
import json
import logging.config
import sys
import zmq
import time
from .config import load_config
import concurrent.futures
import jsonpath_ng
import requests

__version__ = '@@VERSION@@'


@click.command()
@click.option('--config', '-c', 'config_file', type=click.File('r'), required=True, help='Configuration file.')
@click.option('--test', is_flag=True, help='Test configuration file.')
@click.version_option(version=__version__)
def cli(config_file, test=False):
    '''ZeroMQ to stdout.'''

    try:
        config = load_config(config_file)
        config_file.close()
    except Exception as e:
        logging.error('Failed opening configuration file')
        logging.error(str(e))
        sys.exit(1)

    if test:
        click.echo("The configuration file seems ok")
        return

    logging.config.dictConfig(config['log'])
    logging.info('Process started')

    run(config)


def get_value(param, message):
    if isinstance(param, jsonpath_ng.JSONPath):
        tmp = param.find(message)
        if tmp:
            return tmp[0].value

    if isinstance(param, dict):
        data = {}
        for key in param:
            data[key] = get_value(param[key], message)
        return data

    return param


def run(config):
    context = zmq.Context()
    sock = context.socket(zmq.SUB)
    sock.setsockopt_string(zmq.SUBSCRIBE, '')
    sock.connect('tcp://%s:%d' % (config['zmq']['host'], config['zmq']['port']))

    pool = concurrent.futures.ThreadPoolExecutor(max_workers=5)

    def message_worker(message):
        try:
            for webhook in config['webhooks']:

                if 'condition' in webhook:
                    for key, values in webhook['condition'].items():
                        if message[key] in values:
                            break
                    else:
                        logging.debug('stop on condition')
                        continue

                kwargs = {'allow_redirects': True}

                if 'data' in webhook:
                    kwargs['data'] = get_value(webhook['data'], message)

                if 'json' in webhook:
                    kwargs['json'] = get_value(webhook['json'], message)

                if 'params' in webhook:
                    kwargs['params'] = get_value(webhook['params'], message)

                if 'headers' in webhook:
                    kwargs['headers'] = get_value(webhook['headers'], message)

                url = webhook['url'].replace('$.id', message['id'])

                response = requests.request(webhook['method'], url, **kwargs)

                print(response)
        except Exception as e:
            logging.error(e)

    while True:
        try:
            message = sock.recv_json()
            # time = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
            logging.debug("Message: %s", message)

            pool.submit(message_worker, message)
            # message_worker(message)

        except zmq.error.Again as e:
            logging.error('ZeroMQ error: %s' % e)
        except Exception:
            logging.error('Unhandled exception', exc_info=True)


def main():
    try:
        cli()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        click.echo(str(e), err=True)
        if "DEBUG" in sys.argv:
            raise e
        sys.exit(1)
