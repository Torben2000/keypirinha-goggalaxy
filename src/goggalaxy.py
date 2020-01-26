# Keypirinha launcher (keypirinha.com)

import keypirinha as kp
import keypirinha_util as kpu
import os


class goggalaxy(kp.Plugin):
    """
    Launcher for GOG Galaxy 2.0 games.

    This does not only work for GOG native games but also for all the other
    games the new client supports (other game launchers, manually added games).
    """

    # Constants
    EXE_NAME = "GalaxyClient.exe"
    DEFAULT_PATH = "%PROGRAMFILES(X86)%\\GOG Galaxy\\"
    DEFAULT_PATH_TO_GALAXY_CLIENT = DEFAULT_PATH + EXE_NAME
    DB_NAME = "galaxy-2.0.db"
    DEFAULT_DB_PATH = "%PROGRAMDATA%\\GOG.com\\Galaxy\\storage\\"
    DEFAULT_DB = DEFAULT_DB_PATH + DB_NAME

    # Variables
    path_to_galaxy_client = DEFAULT_PATH_TO_GALAXY_CLIENT
    path_to_db = DEFAULT_DB

    def __init__(self):
        super().__init__()

    def on_start(self):
        self._read_config()

    def on_catalog(self):
        self.set_catalog([self._create_launch_item()])

    def on_suggest(self, user_input, items_chain):
        pass

    def on_execute(self, item, action):
        kpu.shell_execute(
            os.path.expandvars(self.path_to_galaxy_client),
            ["/command=runGame", "/gameId=" + item.target()]
            )

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
        self.path_to_galaxy_client = settings.get_stripped(
            "path_to_galaxy_client",
            "main",
            self.DEFAULT_PATH_TO_GALAXY_CLIENT
            )
        self.path_to_db = settings.get_stripped(
            "path_to_db",
            "main",
            self.DEFAULT_DB
            )

        icon_handle = self.load_icon(
            "@{},0".format(self.path_to_galaxy_client))
        if icon_handle:
            self.set_default_icon(icon_handle)
