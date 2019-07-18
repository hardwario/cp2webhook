from schema import Schema, And, Or, Use, Optional, SchemaError
import logging
import os
import sys
import yaml
import jsonpath_ng


DEFAULT = {
    'log': {
        'disable_existing_loggers': False,
        'version': 1,
        'formatters': {
            'short': {
                'format': '%(asctime)s %(levelname)s %(module)s: %(message)s'
            }
        },
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'formatter': 'short',
                'class': 'logging.StreamHandler'
            }
        },
        'loggers': {
            '': {
                'handlers': ['console'],
                'level': 'DEBUG'
            }
        }
    }
}


def port_range(port):
    return 0 <= port <= 65535


def method(method):
    method = method.lower()
    if method in ['post', 'get']:
        return method


def json_path(txt):
    try:
        return jsonpath_ng.parse(txt)
    except Exception as e:
        raise SchemaError('Bad JsonPath format: %s' % txt)


def str_or_jsonPath(txt):
    if "$" in txt:
        return json_path(txt)
    return txt


def jsonPath_or_obj(obj):
    if isinstance(obj, str):
        if '$' in obj:
            return json_path(obj)
    return obj


def jsonPath_or_obj_recursive(obj):
    if isinstance(obj, str):
        if '$' in obj:
            return json_path(obj)

    if isinstance(obj, dict):
        for k, v in obj.items():
            obj[k] = jsonPath_or_obj_recursive(v)

    return obj


schema = Schema({
    'zmq': {
        'host': And(str, len),
        'port': And(Use(int), port_range),
        'timeout': And(Use(int), lambda x: x > 0)
    },
    'webhooks': [{
        Optional('name'): And(str, len),
        'url': And(str, len),
        'method': And(str, Use(method)),
        Optional('data'): Or({str: Use(jsonPath_or_obj_recursive)}, Use(jsonPath_or_obj_recursive)),
        Optional('json'): Or({str: Use(jsonPath_or_obj_recursive)}, Use(jsonPath_or_obj_recursive)),
        Optional('params'): Or({str: Use(jsonPath_or_obj)}, Use(jsonPath_or_obj)),
        Optional('headers'): {str: Use(jsonPath_or_obj)},
        Optional('condition'): {str: [Use(str)]}
    }],
    Optional('log'): dict
})


def load_config(config_file):
    config = yaml.safe_load(config_file)
    try:
        config = schema.validate(config)
    except SchemaError as e:
        # Better error format
        error = str(e).splitlines()
        del error[1]
        raise Exception(' '.join(error))

    _apply_default(config, DEFAULT)

    return config


def _apply_default(config, default):
    for key in default:
        if key not in config:
            config[key] = default[key]
            continue

        if isinstance(default[key], dict):
            _apply_default(config[key], default[key])
