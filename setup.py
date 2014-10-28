
from setuptools import setup


setup(
    name='Flask-SubdomainDevserver',
    version='0.1.1',
    url='http://github.com/saltycrane/flask-subdomaindevserver/',
    license='BSD',
    author='Eliot',
    author_email='saltycrane@gmail.com',
    description='Flask subdomain devserver',
    py_modules=['subdomaindevserver'],
    install_requires=[
        "Werkzeug>=0.9.6",
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)
