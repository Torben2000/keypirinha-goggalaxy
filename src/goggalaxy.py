# Keypirinha launcher (keypirinha.com)

import keypirinha as kp
import keypirinha_util as kpu
import keypirinha_net as kpnet
import os

class goggalaxy(kp.Plugin):
    """
    One-line description of your plugin.

    This block is a longer and more detailed description of your plugin that may
    span on several lines, albeit not being required by the application.

    You may have several plugins defined in this module. It can be useful to
    logically separate the features of your package. All your plugin classes
    will be instantiated by Keypirinha as long as they are derived directly or
    indirectly from :py:class:`keypirinha.Plugin` (aliased ``kp.Plugin`` here).

    In case you want to have a base class for your plugins, you must prefix its
    name with an underscore (``_``) to indicate Keypirinha it is not meant to be
    instantiated directly.

    In rare cases, you may need an even more powerful way of telling Keypirinha
    what classes to instantiate: the ``__keypirinha_plugins__`` global variable
    may be declared in this module. It can be either an iterable of class
    objects derived from :py:class:`keypirinha.Plugin`; or, even more dynamic,
    it can be a callable that returns an iterable of class objects. Check out
    the ``StressTest`` example from the SDK for an example.

    Up to 100 plugins are supported per module.

    More detailed documentation at: http://keypirinha.com/api/plugin.html
    """
    # Constants
    DEFAULT_PATH_TO_GALAXY_CLIENT = "%PROGRAMFILES(X86)%\\GOG Galaxy\\GalaxyClient.exe"

    # Variables
    path_to_galaxy_client = DEFAULT_PATH_TO_GALAXY_CLIENT

    def __init__(self):
        super().__init__()

    def on_start(self):
        self._read_config()

    def on_catalog(self):
        self.set_catalog([self._create_launch_item()])

    def on_suggest(self, user_input, items_chain):
        pass

    def on_execute(self, item, action):
        kpu.shell_execute(os.path.expandvars(self.path_to_galaxy_client), ["/command=runGame", "/gameId=" + item.target()])

    def on_activated(self):
        pass

    def on_deactivated(self):
        pass

    def on_events(self, flags):
        pass

    def _create_launch_item(self):
        return self.create_item(
            category=kp.ItemCategory.KEYWORD,
            label="GOG-Test",
            short_desc="2nd line",
            target="generic_51153138506417067",
            args_hint=kp.ItemArgsHint.FORBIDDEN,
            hit_hint=kp.ItemHitHint.NOARGS
            )

    def _read_config(self):
        settings = self.load_settings()
        self.path_to_galaxy_client = settings.get_stripped("path_to_galaxy_client", "main", self.DEFAULT_PATH_TO_GALAXY_CLIENT)
        icon_handle = self.load_icon("@{},0".format(self.path_to_galaxy_client))
        if icon_handle:
            self.set_default_icon(icon_handle)

