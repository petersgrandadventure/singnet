import logging.config


def setup_logging():
    _logging = {
        'version': 1,
        'disable_existing_loggers': False,

        'root': {
            'level': 'INFO',
            'handlers': ['console'],
        },

        'formatters': {
            'standard': {
                'format': '[%(asctime)s][%(levelname)s] %(name)s %(filename)s:%(funcName)s:%(lineno)d | %(message)s',
                'datefmt': '%H:%M:%S',
            },
        },

        'handlers': {
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'standard'
            },
            'file': {
                'level': 'DEBUG',
                'class': 'logging.FileHandler',
                'formatter': 'standard',
                'filename': 'app.log'
            },
        },

        'loggers': {

            '': {
                'handlers': ['console', 'file'],
                'level': 'DEBUG',
                'propagate': False,
            },

            'sn_agent': {
                'handlers': ['console', 'file'],
                'level': 'DEBUG',
                'propagate': False,
            },

            'demo': {
                'handlers': ['console', 'file'],
                'level': 'DEBUG',
                'propagate': False,
            },

            'tests': {
                'handlers': ['console', 'file'],
                'level': 'DEBUG',
                'propagate': False,
            },
        }
    }

    logging.config.dictConfig(_logging)

