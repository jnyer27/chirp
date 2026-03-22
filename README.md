# CHIRP (RadioDroid fork)

This repository is **[jnyer27](https://github.com/jnyer27)’s fork** of [CHIRP](https://www.chirpmyradio.com), maintained for **[RadioDroid](https://github.com/jnyer27/RadioDroid)** — an Android app that runs CHIRP’s Python radio drivers on-device (via [Chaquopy](https://chaquo.com/chaquopy/)) for USB OTG and Bluetooth LE programming.

## Purpose

- **Submodule source** — RadioDroid vendors this tree at `AndroidRadioDroid/app/src/main/python/chirp`. Clones use `git submodule update` against this fork so every pinned commit is reachable.
- **RadioDroid–specific fixes** — Patches that support Android (e.g. clone/mmap behavior, settings hooks) or drivers validated mainly on RadioDroid may land here before or instead of [upstream CHIRP](https://github.com/kk7ds/chirp).
- **Upstream tracking** — Day-to-day CHIRP development still happens on **kk7ds/chirp**. This fork is periodically merged or rebased from `upstream/master` to stay current.

For submodule URLs, cloning, and bumping the pinned revision in RadioDroid, see [RadioDroid’s CHIRP submodule notes](https://github.com/jnyer27/RadioDroid/blob/main/docs/CHIRP_SUBMODULE.md).

## Contributing

- **Changes intended for all CHIRP users** — Prefer opening a PR against **[kk7ds/chirp](https://github.com/kk7ds/chirp)**; upstream rules and the PR template there apply: [.github/pull_request_template.md](.github/pull_request_template.md).
- **RadioDroid-only or experimental driver work** — Develop here or on a branch, then push; update the submodule pointer in the RadioDroid repo when you cut a release or bump CHIRP.

---

*CHIRP is free open-source software. Upstream project: [chirpmyradio.com](https://www.chirpmyradio.com).*
