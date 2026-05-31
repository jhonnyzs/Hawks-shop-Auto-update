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

## Releasing a new version

1. In the app, bump `APP_VERSION` in `PC app/src/version.py`, then `build.bat`
   → `dist/HawksShop.exe`.
2. Create a GitHub **Release** here (tag e.g. `v1.1.0`) and attach
   `HawksShop.exe` (the `releases/latest/download/HawksShop.exe` URL then points
   to it).
3. Run `python release.py 1.1.0 "note one" "note two"` to update `version.json`,
   commit and push — the app picks it up on its next launch.
