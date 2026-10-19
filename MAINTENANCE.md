# 中文版维护记录

长期分支：`zh-cn`。原项目远程：`upstream`。当前上游基线和官方发行文件校验值见 `zh-upstream.json`。

2026-10-16：保存并标记 `v2.0.3-zh-fix2`（2498b44）；将上游 `v2.0.4-base` 合入维护分支。保留已有中文字体、官方译名、盲注与商店按键提示、上屏和下屏布局修正。接入 2.0.4 的失败页面 A 键、Boss 信息位置和牌组查看时的提示遮挡修复，以及卡面即时应用逻辑。新增语言实际是丹麦语，修正上游 English/简中名称，并把新增汉字加入字体子集。

2026-10-19：同步稳定发行版 `v2.0.5-base`（43497eb8f798cb3d794975de1b0e9f7a56ac53bb），本地修订号 1。接入牌组效果重置、四指计分、补充包跳过与焦点恢复、红牌和篝火触发、百搭牌、若干消耗牌限制及 Boss 效果修复，并新增西班牙语。保留已有官方简中名称与字体、颜色信息和排版修正，语言菜单显示“西班牙语”，字库增至 967 字符。

本轮唯一的合并冲突位于取消键释放逻辑：同时保留上游的“按键在商店开始才允许长按离开”与本地的商店焦点可退出、拖动和连选保护。补充包中开始的 B 键不会误离开商店；重绑定的取消键遵循相同规则。旧版可通过 `v2.0.4-zh-fix1` 回退。

2.0.5 验证：242 项相关回归检查通过；327 个官方名称一致、无缺失翻译键或占位符差异；五个原生字库共 967 字符覆盖完整；84 种盲注布局、28 种 Boss 上屏说明和八个双屏桌面预览通过；CIA 解包 648 个文件核对一致，原生代码、权限及主页图标和音乐与官方 2.0.5 一致。尚未真机验证。

用户于 2026-10-19 要求上传到其原项目 fork：`https://github.com/the1ndex/Balatro3DS`。远程名称为 `fork`，中文维护代码使用 `zh-cn` 分支，现有 `main` 保留。同步上传 `v2.0.3-zh-fix2`、`v2.0.4-zh-fix1`、`v2.0.5-zh-fix1` 三个本地版本标签。该 fork 为公开仓库。此前的自动监控和 GitHub 通知订阅没有设置成功；此次代码推送不代表后台监控或自动发布已开启。

## 后续同步

先运行 `python dev/check_upstream.py` 检查稳定发行版。若有新版，按 `AGENTS.md` 中的流程合并。`git fetch upstream --tags --prune` 只更新本地远程记录，不改工作代码；`git merge --no-ff <发行标签>` 接入新版，避免覆盖我们的提交。确认整合完成后更新版本记录并打标签。

## 本机检查和构建

项目已有 Python 环境位于 `D:/prj/Balatro3DS/work/venv/Scripts/python.exe`。以下命令从本仓库执行：

```text
python dev/test_zh.py
python dev/audit_zh_translation.py
python dev/verify_zh_font.py
python dev/build_zh_font.py
python dev/prepare_zh_release.py
python dev/repack_zh_release.py
python dev/validate_zh_release.py
```

字体需要在变更文字后用 dev/build.sh，或用 mkbcfnt 和 dev/bake_cjk_font.py 重建 13/17/21/27/33 五个原生高度。prepare 从 manifest 所列官方 URL 获取 CIA，校验 SHA-256 后提取官方运行时。repack 和 validate 共用相同 manifest，输出按版本归档到项目 outputs，保留旧安装包。

打包脚本使用本机项目 work 中已有的 CTR 工具和开发依赖；完整源码构建也可按上游 dev/setup.sh、dev/build.sh 执行。真机验证仍需另外记录，桌面预览不能代替真机结果。

2.0.4 验证记录：110 项回归检查通过；327 个名称对照一致；字库 966 字符及五个原生字号检查通过；84 种盲注布局和 28 种 Boss 上屏说明边界检查通过；八个桌面双屏预览通过。Boss 中文说明使用完整面板宽度，与目标分数分区显示。真机验证尚未进行。
