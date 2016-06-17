

def flash(msg='An error occurred', t='danger', f=None):
    """
    Adds a flash message to the provided flash array
    :param t: type of flash message. Corresponds to Bootstrap's alert types
    :param msg: message to display.
    :param f: array of flash messages to append the provided flash to
    :return: array of flash messages
    """
    if f is None:
        return [{'type': t, 'message': msg}]
    f.append({'type': t, 'message': msg})
    return f
