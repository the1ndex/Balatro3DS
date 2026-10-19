# Balatro3DS — Chinese UI maintenance fork

**English** | [简体中文](README.zh-CN.md)

A Simplified Chinese maintenance fork of [idkhan/Balatro3DS](https://github.com/idkhan/Balatro3DS), focused on official terminology, readable Chinese fonts, layouts that fit the 3DS screens, and consistent button prompts.

The maintained branch is **[`zh-cn`](https://github.com/the1ndex/Balatro3DS/tree/zh-cn)**. The current build is **`v2.0.5-zh-fix1`**, based on upstream **`v2.0.5-base`**. [Maintenance history](MAINTENANCE.md) · [Pinned upstream version](zh-upstream.json)

## What this fork improves

| Area | Changes in this fork |
| --- | --- |
| Official Chinese terminology | Corrected 93 catalog names from the original 2.0.3 Chinese translation. All 327 checked names now match the official Simplified Chinese localization from the maintainer's installed Steam copy. |
| Effect descriptions | Restored omitted details such as free edition-tag cards, Double Tag's self-exclusion, and Ancient Joker's per-round suit change. Ectoplasm reports the hand-size penalty of its next use. |
| Chinese fonts | Added a subset of Noto Sans SC Bold, renamed **Balatro3DS SC**, with normalized line metrics and baselines. Five native font sheets use 13/17/21/27/33 px cells; the current subset contains 967 characters. Roles using the same height share a font object. |
| Upper-screen HUD | Keeps round-score labels, ante ratios, and other readouts within their panels. Boss abilities and target scores have separate space; discovery notifications use a compact footer. |
| Blind selection | Lays out Chinese descriptions using their measured height, keeps punctuation with adjacent text, and fits scores, rewards, and skip controls on the bottom screen. |
| Menus and shop | Fits menu labels to available width and improves deck-page footer readability. Adds a guard against leftover hand cards covering shop items or controls. |
| Button prompts and gestures | Blind selection shows the current confirm/cancel bindings. The shop exit shows the cancel binding and a hold hint. A hold must begin in the shop to leave it; skipping a booster with B cannot also exit the shop. Dragging and sweep selection are protected. |
| Localization structure | Keeps stable translation keys and internal card IDs, preserves existing structured color segments, and retains placeholders for dynamic values. Adds official-name, placeholder, font, and UI regression checks. |

These changes build on the upstream game's rendering, localization, structured tooltips, and input system. The gameplay fixes in 2.0.5—including deck-effect resets, Four Fingers scoring, booster-skip triggers, and Boss behavior—come from upstream and are merged into this branch.

## Interface previews

Desktop dual-screen previews of this fork; these are **not photographs of a 3DS**.

| Blind selection | Shop and button prompts |
| --- | --- |
| ![Chinese blind selection with visible scores, rewards, and button prompts](docs/images/zh-blinds.png) | ![Chinese shop with hold-to-exit and reroll button prompts](docs/images/zh-shop.png) |

## Versions and validation

Source checkpoints are available as Git tags:

- [`v2.0.5-zh-fix1`](https://github.com/the1ndex/Balatro3DS/tree/v2.0.5-zh-fix1) — current upstream base: 2.0.5.
- [`v2.0.4-zh-fix1`](https://github.com/the1ndex/Balatro3DS/tree/v2.0.4-zh-fix1).
- [`v2.0.3-zh-fix2`](https://github.com/the1ndex/Balatro3DS/tree/v2.0.3-zh-fix2).

The 2.0.5 maintenance build passed **242 regression checks**, the **327-name official Chinese comparison**, placeholder checks, and verification of all five native font sheets. Desktop checks cover 84 blind-selection layouts, 28 Boss HUDs, and eight dual-screen scenes. The CIA was extracted and all 648 files were checked; its native code, process settings, HOME Menu icon, and banner audio match the official upstream 2.0.5 package.

**This maintenance build has not yet been verified on a physical 3DS.** These checks cover the cases listed above; they do not establish that every translation, layout, or gameplay interaction is correct.

## Installation and saves

This repository currently publishes the fork's **source branch and version tags**. Fork-specific prebuilt packages have not yet been attached to its GitHub Releases. The [upstream releases](https://github.com/idkhan/Balatro3DS/releases) provide upstream builds.

For a CIA built from this branch, use **FBI** on a 3DS with custom firmware. The title ID is **`000400000BA1A700`**, matching upstream 2.x, so it updates the same installed title. Keep a save backup before changing versions. The save directory remains:

```text
SD:/3ds/save/Balatro3DS/sdmc/
```

For a `.3dsx` built from this branch, place it in the SD card's `3ds` directory and launch it through the Homebrew Launcher. Mods use `/3ds/save/Balatro3DS/sdmc/mods`; see [MODDING.md](MODDING.md) for supported APIs and limitations.

Default shortcuts relevant to this fork:

| Screen | Action |
| --- | --- |
| Blind selection | **A** selects the available blind; **B** skips an eligible blind. |
| Shop | **X** rerolls; hold **B** for at least 0.4 seconds to leave. |
| Booster pack | **B** skips the pack; releasing it afterward keeps you in the shop. |

Prompts follow remapped bindings. The touch screen remains usable alongside buttons.

## Building and maintaining

For a full build, follow the upstream setup instructions:

```bash
./dev/setup.sh
./dev/build.sh        # CIA
./dev/build.sh 3dsx   # 3DSX
```

Full-build output goes to `dev/dist/`. Chinese font generation requires Python and `fonttools`, in addition to the upstream build dependencies.

The fork also includes maintenance checks:

```bash
python dev/test_zh.py
python dev/audit_zh_translation.py --official-game /path/to/Balatro.exe
python dev/verify_zh_font.py
```

These checks require `lupa` and `fonttools`. The translation audit reads the official localization from your own installed game; it does not download it. The release-repacking scripts in `dev/` use a pinned official CIA and the maintainer's local CTR tools; they are not a standalone build environment. See [MAINTENANCE.md](MAINTENANCE.md) for that workflow and [BUILD.md](BUILD.md) for the older manual 3DSX recipe.

Updates are merged from stable upstream releases, then translations, fonts, inputs, affected layouts, and packages are checked. Previous version tags are retained for comparison and rollback. Background update monitoring and automatic publishing are not currently enabled.

## Credits and licenses

- [idkhan/Balatro3DS](https://github.com/idkhan/Balatro3DS) and its contributors: the original 3DS remake and ongoing gameplay work, including contributions from rosematcha.
- Fussyzhy: the upstream Simplified Chinese localization on which these revisions build.
- [LövePotion](https://github.com/lovebrew/lovepotion), TurtleP, and devkitPro: the homebrew runtime and toolchain.
- LocalThunk and the original Balatro creators: the game, artwork, and audio. Please support the original game.

This is an unofficial fan project and is not affiliated with LocalThunk. See [LICENSE](LICENSE) for the project's code license, and [OFL-zh_CN.txt](resources/fonts/OFL-zh_CN.txt) for the Chinese font's SIL Open Font License 1.1. Original game assets retain their original attribution.
