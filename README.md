## Flask Subdomain Devserver

This module provides a Flask local development server that allows you to
set configuration based on the subdomain of the incoming request.

This requires the Unix command, "touch". Tested on Ubuntu 14.04.

NOTE: the first request after changing the subdomain of the URL will
still use the settings from the previous subdomain. This first request
triggers the devserver to reload and subsequest requests will use the
correct settings for the subdomain.

This code is modified from the Subdomain Dispatcher code on pocoo.org:
http://flask.pocoo.org/docs/0.10/patterns/appdispatch/#dispatch-by-subdomain


### Usage

1. Add the following to your hosts file (/etc/hosts on Ubuntu):

        0.0.0.0 dev.localhost
        0.0.0.0 qa.localhost

2. Create an application factory (http://flask.pocoo.org/docs/0.10/patterns/appfactories/)
   that takes a keyword argument, subdomain, and use it to configure your app.

        def create_app(subdomain=None):
            app = Flask(__name__)

            # Set default configuration
            # ...

            # Override configuration based on the subdomain
            if subdomain == 'dev':
                app.config['API_HOST'] = 'dev-host'
            elif subdomain == 'qa':
                app.config['API_HOST'] = 'qa-host'

            return app

3. Run the Subdomain Devserver

        import subdomaindevserver
        subdomaindevserver.run(create_app, host='0.0.0.0', port=5000)


### To run the example

1. Add the following to your hosts file (/etc/hosts on Ubuntu):

        0.0.0.0 dev.localhost
        0.0.0.0 qa.localhost

2. Install stuff

        cd example
        virtualenv venv
        source venv/bin/activate
        pip install -r requirements.txt

3. Run the local development server

        python myapp.py

4. Visit the following URLs in the browser:
   - <http://localhost:5000/>
   - <http://dev.localhost:5000/>, reload the page in the browser to see the changes take effect
   - <http://qa.localhost:5000/>, reload the page in the browser to see the changes take effect
