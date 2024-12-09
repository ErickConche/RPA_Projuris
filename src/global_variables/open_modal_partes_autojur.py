opened_modal = False


def get_opened_modal():
    global opened_modal
    return opened_modal


def update_opened_modal(status: bool):
    global opened_modal
    opened_modal = status
