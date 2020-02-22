# Keypirinha Plugin: goggalaxy

This is goggalaxy, a plugin for the [Keypirinha](http://keypirinha.com)
launcher.

It enables launching of installed games that are available in
[GOG Galaxy 2.0](https://www.gogalaxy.com/). It supports all platforms that work
within GOG Galaxy 2.0 including manually added games.

**INFO:** Only supports version 2.0 of GOG Galaxy which is currently in beta
state. It is not intended to be used with GOG Galaxy 1.x!

**INFO 2:** For individual game icon support `dwebp.exe` is needed. See
*Install* section below for details.


## Install

### Option 1: Managed

Use [PackageControl](https://github.com/ueffel/Keypirinha-PackageControl) to
to install the plugin.

### Option 2: Manual

You can download the latest release from the
[releases](https://github.com/Torben2000/keypirinha-goggalaxy/releases) page.

Once the `goggalaxy.keypirinha-package` file is downloaded, move it to the
`InstalledPackage` folder located at:

* `Keypirinha\portable\Profile\InstalledPackages` in **Portable mode**
* **Or** `%APPDATA%\Keypirinha\InstalledPackages` in **Installed mode** (the
  final path would look like
  `C:\Users\%USERNAME%\AppData\Roaming\Keypirinha\InstalledPackages`)

### Optional
For individual game icons (instead of the generic GOG Galaxy icon), the icons
used within GOG Galaxy 2.0 need to be converted from WebP to a format that is
compatible with Keypirinha. To achieve this, the plugin uses `dwebp.exe`.
2 steps are necessary to make it work:

1. Download it from https://developers.google.com/speed/webp/download.
2. Make the `dwebp.exe` available to the plugin by
   * **Either** putting it into a folder that is within the system's path
   * **Or** putting it anywhere and configuring the plugin to use this folder by
   setting the `path_to_dwebp` setting.


## Usage

Games that are installed and available within GOG Galaxy 2.0 should work
out-of-the-box. Just search for them with Keypirinha and launch them normally
(prefix in search results is `GOG Galaxy`).

If you installed GOG Galaxy 2.0 somewhere else or your database is not in the
standard location, adjust the plugin's configuration.

If it is still not working or you feel it is not behaving correctly, check
Keypirinha's console for details and/or report an
[issue](https://github.com/Torben2000/keypirinha-goggalaxy/issues).


## Change Log

### v1.1

* New features
  * Open game detail view ([#2](https://github.com/Torben2000/keypirinha-goggalaxy/issues/2))
  * Search in all games incl. uninstalled ([#3](https://github.com/Torben2000/keypirinha-goggalaxy/issues/3))
  * Uninstall games (experimental, might resolve [#1](https://github.com/Torben2000/keypirinha-goggalaxy/issues/1))

### v1.0.1

* Support for GOG games
* Remove hardcoded id that is individual per installation

### v1.0

* Initial release


## License

This package is distributed under the terms of the MIT license.


## Contribute

If you find any bugs or have suggestions for further features, please file an
[issue](https://github.com/Torben2000/keypirinha-goggalaxy/issues).

If you want to contribute directly to the code, just fork the repo, do your
changes and create a pull request.
