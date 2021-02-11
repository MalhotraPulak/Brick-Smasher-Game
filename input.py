import signal
import sys


class AlarmException(Exception):
    pass


def alarmHandler(signum, frame):
    raise AlarmException


def nonBlockingRawInput(timeout):
    signal.signal(signal.SIGALRM, alarmHandler)
    signal.setitimer(signal.ITIMER_REAL, timeout)

    try:
        text = sys.stdin.read(1)
        signal.alarm(0)
        return text
    except AlarmException:
        pass
    signal.signal(signal.SIGALRM, signal.SIG_IGN)
    return ''
