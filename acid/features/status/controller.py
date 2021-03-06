# -*- coding: utf-8 -*-
from flask import Blueprint, current_app, render_template

from . import service


status = Blueprint('status', __name__, template_folder='../../templates')


@status.route('/status')
@status.route('/status/<string:pipename>')
def show_status(pipename=None):
    config = current_app.config
    zuul_url = config['zuul']['url']

    pipename = (pipename if pipename is not None else
                config['default']['pipename'])
    queues = service.make_queues(service.get_zuul_pipelines(),
                                 pipename, zuul_url)
    refs_list = ["collapse" + buildset.ref for queue in queues
                 for buildset in queue.buildsets]

    return render_template('status.html', queues=queues, pipename=pipename,
                           refs_list=refs_list)


@status.route('/')
def show_dashboard():
    config = current_app.config
    pipeline_stats = service.pipelines_stats(
        service.get_zuul_pipelines(), config['zuul']['pipelines'])
    return render_template('dashboard.html', pipeline_stats=pipeline_stats)
