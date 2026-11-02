import sys
from importlib import import_module

import siglus_ssu as _runtime
from . import CONST_PROFILE_IDS, command_name as _prog, package_version


def _print_version() -> None:
    p = _prog()
    sys.stdout.write(f"{p} {package_version() or 'unknown'}\n")


def _usage():
    p = _prog()
    text = (
        f"{p} {package_version() or 'unknown'}\n"
        f"用法：{p} [-h] [-V|--version] [--legacy] [--legacy-full] [--const-profile N] [--string-xor-multiplier N] (-lsp|-c|-x|-a|-d|-k|-e|-m|-g|-s|-v|-p|test) [args]\n"
        "\n"
        "選項：\n"
        "  -V, --version   顯示版本資訊後結束\n"
        "  --legacy        強制使用 Python 編譯後端（仍啟用原生輔助功能）\n"
        "  --legacy-full   停用所有 Rust 原生加速功能\n"
        f"  --const-profile 選擇常數設定檔（{', '.join(map(str, CONST_PROFILE_IDS))}；預設：0；3 支援 TheGodofDeath HD；4 支援 Rewrite；5 支援 nanami/Kisaragi；6 允許屬性出現在命令之外；7 支援 Rurumi/Yamiiro；8 支援 Rewrite trial；9 支援 Rewrite Harvest festa!；10 重建 FlixEngine；不可與 -c --tmp 同時使用）\n"
        "  --string-xor-multiplier 覆寫場景字串 XOR 乘數（0..0xFFFF；預設：profile 3、5、8 為 0，其餘為 0x7087；0 只停用此 XOR）\n"
        "  --              放在模式名稱之後時，將其餘所有引數視為位置引數\n"
        "\n"
        "模式：\n"
        "  -lsp            啟動 SiglusSceneScript 語言伺服器（stdio LSP）\n"
        "  -c, --compile   編譯腳本\n"
        "  -x, --extract   解包／反編譯 .pck、反組譯 .dat，或從 Gameexe.dat 還原 Gameexe.ini\n"
        "  -a, --analyze   分析／比較檔案\n"
        "  -d, --db        匯出／套用／分析 .dbs\n"
        "  -k, --koe       依角色收集 KOE/EXKOE 語音\n"
        "  -e, --exec      從指定的 #z 標籤執行\n"
        "  -m, --textmap   匯出／套用已編譯 .dat 檔案的文字對照\n"
        "  -g, --g00       解包／分析 .g00 圖片\n"
        "  -s, --sound     解碼／解包／播放 .ovk/.owp/.nwa 音訊\n"
        "  -v, --video     解包／分析 .omv 影片\n"
        "  -p, --patch     修補 SiglusEngine.exe（altkey/lang/info/loc）\n"
        "  test            對 .pck 內嵌來源或反編譯腳本進行往返測試\n"
        "\n"
        "LSP 模式：\n"
        f"  {p} -lsp [--serial] [--read-sav <read.sav>]\n"
        "    --serial       停用 LSP 工作區預設的平行掃描\n"
        "    --read-sav     載入已儲存的閱讀旗標，供 hover 和 siglus/readFlags requests 使用\n"
        "\n"
        "Compile 模式：\n"
        f"  {p} -c [--debug] [--charset ENC] [--allow-invalid] [--no-os] [--dat-repack] [--no-angou] [--no-lzss] [--serial] [--max-workers N] [--set-shuffle SEED] [--tmp <tmp_dir>] <input_dir> <output_pck|output_dir>\n"
        f"  {p} -c --test-shuffle [seed0] [--csv <seed_csv>] <input_dir> <output_pck|output_dir> <test_dir>\n"
        f"  {p} -c --gei <input_dir|Gameexe.ini> <output_dir>\n"
        "    --debug         保留暫存檔以供檢查（不可與 --tmp 同時使用）\n"
        "    --charset ENC   強制指定來源字元編碼（Python codec 名稱）\n"
        "    --allow-invalid 解碼時以 U+FFFD 取代無效的來源位元組\n"
        "    --no-os         編譯後移除來源資料區塊，但保留封包標頭\n"
        "    --dat-repack    重新封裝 input_dir 中現有的 .dat 檔案（模式選項僅限 --no-os/--no-lzss；仍可使用全域選項）\n"
        "    --no-angou      停用加密／壓縮（不可與 --tmp 同時使用）\n"
        "    --no-lzss       停用場景 LZSS 並省略來源資料區塊（官方 easy link；不可與 --tmp 同時使用）\n"
        "    --serial        停用平行編譯\n"
        "    --max-workers   將平行工作執行緒限制為正整數（預設：自動；僅平行模式）\n"
        "    --set-shuffle   設定 .dat 字串順序的初始 shuffle seed（MSVCRand）；會啟用 --serial（不可與 --tmp 同時使用）\n"
        "    --tmp           使用指定的暫存目錄（不可與 --debug/--dat-repack/--no-angou/--no-lzss/--set-shuffle/--test-shuffle/--csv/--gei/--const-profile 同時使用）\n"
        "    --test-shuffle  暴力搜尋 .dat 字串順序的初始 shuffle seed（MSVCRand；不可與 --tmp/--gei 同時使用）\n"
        "    --csv           搭配 --test-shuffle 使用，將每個物件的初始／最終 seed 寫入 CSV（不可與 --tmp 同時使用）\n"
        "    --gei           僅在 Gameexe.ini 存在時產生 Gameexe.dat；若找不到輸入檔，會顯示警告並略過（不可與 --tmp/--test-shuffle 同時使用）\n"
        "\n"
        "Extract 模式：\n"
        f"  {p} -x <input_pck> [output_dir] [--angou VALUE]\n"
        f"  {p} -x [--disam|--decompile] <input_pck> [output_dir] [--angou VALUE]\n"
        f"  {p} -x --disam <input_dir> [output_dir] [--angou VALUE]\n"
        f"  {p} -x --gei <Gameexe.dat|input_dir> [output_dir] [--angou VALUE]\n"
        "    --disam        解包 .pck 或掃描 .dat 目錄時，輸出 .dat 反組譯內容\n"
        "    --decompile    輸入完整的 .pck 時，輸出 .dat 反組譯內容及重建的 decompiled/*.ss 腳本\n"
        "    --gei          從 Gameexe.dat 還原 Gameexe.ini\n"
        "    output_dir     預設為輸入檔所在目錄，或輸入目錄本身\n"
        "\n"
        "Analyze 模式：\n"
        f"  {p} -a <input_file.pck> [--angou VALUE]\n"
        f"  {p} -a [--disam] <input_file.dat> [--angou VALUE]\n"
        f"  {p} -a [--readall|--apply] <input_file.sav>\n"
        f"  {p} -a --read-flags <read.sav> [Scene.pck] [--report-json FILE] [--angou VALUE]\n"
        f"  {p} -a <input_file.(gan|sav|cgm|tcr)>\n"
        f"  {p} -a [--payload] <input_file_1.pck> <input_file_2.pck> [--angou VALUE]\n"
        f"  {p} -a [--payload] [--disam] <input_file_1.dat> <input_file_2.dat> [--angou VALUE]\n"
        f"  {p} -a <input_file_1> <input_file_2>\n"
        f"  {p} -a --word <input_pck> [output_csv] [--angou VALUE]\n"
        f"  {p} -a --angou <path|angou=text|key=bytes>\n"
        f"  {p} -a --gei <Gameexe.dat> [Gameexe.dat_2] [--angou VALUE]\n"
        "    --disam        僅適用於 .dat 輸入；在每個分析的 .dat 旁寫入 <scene>.dat.txt\n"
        "    --readall      對 read.sav/global.sav：就地解除已讀或引擎管理的收集旗標，並建立備份\n"
        "    --read-flags   將未讀旗標匯出為 <save_stem>.flags.json；可選擇提供原始來源行的 PCK\n"
        "    --report-json  搭配 --read-flags 使用時，指定 JSON 輸出檔案\n"
        "    --apply        對 global.sav：將同目錄的 global.txt 套用至 G/Z/cg_table/bgm_table/chrkoe，並建立備份\n"
        "    --word         計算 .pck 中每個 .dat/.ss 的對話單位數，並且只輸出 CSV\n"
        "    --payload      比較 .pck/.dat 的正規化場景執行語意，包含 bytecode 及 routing/property 中繼資料；耗時較長\n"
        "    --angou VALUE  .pck/.dat、--word、搭配 PCK 的 --read-flags，或 --gei 的金鑰來源：path、angou=text 或 key=bytes\n"
        "    --gei          分析／比較 Gameexe.dat\n"
        "\n"
        "KOE 模式：\n"
        f"  {p} -k [--stats-only] <scene_input> <voice_dir> <output_dir> [--angou VALUE]\n"
        f"  {p} -k [--stats-only] --single KOE_NO <voice_dir> <output_dir>\n"
        "    --stats-only   只輸出摘要；除非使用 --single，否則也會輸出 CSV；不解包 .ogg 檔案\n"
        "    --single       只將指定的全域 KOE 編號直接解包至 output_dir；不產生 CSV 或角色子目錄\n"
        "\n"
        "Execute 模式：\n"
        f"  {p} -e <path_to_engine> <scene_name> <label>\n"
        "\n"
        "Textmap 模式：\n"
        f"  {p} -m <path_to_dat|path_to_dir> [--angou VALUE]\n"
        f"  {p} -m --apply <path_to_dat|path_to_dir> [--angou VALUE]\n"
        "    --apply        將 .dat.csv 套用回 .dat\n"
        "\n"
        "G00 模式：\n"
        f"  {p} -g --a <input_g00>\n"
        f"  {p} -g --x [--trim] <input_g00|input_dir> <output_dir>\n"
        f"  {p} -g --m [--trim] <input_g00[:cutNNN]> <input_g00[:cutNNN]> [input_g00[:cutNNN] ...] [--o <output_dir>]\n"
        "    注意：可使用後綴 :cutNNN 選擇 type2 cut（例如 foo.g00:cut002）\n"
        "    --trim 搭配 --x 時，會裁切透明或不透明背景的 PNG 邊緣，以及 JPEG 背景邊緣；不會寫入 type2 JSON；搭配 --m 時會裁切合併後的 PNG 邊緣\n"
        f"  {p} -g --c [--type N] [--refer <ref_g00|ref_dir>] <input_png|input_jpeg|input_json(type2 only)|input_dir> [output_g00|output_dir]\n"
        "    注意：未使用 --refer 時，--c 會建立 .g00（支援 type0/type2/type3；JSON 輸入僅接受 --type 2）\n"
        "          使用 --refer 時，--c 會根據參考 .g00 更新，而不是自動將輸出檔案讀取為基底\n"
        "    type2：若存在多個 cut，請使用 name_cut###.png 指定目標 cut\n"
        "\n"
        "Sound 模式：\n"
        f"  {p} -s --x <input_dir|input_file> <output_dir> [--trim <path_to_Gameexe.dat>] [--angou VALUE]\n"
        f"  {p} -s --a <input_file.(nwa|ovk|owp)> [input_file_2.ovk]\n"
        f"  {p} -s --c <input_ogg|input_dir> <output_dir>\n"
        f"  {p} -s --play <input_file.(nwa|owp|ogg)|input_dir> [path_to_Gameexe.dat|Gameexe.ini] [--angou VALUE]\n"
        "\n"
        "DB 模式：\n"
        f"  {p} -d --x <input_dir|input_file> <output_dir>\n"
        f"  {p} -d --a <input_file.dbs> [input_file_2.dbs]\n"
        f"  {p} -d --c [--type N] [--set-shuffle SEED] <input_csv|input_dir> <output_dbs|output_dir>\n"
        f"  {p} -d --c --test-shuffle [skip0] <expected.dbs> <input_csv> <output_dbs>\n"
        "\n"
        "Video 模式：\n"
        f"  {p} -v --x <input_dir|input_file> <output_dir>\n"
        f"  {p} -v --a <input_file.omv>\n"
        f"  {p} -v --c <input_ogv> <output_omv|output_dir> [--refer ref.omv] [--mode N] [--flags 0x18DE00]\n"
        "    --refer  套用參考 .omv 的 mode 和 TableB flags_hi24（可由 --mode/--flags 覆寫）\n"
        "    --mode   覆寫標頭 mode（@0x28），預設：2（YUV）\n"
        "    --flags  覆寫 TableB flags 的高 24 位元，預設：0\n"
        "\n"
        "Patch 模式：\n"
        f"  {p} -p --altkey <input_exe> <input_key> [-o output_exe] [--inplace]\n"
        f"  {p} -p --lang (cjk|cjk-path|config.json) <input_exe> [-o output_exe] [--inplace] [--allow-partial] [--revert]\n"
        f"  {p} -p --info <input_exe>\n"
        f"  {p} -p --loc (0|1) <input_exe> [-o output_exe] [--inplace]\n"
        "    <input_key> 可使用暗号.dat / key.txt / SiglusEngine*.exe / Scene.pck 的檔案路徑、key=bytes 或 angou=text；不接受目錄\n"
        "    --loc 0       停用區域偵測（強制通過）\n"
        "    --loc 1       啟用區域偵測（還原原始檢查）\n"
        "    --lang cjk       修補字型字元集、地區設定及語言代碼；保留 Gameexe/Scene/savedata 路徑\n"
        "    --lang cjk-path  與 cjk 相同，並將路徑改為 GameexeZH.dat、SceneZH.pck 及 savedata_zh\n"
        "    --lang config.json  套用六欄位、可還原的語言設定\n"
        "    --revert          使用內嵌 overlay 還原逐位元組相同的原始執行檔\n"
        "    --allow-partial   即使所選預設設定有部分項目無法使用，仍寫入語言修補\n"
        "\n"
        "Test 模式：\n"
        f"  {p} [--const-profile N] test [--decompile] [--serial] [--report-json FILE] <input_pck|input_dir>\n"
        "    input_dir      測試該目錄下的 .pck 檔案\n"
        "    --decompile    必須指定 --const-profile N；僅反編譯並重建該 profile，檢查 payload 是否相同\n"
        "    --serial       重建期間停用平行編譯\n"
        "    --report-json  將每個檔案的結果及成功的 profiles 寫入 JSON\n"
        "    output         回報 EXACT/PAYLOAD_SAME/SKIP/FAIL 及耗時；--decompile 成功時一律為 PAYLOAD_SAME\n"
        f"    const-profile  內嵌來源測試會依序嘗試 profiles {', '.join(map(str, CONST_PROFILE_IDS))}，然後使用 --charset utf8 --allow-invalid 重試；--decompile 不會使用備援設定\n"
    )
    sys.stdout.write(text)


