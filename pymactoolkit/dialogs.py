from subprocess import Popen, PIPE, call

def say(text: str) -> None:
    """Speaks a text (non-blocking)

    Examples
    --------
    >>> say("Hello John!")

    """
    p = Popen(["say", text], stdin=PIPE, stdout=PIPE, stderr=PIPE)

def system_sound(name: str ='Hero') -> None:
    """Play a system sound (non-blocking).

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

def prompt(message: str, default: str = "") -> str:
    """Prompt the user.

    Examples
    --------
    >>> prompt("Please type HELLO and click OK...")
    'HELLO'
    >>> prompt("Please type whatever and click Cancel...")

    >>> prompt("Please leave the field empty and click OK...")
    ''
    """
    result: str = None
    script = 'set theResponse to display dialog "%s" default answer "%s"' % (message, default)

    p = Popen(["osascript", "-e", script], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output, err = p.communicate()

    if err:
        exception_text = err.decode("utf-8").strip()
        if exception_text.endswith('(-128)'):
            output = None
        else:
            raise Exception(exception_text)
    else:
        output = output.decode("utf-8").strip().split(':')[2]

    return output

def prompt_choice(message: str, choices: list, title: str = "") -> str:
    """Prompting for a Choice from a List.

    Examples
    --------
    >>> prompt_choice("Select DOG and click OK", choices=['DOG', 'BIRD', 'CAT'])
    ['DOG']
    >>> prompt_choice("Select DOG and CAT and click OK", choices=['DOG', 'BIRD', 'CAT'])
    ['DOG', 'CAT']
    >>> prompt_choice("Select whatever and cancel", choices=['DOG', 'BIRD', 'CAT'])

    >>> prompt_choice("Select nothing and click OK", choices=['DOG', 'BIRD', 'CAT'], title="Empty selection")
    []
    """
    list_as_string = ', '.join(['"{}"'.format(choice) for choice in choices])

    script = 'choose from list {%s} with prompt "%s" with title "%s" with multiple selections allowed and empty selection allowed' % (list_as_string, message, title)

    p = Popen(["osascript", "-e", script], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output, err = p.communicate()

    output = output.decode("utf-8").strip().split(', ')

    if output == ['false']:
        output = None
    elif output == ['']:
        output = []

    return output

def notification(title: str, message: str = "", subtitle: str = "", sound_name: str = None) -> None:
    """Display a system notification.

    Note
    ----
    Does not allow links, buttons and callbacks.

    Parameters
    ----------
    sound_name:
        Basso|Blow|Bottle|Frog|Funk|Glass|Hero|Morse|Ping|Pop|Purr|Sosumi|Submarine|Tink

    Examples
    --------
    >>> notification("Hello!")

    >>> notification(title="The title", subtitle="The subtitle", message="The message", sound_name="Pop")

    """
    lines = ['display notification "%s" with title "%s" subtitle "%s"' % (message, title, subtitle)]

    if sound_name:
        lines.append('sound name "%s"' % sound_name)

    script = ' '.join(lines)

    p = Popen(["osascript", "-e", script], stdin=PIPE, stdout=PIPE, stderr=PIPE)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
