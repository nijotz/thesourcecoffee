import os

DATABASES = {
    "default": {
        # Ends with "postgresql_psycopg2", "mysql", "sqlite3" or "oracle".
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        # DB name or path to database file if using sqlite3.
        "NAME": "%(proj_name)s",
        # Not used with sqlite3.
        "USER": "%(proj_name)s",
        # Not used with sqlite3.
        "PASSWORD": "%(db_pass)s",
        # Set to empty string for localhost. Not used with sqlite3.
        "HOST": "127.0.0.1",
        # Set to empty string for default. Not used with sqlite3.
        "PORT": "",
    }
}

#STRIPE_PUBLIC_KEY = os.environ.get("STRIPE_PUBLIC_KEY", "pk_test_8aFt7ltHKPQ4Pm9CDzhWEyyv")
#STRIPE_SECRET_KEY = os.environ.get("STRIPE_SECRET_KEY", "sk_test_IKVpC0Z3UvwETbTNQMNKHRKl")
STRIPE_PUBLIC_KEY = os.environ.get("STRIPE_PUBLIC_KEY", "pk_live_RAbmHMYx6d3u02qEEgFi8WP2")
STRIPE_SECRET_KEY = os.environ.get("STRIPE_SECRET_KEY", "sk_live_4S00xu51gSTkzpbcVDsmbO3Y")

#SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTOCOL", "https")
#
#CACHE_MIDDLEWARE_SECONDS = 60
#
#CACHE_MIDDLEWARE_KEY_PREFIX = "%(proj_name)s"
#
#CACHES = {
#    "default": {
#        "BACKEND": "django.core.cache.backends.memcached.MemcachedCache",
#        "LOCATION": "127.0.0.1:11211",
#    }
#}
#
#SESSION_ENGINE = "django.contrib.sessions.backends.cache"