def _usage_short():
    p = _prog()
    text = (
        f"{p} {package_version() or 'unknown'}\n"
        f"用法：{p} [-h] [-V|--version] [--legacy] [--legacy-full] [--const-profile N] [--string-xor-multiplier N] (-lsp|-c|-x|-a|-d|-k|-e|-m|-g|-s|-v|-p|test) [args]\n"
        f"請使用 '{p} --help' 查看詳細說明。\n"
    )
    sys.stderr.write(text)


def _parse_scene_string_xor_multiplier(value):
    text = value.strip()
    if text.startswith(("0x", "0X")):
        digits = text[2:]
        base = 16
        valid = bool(digits) and all(ch in "0123456789abcdefABCDEF" for ch in digits)
    else:
        digits = text
        base = 10
        valid = bool(digits) and all("0" <= ch <= "9" for ch in digits)
    if not valid:
        raise ValueError(f"invalid --string-xor-multiplier value: {value}")
    multiplier = int(digits, base)
    if not 0 <= multiplier <= 0xFFFF:
        raise ValueError(
            f"invalid --string-xor-multiplier value: {value} (expected 0..0xFFFF)"
        )
    return multiplier


def _consume_global_options(argv):
    legacy = False
    legacy_full = False
    const_profile = None
    string_xor_multiplier = None
    out = []
    i = 0
    while i < len(argv):
        arg = argv[i]
        if arg == "--":
            out.extend(argv[i:])
            break
        if arg == "--legacy":
            legacy = True
            i += 1
            continue
        if arg == "--legacy-full":
            legacy_full = True
            i += 1
            continue
        if arg == "--const-profile":
            if i + 1 >= len(argv):
                raise ValueError("--const-profile requires a value")
            const_profile = argv[i + 1]
            i += 2
            continue
        if arg.startswith("--const-profile="):
            const_profile = arg.split("=", 1)[1]
            i += 1
            continue
        if arg == "--string-xor-multiplier":
            if i + 1 >= len(argv):
                raise ValueError("--string-xor-multiplier requires a value")
            string_xor_multiplier = argv[i + 1]
            i += 2
            continue

        if arg.startswith("--string-xor-multiplier="):
            string_xor_multiplier = arg.split("=", 1)[1]
            i += 1
            continue
        out.append(arg)
        i += 1
    profile = None
    if const_profile is not None:
        value = str(const_profile).strip()
        try:
            profile = int(value, 0)
        except ValueError as exc:
            raise ValueError(f"invalid --const-profile value: {const_profile}") from exc
        if profile not in CONST_PROFILE_IDS:
            raise ValueError(
                f"invalid --const-profile value: {const_profile} (expected {', '.join(map(str, CONST_PROFILE_IDS))})"
            )

    multiplier = 0x7087
    if string_xor_multiplier is not None:
        multiplier = _parse_scene_string_xor_multiplier(string_xor_multiplier)
    return (
        out,
        profile,
        legacy or legacy_full,
        legacy_full,
        multiplier,
        string_xor_multiplier is not None,
    )


