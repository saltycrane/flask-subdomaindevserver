from flask import Flask

from simple_page.simple_page import simple_page


API_HOST = 'default-host'
DB_SERVER = 'default-db-server'


class FakeApiRequester(object):
    def __init__(self, host):
        self.host = host

    def __repr__(self):
        return 'FakeApiRequester(host={})'.format(self.host)


class FakeDatabase(object):
    def __init__(self, host):
        self.host = host

    def __repr__(self):
        return 'FakeDatabase(host={})'.format(self.host)


def get_subdomain_based_config(subdomain):

    class Config(object):
        pass
    config = Config()

    if subdomain == 'dev':
        config.API_HOST = 'dev-host'
        config.DB_SERVER = 'dev-db-server'
    elif subdomain == 'qa':
        config.API_HOST = 'qa-host'
        config.DB_SERVER = 'qa-db-server'

    return config


def create_app(debug=False, subdomain=None):
    app = Flask(__name__)
    app.debug = debug

    # Default configuration
    app.config.from_object(__name__)

    # Override configuration using config passed into create_app
    if subdomain:
        app.config.from_object(get_subdomain_based_config(subdomain))

    # Instantiate stuff using the configuration variables
    app.fake_api_requester = FakeApiRequester(app.config['API_HOST'])
    app.fake_database = FakeDatabase(app.config['DB_SERVER'])

    app.register_blueprint(simple_page)

    return app


if __name__ == '__main__':
    import subdomaindevserver
    subdomaindevserver.run(create_app, host='0.0.0.0', port=5000)
