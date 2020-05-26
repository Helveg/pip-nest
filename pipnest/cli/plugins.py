import pkg_resources
from ..exceptions import *


def discover(category, *args, **kwargs):
    plugins = []
    for plugin in pkg_resources.iter_entry_points("pipnest." + category):
        try:
            advert = plugin.load()
            # Load the advertised object, and create an instance of it.
            instance = advert(*args, **kwargs)
            instance.__name__ = plugin.name
            plugins.append(instance)
        except:
            raise PluginError("Could not instantiate the `{}` plugin".format(plugin.name))
    return plugins
