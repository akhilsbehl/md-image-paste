import os
import vim
from datetime import datetime
import platform


CONFIG = {
    'fig_dir': "./figs",
    'img_suffix': lambda: f'{datetime.now().strftime("%Y-%m-%d-%H-%M-%S")}',
}


def identify_os() -> str:
    plt = platform.platform()
    if plt.startswith("Linux"):
        if 'microsoft' in plt:
            return 'Windows'
        else:
            return 'Linux'
    elif platform == "win32":
        return 'Windows'
    else:
        raise Exception("Unsupported OS: {p}".format(p=platform))


def make_cmds_for_cliboard() -> tuple:

    if OPSYS == 'Linux':
        env = os.getenv('XDG_SESSION_TYPE')
        if env == 'wayland':
            check = 'wl-paste --list-types | grep -q image/png'
            put = 'wl-paste --no-newline --type image/png > {f}.png'
            return (check, put)
        elif env in ('x11', 'tty'):
            check = ('xclip -selection clipboard -t TARGETS -o '
                     '| grep -q image/png')
            put = 'xclip -selection clipboard -t image/png -o > {f}.png'
            return (check, put)
        else:
            raise Exception("Unsupported Linux session type: {t}"
                            .format(t=env))

    elif OPSYS == 'Windows':
        check = 'Get-Clipboard -Format image'
        put = ' '.join(["$content = ", check,
                        ''';$content.Save({f}, 'png')'''])
        check = 'powershell.exe -Command "{c}"'.format(c=check)
        put = 'powershell.exe -Command "{p}"'.format(p=put)
        return (check, put)


OPSYS = identify_os()
CHECK_CLIPBOARD_CMD, SAVE_CLIPBOARD_CMD = make_cmds_for_cliboard()


def paste_image(with_alttext: str = '') -> None:

    try:

        if not is_clibboard_image():
            raise Exception('There is no image in the clipboard')
            return

        image_path = make_image_path(from_alttext=with_alttext)
        save_clipboard_image_content(to_path=image_path)
        write_image_anchor(
            make_image_md_anchor(
                with_alttext=with_alttext, with_path=image_path))

    except Exception as e:
        raise Exception(e)


def is_clibboard_image() -> bool:
    return bool(os.popen(CHECK_CLIPBOARD_CMD).read())


def make_image_path(from_alttext) -> str:
    from_alttext = 'fig' if not from_alttext else from_alttext
    return f'{CONFIG["fig_dir"]}/{from_alttext}-{CONFIG["img_suffix"]()}.png'


def save_clipboard_image_content(to_path: str) -> None:
    dirname = os.path.dirname(to_path)
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    os.system(SAVE_CLIPBOARD_CMD.format(f=to_path))


def write_image_anchor(image_anchor: str) -> None:
    row, _ = vim.current.window.cursor
    buf = vim.current.buffer
    buf.append(image_anchor, row)


def make_image_md_anchor(with_alttext: str, with_path: str) -> str:
    return f'![{with_alttext}]({with_path})'
