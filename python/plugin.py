import os
import vim
from datetime import datetime
import platform


def identify_os() -> str:
    plt = platform.platform()
    if plt.startswith("Linux"):
        if 'microsoft' in plt:
            return 'WSL'
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
            put = 'wl-paste --no-newline --type image/png > {f}'
            return (check, put)
        elif env in ('x11', 'tty'):
            check = ('xclip -selection clipboard -t TARGETS -o '
                     '| grep -q image/png')
            put = 'xclip -selection clipboard -t image/png -o > {f}'
        else:
            raise Exception("Unsupported Linux session type: {t}"
                            .format(t=env))

    elif OPSYS in ('Windows', 'WSL'):
        check = 'powershell.exe -Command "Get-Clipboard -Format Image"'
        put = '''$img = Get-Clipboard -Format Image; $img.Save("{f}")'''
        put = f"powershell.exe -Command '{put}'"

    else:
        raise Exception("Unsupported OS: {o}".format(o=OPSYS))

    return (check, put)


OPSYS = identify_os()
CHECK_CLIPBOARD_CMD, SAVE_CLIPBOARD_CMD = make_cmds_for_cliboard()


def paste_image(with_alttext: str = '') -> None:

    if not is_clibboard_image():
        print('There is no image in the clipboard')
        return

    image_name = make_image_name(from_alttext=with_alttext)
    save_clipboard_image_content(with_name=image_name)
    write_image_anchor(f'![{with_alttext}](./figs/{image_name})')


def is_clibboard_image() -> bool:
    return bool(os.popen(CHECK_CLIPBOARD_CMD).read())


def make_image_name(from_alttext) -> str:
    alttext = 'fig' if not from_alttext else from_alttext.replace(' ', '-')
    suffix = f'{datetime.now().strftime("%Y-%m-%d-%H-%M-%S")}'
    return (f'{alttext}-{suffix}.png')


def save_clipboard_image_content(with_name: str) -> None:

    dirname, slash = f'{os.path.dirname(vim.current.buffer.name)}/figs', '/'
    if not os.path.exists(dirname):
        os.makedirs(dirname, exist_ok=True)

    # Need path conversion between WSL & Windows for Powershell
    if OPSYS == 'WSL':
        dirname, slash = os.popen(f'wslpath -w {dirname}').read().strip(), '\\'

    print(SAVE_CLIPBOARD_CMD.format(f=f'{dirname}{slash}{with_name}'))
    os.system(SAVE_CLIPBOARD_CMD.format(f=f'{dirname}{slash}{with_name}'))


def write_image_anchor(image_anchor: str) -> None:
    row, _ = vim.current.window.cursor
    buf = vim.current.buffer
    buf.append(image_anchor, row)
