import aiohttp_jinja2
import jinja2

def setup_ui(app):
    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('sn_agent/ui/templates'))
