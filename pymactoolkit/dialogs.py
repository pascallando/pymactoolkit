from subprocess import Popen, PIPE, call

def system_sound(name: str ='Hero') -> None:
    """Play a system sound (not blocking).

    Parameters
    ----------
    name:
        Basso|Blow|Bottle|Frog|Funk|Glass|Hero|Morse|Ping|Pop|Purr|Sosumi|Submarine|Tink

    Examples
    --------
    >>> system_sound("Bottle")

    >>> system_sound("Blow")

    """
    p = Popen(["afplay", "/System/Library/Sounds/{}.aiff".format(name)], stdin=PIPE, stdout=PIPE, stderr=PIPE)

def alert(text: str, message: str = "", alert_type: str = "informational", buttons: dict = None) -> str:
    """Display an alert.

    Parameters
    ----------
    text:
        The highlighted text
    message:
        A non-bold text message displayed bellow `text`
    alert_type:
        informational|critical|warning
    buttons:
        A dict with `default` and `cancel` keys

    Examples
    --------
    >>> alert("Please click OK")
    'OK'
    >>> alert(text="This is a title", message="Please click OK...", alert_type="critical")
    'OK'
    >>> alert("Please click Delete", buttons={'default': "Delete", 'cancel': "Abort"})
    'Delete'
    """
    result: str = None

    lines = ['display alert "{}" message "{}"'.format(text, message)]

    if alert_type:
        lines.append('as %s' % alert_type)
    if buttons:
        lines.append('buttons {"%s", "%s"} default button "%s" cancel button "%s"' % (buttons['default'], buttons['cancel'], buttons['default'], buttons['cancel']))


    script = ' '.join(lines)

    p = Popen(["osascript", "-e", script], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output, err = p.communicate()

    if err:
        exception_text = err.decode("utf-8").strip()
        if exception_text.endswith('(-128)'):
            output = "Cancel"
        else:
            raise Exception(exception_text)
    else:
        output = output.decode("utf-8").strip().split(':')[1]

    return output


if __name__ == "__main__":
    import doctest
    doctest.testmod()
