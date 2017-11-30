import logging

import aiohttp_jinja2 as aiohttp_jinja2
from aiohttp import web

logger = logging.getLogger(__name__)


def get_base_context(app):
    context = {}
    context['service_adapters'] = app['service_manager'].service_adapters
    return context


class IndexHandler(web.View):
    async def get(self):
        context = get_base_context(self.request.app)
        response = aiohttp_jinja2.render_template('dashboard.jinja2', self.request, context)
        return response


class ServiceHandler(web.View):
    async def get(self):
        service_id = self.request.match_info.get('service_id')

        context = get_base_context(self.request.app)

        service_adapter = self.request.app['service_manager'].get_service_adapter_for_id(service_id)

        context['service_adapter'] = service_adapter

        context['page_title'] = service_adapter.service.name
        context['description'] = service_adapter.service.description

        response = aiohttp_jinja2.render_template('service-default.jinja2', self.request, context)
        return response


@aiohttp_jinja2.template('mnistclassifier.jinja2')
def tensorflowmnistclassifier(request):
    return {'name': 'Andrew', 'surname': 'Svetlov'}


@aiohttp_jinja2.template('simpleadapter.jinja2')
def simpleadapter(request):
    return {'name': 'Andrew', 'surname': 'Svetlov'}


@aiohttp_jinja2.template('relexparser.jinja2')
def relexparser(request):
    return {'name': 'Andrew', 'surname': 'Svetlov'}


@aiohttp_jinja2.template('aigentstextsclusterer.jinja2')
def aigentstextsclusterer(request):
    return {'name': 'Andrew', 'surname': 'Svetlov'}


@aiohttp_jinja2.template('aigentstextextractor.jinja2')
def aigentstextextractor(request):
    return {'name': 'Andrew', 'surname': 'Svetlov'}


@aiohttp_jinja2.template('aigentssocialgrapher.jinja2')
def aigentssocialgrapher(request):
    return {'name': 'Andrew', 'surname': 'Svetlov'}


@aiohttp_jinja2.template('aigentsrssfeeder.jinja2')
def aigentsrssfeeder(request):
    return {'name': 'Andrew', 'surname': 'Svetlov'}


@aiohttp_jinja2.template('tensorflowimagenetclassifier.jinja2')
def tensorflowimagenetclassifier(request):
    return {'name': 'Andrew', 'surname': 'Svetlov'}
