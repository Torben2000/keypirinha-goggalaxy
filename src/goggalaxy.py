# Keypirinha launcher (keypirinha.com)

import keypirinha as kp
import keypirinha_util as kpu
import os
import sqlite3


class Game():
    def __init__(self, platform, releaseKey, title):
        self.platform = platform
        self.releaseKey = releaseKey
        self.title = title


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
        games = self._load_games()

        catalog = []
        for game in games:
            catalog.append(self._create_launch_item(game))

        self.set_catalog(catalog)

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
        if flags & kp.Events.PACKCONFIG:
            self.info("Configuration changed, rebuilding catalog...")
            self._read_config()
            self.on_catalog()

    def _load_games(self):
        games = []
        try:
            connection = sqlite3.connect(os.path.expandvars(self.path_to_db))
            c = connection.cursor()
            c.execute('SELECT p.name as platform, gp.releaseKey, substr(gp.value, 11, length(gp.value)-12) as title from GamePieces gp, InstalledExternalProducts iep, platforms p WHERE gp.gamePieceTypeId = 3396 AND iep.platformId = p.id AND gp.releaseKey = (p.name || "_" || iep.productId);')
        except:
            self.err("Unable to load database file: " + str(self.path_to_db))
            return games

        for row in c.fetchall():
            platform = row[0]
            releaseKey = row[1]
            title = row[2]
            self.info([platform, releaseKey, title])
            games.append(Game(platform, releaseKey, title))

        return games

    def _create_launch_item(self, game):
        return self.create_item(
            category=kp.ItemCategory.KEYWORD,
            label="GOG Galaxy: " + game.title,
            short_desc=game.platform,
            target=game.releaseKey,
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