def _run_mode(module_name, args, const_profile=None):
    module = import_module(f"siglus_ssu.{module_name}")
    try:
        if module_name == "test":
            rc = module.main(args, const_profile=const_profile)
        else:
            rc = module.main(args)
    except OSError as exc:
        sys.stderr.write(f"{_prog()}: error: {exc}\n")
        return 1
    if rc == 2:
        _usage_short()
    return rc


MODE_MODULES = {
    "-c": "compiler",
    "--compile": "compiler",
    "-x": "extract",
    "--extract": "extract",
    "-a": "analyze",
    "--analyze": "analyze",
    "-d": "db",
    "--db": "db",
    "-k": "koe_collector",
    "--koe": "koe_collector",
    "-e": "exec",
    "--exec": "exec",
    "--execute": "exec",
    "-m": "textmap",
    "--textmap": "textmap",
    "-g": "g00",
    "--g00": "g00",
    "-s": "sound_tool",
    "--sound": "sound_tool",
    "-v": "video_tool",
    "--video": "video_tool",
    "-p": "patch",
    "--patch": "patch",
    "test": "test",
}


def _uses_string_xor_multiplier(mode, args):
    if "--" in args:
        args = args[: args.index("--")]
    options = {str(arg).partition("=")[0] for arg in args}
    match MODE_MODULES.get(mode):
        case "compiler":
            return not options & {"--gei", "--dat-repack"}
        case "extract":
            return bool(options & {"--disam", "--decompile"})
        case "analyze":
            return bool(options & {"--disam", "--payload", "--word"})
        case "koe_collector":
            return "--single" not in options
        case "textmap" | "test":
            return True
        case _:
            return False


