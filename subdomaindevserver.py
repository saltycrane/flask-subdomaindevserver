import subprocess

from werkzeug.serving import WSGIRequestHandler, run_simple


# global flag
reloadme = False


class SubdomainDispatcher(object):
    """Modified from http://flask.pocoo.org/docs/patterns/appdispatch/#dispatch-by-subdomain

    WSGI middleware that allows for configuring a Flask app using the
    subdomain of the incoming request.

     - If the subdomain is different from the previous request, this
       file is touched so that the Werkzeug dev server will reload
     - After reload, the app_factory is called with an additional
       keyword argument, subdomain. The app_factory should configure the
       Flask app based on this argument.
     - SubdomainDispatcher must be used with SubdomainRequestHandler
       because it uses the global flag, reloadme to reload the dev
       server.
     - The original SubdomainDispatcher on pocoo.org stored a dict of
       app instances. This worked very well when all the configuration
       was specific to the app. However in the unique case where
       configuration occurs at the module (global) level, this did not
       work. This is the reason the dev server is reloaded. Reloading
       the dev server starts a new process so module level configuration
       will be cleared.

    """

    def __init__(self, app_factory, *args, **kwargs):
        """
        :param app_factory: a function that returns a `flask.Flask` instance
            and accepts a keyword argument, "subdomain".
        :param args: *args passed to app_factory
        :param kwargs: **kwargs passed to app_factory
        """
        self.app_factory = app_factory
        self.args = args
        self.kwargs = kwargs
        self.subdomain = None
        self.app = None

    def __call__(self, environ, start_response):
        self._get_application(environ['HTTP_HOST'])
        return self.app(environ, start_response)

    def _get_application(self, host):
        global reloadme

        parts = host.split('.')
        subdomain = parts[0] if len(parts) > 1 else None

        if self.app and subdomain != self.subdomain:
            # If the subdomain is different, set reload to True. Setting
            # reload to True should cause the dev server to reload which
            # should clear memory which should make self.app = None. So
            # it will create a new app on the next request below.
            self.subdomain = None
            reloadme = True
        else:
            reloadme = False

        if not self.app:
            self.subdomain = subdomain
            self.kwargs['subdomain'] = subdomain
            self.app = self.app_factory(*self.args, **self.kwargs)


class SubdomainRequestHandler(WSGIRequestHandler):

    def handle_one_request(self):
        """Handle a single HTTP request."""
        self.raw_requestline = self.rfile.readline()
        if not self.raw_requestline:
            self.close_connection = 1
        elif self.parse_request():
            rv = self.run_wsgi()

            if reloadme:
                # TODO: is there a better way to reload the server than touching a file?
                filename = __file__
                if filename[-4:] in ('.pyc', '.pyo'):
                    filename = filename[:-1]
                subprocess.call(['touch', filename])

            return rv


def run(app_factory, host=None, port=None, debug=True, **options):
    """
    Modified from `flask.Flask.run` to use the SubdomainDispatcher
    middleware and the SubdomainRequestHandler request handler.

    :param app_factory: a function that returns a `flask.Flask` instance
        and accepts a keyword argument, "subdomain".

    """
    if host is None:
        host = '0.0.0.0'
    if port is None:
        port = 5000
    options.setdefault('use_reloader', debug)
    options.setdefault('use_debugger', debug)

    app = SubdomainDispatcher(app_factory, debug=debug)

    run_simple(
        host, port, app, request_handler=SubdomainRequestHandler, **options)
