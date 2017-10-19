import aiohttp_jinja2 as aiohttp_jinja2


@aiohttp_jinja2.template('index.jinja2')
def index(request):
    return {'name': 'Andrew', 'surname': 'Svetlov'}
