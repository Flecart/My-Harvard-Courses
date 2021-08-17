from . import util
from .globals import DEF_IMAGE

def url_cleaner(url):
    try:
        if not util.is_url_image(url):
            return DEF_IMAGE

        return url
    except:
        return DEF_IMAGE
