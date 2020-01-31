# Keypirinha launcher (keypirinha.com)

import keypirinha as kp
import keypirinha_util as kpu
import os
import sqlite3
import re


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
    DEFAULT_PATH_TO_GALAXY_CLIENT = "%PROGRAMFILES(X86)%\\GOG Galaxy"
    DB_NAME = "galaxy-2.0.db"
    DEFAULT_DB_PATH = "%PROGRAMDATA%\\GOG.com\\Galaxy\\storage"
    DEFAULT_WEBCACHE_PATH = "%PROGRAMDATA%\\GOG.com\\Galaxy\\webcache"

    # Variables
    path_to_galaxy_client = os.path.expandvars(DEFAULT_PATH_TO_GALAXY_CLIENT)
    path_to_exe = os.path.join(path_to_galaxy_client, EXE_NAME)
    path_to_db = os.path.expandvars(DEFAULT_DB_PATH)
    path_to_db_file = os.path.join(path_to_db, DB_NAME)
    path_to_webcache = os.path.expandvars(DEFAULT_WEBCACHE_PATH)
    platforms = {}

    def __init__(self):
        super().__init__()

    def on_start(self):
        self._read_config()

    def on_catalog(self):
        self._load_platforms()
        games = self._load_games()

        self._load_icons(games)

        catalog = []
        for game in games:
            catalog.append(self._create_launch_item(game))

        self.set_catalog(catalog)

    def on_suggest(self, user_input, items_chain):
        pass

    def on_execute(self, item, action):
        kpu.shell_execute(
            self.path_to_exe,
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

    def _load_platforms(self):
        self.platforms = {}

        vendor_js = kpu.slurp_text_file(os.path.join(self.path_to_galaxy_client, "web\\vendor.js"))

        platform_ids = {}
        for m in re.finditer("PlatformId\\[\\\"(.*)\\\"\\] = \\\"(.*)\\\";", vendor_js):
            platform_ids[m.group(1)] = m.group(2)

        for m in re.finditer("AccountFullPlatformName\\[\\\"(.*)\\\"\\] = \\\"(.*)\\\";", vendor_js):
            self.platforms[platform_ids[m.group(1)]] = m.group(2)

    def _load_games(self):
        games = []
        try:
            connection = sqlite3.connect(self.path_to_db_file)
            c = connection.cursor()

            queries = [
                'SELECT p.name as platform, gp.releaseKey, substr(gp.value, 11, length(gp.value)-12) as title from GamePieces gp, InstalledExternalProducts iep, platforms p WHERE gp.gamePieceTypeId = 3396 AND iep.platformId = p.id AND gp.releaseKey = (p.name || "_" || iep.productId);',
                'SELECT "generic" as platform, le.releaseKey, substr(gp.value, 11, length(gp.value)-12) as title from GamePieces gp, LinkedExecutables le WHERE gp.gamePieceTypeId = 3396 AND gp.releaseKey = le.releaseKey;'
            ]

            for query in queries:
                c.execute(query)
                for row in c.fetchall():
                    platform = row[0]
                    releaseKey = row[1]
                    title = row[2]
                    self.info([platform, releaseKey, title])
                    games.append(Game(platform, releaseKey, title))

            connection.close()

        except:
            self.err("Unable to load database file: " + str(self.path_to_db))

        return games

    def _create_launch_item(self, game):
        return self.create_item(
            category=kp.ItemCategory.REFERENCE,
            label="GOG Galaxy: " + game.title,
            short_desc=self.platforms[game.platform] if game.platform in self.platforms else str(game.platform).capitalize(),
            target=game.releaseKey,
            args_hint=kp.ItemArgsHint.FORBIDDEN,
            hit_hint=kp.ItemHitHint.NOARGS,
            icon_handle=self._get_icon(game.releaseKey)
            )

    def _get_icon(self, releaseKey):
        if os.path.exists(self._build_icon_cache_path(releaseKey)):
            return self.load_icon("cache://{}/icons/{}.png".format(self.package_full_name(), releaseKey))

    def _build_icon_cache_path(self, releaseKey):
        return os.path.join(self.get_package_cache_path(), "icons", releaseKey + ".png")

    def _load_icons(self, games):
        connection = sqlite3.connect(self.path_to_db_file)
        c = connection.cursor()

        icons_cache_path = os.path.join(self.get_package_cache_path(True), "icons")
        if not os.path.exists(icons_cache_path):
            os.mkdir(icons_cache_path)

        for game in games:
            cache_path = self._build_icon_cache_path(game.releaseKey)
            if not os.path.exists(cache_path):
                c.execute('SELECT wcr.userId, ogl.gameId, wcr.filename FROM WebCacheResources wcr, OriginalGameLinks ogl WHERE wcr.webCacheResourceTypeId=2 AND wcr.releaseKey=? AND ogl.releaseKey=wcr.releaseKey', (game.releaseKey, ))
                row = c.fetchone()
                if row is not None:
                    original_path = os.path.join(self.path_to_webcache, str(row[0]), game.platform, row[1], row[2])
                    if (os.path.exists(original_path)):
                        # create an empty file first to avoid problems with long running conversion
                        open(cache_path, 'a')
                        kpu.shell_execute("dwebp.exe", (original_path, "-o", cache_path), show=0)

        connection.close()

    def _read_config(self):
        settings = self.load_settings()
        self.path_to_galaxy_client = os.path.expandvars(settings.get_stripped(
            "path_to_galaxy_client",
            "main",
            self.DEFAULT_PATH_TO_GALAXY_CLIENT
            ))

        self.path_to_exe = os.path.join(self.path_to_galaxy_client, self.EXE_NAME)

        self.path_to_db = os.path.expandvars(settings.get_stripped(
            "path_to_db",
            "main",
            self.DEFAULT_DB_PATH
            ))

        self.path_to_db_file = os.path.join(self.path_to_db, self.DB_NAME)

        self.path_to_webcache = os.path.expandvars(settings.get_stripped(
            "path_to_webcache",
            "main",
            self.DEFAULT_WEBCACHE_PATH
            ))

        icon_handle = self.load_icon(
            "@{},0".format(self.path_to_exe))
        if icon_handle:
            self.set_default_icon(icon_handle)
