import os


SITE_ROOT = 'http://www.opendatacincy.org'

ALLOWED_HOSTS = [
    '.opendatacincy.org', # Allow domain and subdomains
    '.opendatacincy.org.', # Also allow FQDN and subdomains
]

# Theme info
#LOCAL_STATICFILE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__),
#                               '../../ODC-overlay/static'))
#LOCAL_TEMPLATE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__),
#                             '../../ODC-overlay/templates'))

# ReCatchpa stuff
RECAPTCHA_PUBLIC_KEY = '6LcPxeUSAAAAAEFHswjx_dGd3SE8SXwh0HldDEeJ'
RECAPTCHA_PRIVATE_KEY = '6LcPxeUSAAAAAFIgNtj5FoingGxiAa_yjkjI5l3q'

# Twitter stuff
TWITTER_USER = None

# AWS Credentials for Warehouse stuff
AWS_ACCESS_KEY = None
AWS_SECRET_KEY = None

# Contacts
mx_host = 'opendatacincy.org'
ADMINS = (
     ('OpenData Admins', 'admin@%s' % (mx_host,)),
)
CONTACT_EMAILS = ['info@%s' % (mx_host,),]
DEFAULT_FROM_EMAIL = 'OpenData Site <noreply@%s>'
EMAIL_SUBJECT_PREFIX = '[OpenDataCatalog - Cincinnati] '
SERVER_EMAIL = 'OpenData Team <info@%s>' % (mx_host,)

MANAGERS = (
     ('OpenData Team', 'info@%s' % (mx_host,)),
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'opendata',                      # Or path to database file if using sqlite3.
        'USER': 'odc-user',                      # Not used with sqlite3.
        'PASSWORD': 'odcCincyD4ta',                  # Not used with sqlite3.
        'HOST': 'localhost',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'thisissomesecuredata'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
