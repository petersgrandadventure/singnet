import logging.config


def setup_logging():
    DEFAULT_LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': '%(asctime)s [%(levelname)s] %(name)s[L%(lineno)3d]: %(message)s'
            }
        },
        'handlers': {
            'default': {
                'level': 'DEBUG',
                'formatter': 'standard',
                'class': 'logging.StreamHandler',
            },
        },
        'loggers': {
            '': {
                'level': 'DEBUG',
            },
            'sn_agent': {
                'level': 'DEBUG',
            },
        },
        'root': {
            'handlers': ['default'],
            'level': 'DEBUG',
        },
    }
    logging.config.dictConfig(DEFAULT_LOGGING)
