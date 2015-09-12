import sys
import os.path
  
os.environ['DJANGO_SETTINGS_MODULE'] = 'MoocKitchen.settings'
sys.path.append(os.path.join(os.path.dirname(__file__), 'MoocKitchen'))
  
import sae
from MoocKitchen import wsgi
from sae.ext.storage import monkey
monkey.patch_all()
  
application = sae.create_wsgi_app(wsgi.application)