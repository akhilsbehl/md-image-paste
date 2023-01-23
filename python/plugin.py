from datetime import datetime


CONFIG = {
    fig_dir = "./figs",
    fig_dir_txt = "figs",
    image_suffix = lambda: f'-{datetime.now().strftime("%Y-%m-%d-%H-%M-%S")}',
    affix = "%s",
}


GET_CLIPBOARD_CMD = make_cmd_to_get_cliboard()
PUT_CLIPBOARD_CMD = make_cmd_to_put_cliboard()


def make_cmd_to_get_cliboard():
    pass


def make_cmd_to_put_cliboard():
    pass


def paste_image(alttext):

    content = get_clipboard_content()

    if not is_image(content):
        vim.notify('There is no image in the clipboard', vim.log.levels.ERROR)
        return

    image_path = make_image_path()
    image_anchor = make_image_md_anchor(image_path, alttext)

    try:
        save_image(content, image_path)
        write_image_anchor(image_anchor)
    except Exception as e:
        vim.notify(str(e), vim.log.levels.ERROR)



def get_clipboard_content():
    pass


def make_image_path():
    pass


def make_image_md_anchor(image_path, alttext):
    pass


def save_image(content, image_path):
    pass


def write_image_anchor(image_anchor):
    pass
