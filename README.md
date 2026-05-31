# Hawkstronix Shop — Update Server

This repo hosts the **version manifest** that the Hawkstronix Shop desktop app
polls on launch. The app fetches `version.json`, compares it to its own
`APP_VERSION`, and — if a newer version exists — offers to download and install
the new build.

```
Hawks Shop app  ──GET version.json──▶  raw.githubusercontent.com/.../version.json
        │
        ▼  version > APP_VERSION ?
   yes → prompt → download windows_url → run installer
```

**Manifest URL the app reads (raw, main branch):**
```
https://raw.githubusercontent.com/jhonnyzs/Hawks-shop-Auto-update/main/version.json
```
(The app appends a cache-buster to dodge the ~5-min GitHub raw CDN cache.)

## `version.json` fields

| Field           | Meaning                                                         |
| --------------- | -------------------------------------------------------------- |
| `version`       | The newest version, e.g. `1.1.0`. App compares vs `APP_VERSION`.|
| `releaseDate`   | `YYYY-MM-DD`.                                                   |
| `forceUpdate`   | `true` to make the update mandatory.                           |
| `windows_url`   | Direct download for `HawksShop.exe` (a GitHub Release asset).  |
| `fileSizeBytes` | Size of the download (0 if unknown).                           |
| `sha256`        | Checksum of the download (optional).                           |
| `changelog`     | List of human-readable notes shown to the user.                |

## Releasing a new version (one click)

From the app folder (`Hawks Shop`), run **`release.bat`** (double-click it).
It bumps the version, rebuilds `HawksShop.exe`, runs the **self-test gate**
(won't publish a broken build), then commits the new `HawksShop.exe` +
`version.json` into **this** repo and pushes. The app downloads the exe straight
from the committed **raw URL** above — so **no GitHub Release is needed**.

```
release.bat                bump patch + publish
release.bat minor          bump minor
release.bat --no-publish   build only, don't upload
```

> The standalone `release.py` in this repo is just a manual fallback for editing
> `version.json` by hand.
