# Prep your dev environment

    Install virtualbox: https://www.virtualbox.org/
    Build a Linux VM from Ubuntu 12.04: http://www.ubuntu.com/

# Installing the Open Data Catalog
## Non-Python Dependencies

        sudo apt-get update
        sudo apt-get install git sendmail postgresql python postgresql-plpython-9.1 python-pip libpq-dev python-dev libxml2-dev libxslt1-dev libgeos-c1

## Python Dependencies

        sudo pip install virtualenv

## Setting up the App
### Create Virtual Env
Create the shell of the virtual env and "activate" it

        virtualenv opendatacatalog
        cd opendatacatalog
        source bin/activate

### Grab the source
At this point you can grab the source from github:

        git clone git://github.com/azavea/Open-Data-Catalog.git
        cd Open-Data-Catalog

Or fork the code, make it better and send us a pull request!

Grab the python dependencies and do some final setup:

        pip install -r requirements.txt
        cd OpenDataCatalog
        mkdir media
        chmod 755 media
        ln -s ../../lib/python2.7/site-packages/django/contrib/admin admin_media


## Setting up the database
### Create a new postgres db

        sudo su postgres # Become the postgres user
        createuser -P odc-user
        psql template1 -c "CREATE DATABASE opendata OWNER \"odc-user\";"
        createlang plpythonu opendata
        psql -d opendata -f etc/pycsw_plpythonu.sql
        exit # Exit out of the postgres user's shell

Note that running the unit tests requires that your postgres user be a super user (since it drops/creates databases). To create a user as a superuser simply do:

        createuser -Ps odc-user

You can verify the connection with:

        psql opendata odc-user -h localhost

### Update settings

Copy local_settings.py.example to local_settings.py

Update the database settings in local_settings.py. You'll probably have to update "name", "user", "password", and "host". It should look similar to:

        DATABASES = {
           'default': {
               'ENGINE': 'django.db.backends.postgresql_psycopg2',
               'NAME': 'opendata',
               'USER': 'odc-user',
               'PASSWORD': 'PASSWORD',
               'HOST': 'localhost',
               'PORT': '',
           }
        }

Open Data Catalog supports the [OGC Catalogue Service] (http://www.opengeospatial.org/standards/specifications/catalog) specification (CSW) using [pycsw](http://pycsw.org).  CSW settings can be set/modified in `settings.CSW`.  As well, `settings.SITEHOST` and `settings.SITEPORT` must be set accordingly for your deployment environment.

### Email Setup

Open Data Catalog is by default setup to output all emails to the console, instead of sending them via SMTP. You can use a local server, by simply changing the local_settings.py from:

        EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

to:

        EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

Follow the DJango manual to see how to setup your SMTP server:

        https://docs.djangoproject.com/en/dev/topics/email/

### Creating the database scheme

To create the scheme we use django "syncdb" command, using --migrate to apply database migrations

        python manage.py syncdb --migrate

## Running a server
We installed gunicorn as part of the installation process. All you need to do now is start it:

        gunicorn_django


# Customizing your installation

## Settings

You should read OpenDataCatalog/local_settings.py for a list of configurable
values, such as TWITTER_USER and SITE_ROOT.  Feel free to play with these
settings as much as you want.

## Style

In local_settings.py you should specify a LOCAL_TEMPLATE_DIR that is the full
path to your template location.  As you want to change the style, you copy
files out of OpenDataCatalog/templates and into your local overly directory
and make the changes there.  That way you can keep your repository in sync
with the upstream more easily while still maintaining your own style.

# Deploy to Heroku

For a quick and free deployment you can deploy directly to heroku (http://heroku.com). First make an account on the heroku website and then do the following:

        sudo gem install heroku       
        heroku create --stack cedar --buildpack git@github.com:heroku/heroku-buildpack-python.git
        git push heroku master       
        heroku run python OpenDataCatalog/manage.py syncdb


# Apache

Django can run via mod_wsgi on Apache as well. Add the following to a new Apache site:

        WSGIScriptAlias /hidden /<project location>/odp.wsgi
        Alias /media /<project location>/media
        Alias /static /<project location>/static

        create /<project location>/odp.wsgi >
        import os, sys
        sys.path.insert(0, '/home/azavea/NPower_OpenDataPhilly')

        import settings

        import django.core.management
        django.core.management.setup_environ(settings)
        utility = django.core.management.ManagementUtility()
        command = utility.fetch_command('runserver')

        command.validate()

        import django.conf
        import django.utils

        django.utils.translation.activate(django.conf.settings.LANGUAGE_CODE)

        import django.core.handlers.wsgi

        application = django.core.handlers.wsgi.WSGIHandler()


# Nginx

DJango can run behind Nginx by simply forwarding the requests from the web to the local gunicorn_django wsgi server


        server {
        
            listen       80 default;
            server_name  opendataCITY.org www.opendataCITY.org;
            access_log   /<log location>/opendata-site.access.log;
            error_log    /<log location>/opendata-site.error.log;

            # redirect to www
            if ($host !~* ^www\.) {
                rewrite ^(.*)$ http://www.$host$1 permanent;
            }

            location = /biconcave {
                return  404;
            }

            location  /static/ {
            root  /<project location>/Open-Data-Catalog/OpenDataCatalog/;
            }

            location  /media/ {
            root  /<project location>/Open-Data-Catalog/OpenDataCatalog/;
            }


            location  / {
                proxy_pass            http://127.0.0.1:8000/;
                proxy_redirect        off;
                proxy_set_header      Host             $host;
                proxy_set_header      X-Real-IP        $remote_addr;
                proxy_set_header      X-Forwarded-For  $proxy_add_x_forwarded_for;
                proxy_set_header      X-Scheme         $scheme;
                client_max_body_size  10m;
                proxy_connect_timeout 10;
                proxy_read_timeout    10;
            }

        }
