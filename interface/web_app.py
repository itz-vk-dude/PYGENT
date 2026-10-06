import os
from flask import Flask, render_template
from interface.api import api_bp, init_api

def create_app(state_store=None, agent_core=None):
    template_dir = os.path.join(os.path.dirname(__file__), 'templates')
    static_dir = os.path.join(os.path.dirname(__file__), 'static')
    
    app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
    init_api(state_store, agent_core)
    app.register_blueprint(api_bp)

    @app.route('/')
    def home_page():
        return render_template('index.html')

    @app.route('/world')
    def world_page():
        return render_template('world.html')

    @app.route('/twin')
    def twin_page():
        return render_template('twin.html')

    @app.route('/agent')
    def agent_page():
        return render_template('agent.html')

    @app.route('/robot')
    def robot_page():
        return render_template('robot.html')

    @app.route('/learning')
    def learning_page():
        return render_template('learning.html')

    @app.route('/system')
    def system_page():
        return render_template('system.html')

    return app
