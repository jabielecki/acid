# -*- coding: utf-8 -*-
from flask import Blueprint, current_app, render_template

from . import service


status = Blueprint('status', __name__, template_folder='../../templates')


@status.route('/status')
@status.route('/status/<string:pipename>')
def show_status(pipename=None):
    zuul_url = current_app.config["zuul"]["url"]
    zuul_endpoint = current_app.config['zuul']['status_endpoint']

    pipename = (pipename if pipename is not None else
                current_app.config['default']['pipename'])
    url = service.status_endpoint(zuul_url, zuul_endpoint)
    resource = service.fetch_json_data(endpoint=url)
    queues = service.make_queues(resource['pipelines'], pipename, zuul_url)
    return render_template('status.html', queues=queues, pipename=pipename)


@status.route('/')
def show_dashboard():
    zuul_url = current_app.config["zuul"]["url"]
    zuul_endpoint = current_app.config['zuul']['status_endpoint']

    url = service.status_endpoint(zuul_url, zuul_endpoint)
    resource = service.fetch_json_data(endpoint=url)
    pipeline_stats = service.pipelines_stats(
        resource['pipelines'], current_app.config['zuul']['pipelines'])
    return render_template('dashboard.html', pipeline_stats=pipeline_stats)