def main():
    _runtime._configure_output_streams()
    argv = sys.argv[1:]
    _runtime._LEGACY_COMPILE = False
    _runtime._LEGACY_FULL = False
    _runtime._SCENE_STRING_XOR_MULTIPLIER = 0x7087
    _runtime._SCENE_STRING_XOR_MULTIPLIER_EXPLICIT = False
    try:
        (
            argv,
            const_profile,
            _runtime._LEGACY_COMPILE,
            _runtime._LEGACY_FULL,
            _runtime._SCENE_STRING_XOR_MULTIPLIER,
            string_xor_multiplier_explicit,
        ) = _consume_global_options(argv)
        _runtime._SCENE_STRING_XOR_MULTIPLIER_EXPLICIT = string_xor_multiplier_explicit
    except ValueError as exc:
        sys.stderr.write(f"{_prog()}: {exc}\n")
        return 2
    if argv and argv[0] in ("-V", "--version", "version"):
        _print_version()
        return 0
    if not argv:
        _usage_short()
        return 0
    if argv[0] in ("-h", "--help", "help"):
        _usage()
        return 0
    mode = argv[0]
    mode_args = argv[1:]
    if "--" in mode_args:
        mode_args = mode_args[: mode_args.index("--")]
    if len(argv) > 1 and (
        argv[1] == "help" or any(a in ("-h", "--help") for a in mode_args)
    ):
        _usage()
        return 0
    if (
        string_xor_multiplier_explicit
        and (mode in MODE_MODULES or mode == "-lsp")
        and not _uses_string_xor_multiplier(mode, argv[1:])
    ):
        sys.stderr.write(
            f"{_prog()}: warning: --string-xor-multiplier has no effect for this operation\n"
        )
    try:
        from . import const as C

        C.set_profile(const_profile)
    except FileNotFoundError as exc:
        sys.stderr.write(f"{_prog()}: {exc}\n")
        return 2
    except Exception as exc:
        sys.stderr.write(f"{_prog()}: failed to load const.py: {exc}\n")
        return 1
    if mode in ("-c", "--compile") and const_profile is not None:
        from .common import has_option

        if has_option(argv[1:], "--tmp"):
            sys.stderr.write(
                f"{_prog()}: error: --tmp cannot be used with --const-profile\n"
            )
            return 2
    if mode == "-lsp":
        from . import lsp as lsp_server

        return lsp_server.main(argv[1:])
    module_name = MODE_MODULES.get(mode)
    if module_name is not None:
        return _run_mode(module_name, argv[1:], const_profile=const_profile)
    sys.stderr.write(f"{_prog()}: unknown mode: {mode}\n")
    _usage_short()
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
