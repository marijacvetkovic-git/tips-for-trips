import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or '29f1e0c0aa878d75764d2deb8c758f2d'
    WTF_CSRF_ENABLED=False