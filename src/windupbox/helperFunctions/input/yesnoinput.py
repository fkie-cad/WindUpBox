# configure logging
import logging
log = logging.getLogger(__name__)


def yesnoinput(question: str, tries: int = 2) -> int:
    i = 0
    result = -1
    while i < tries:
        answer = input(f'{question} (yes or no)  ')
        if any(answer.lower() == f for f in ["yes", 'y', '1']):
            result = 1
            break
        elif any(answer.lower() == f for f in ['no', 'n', '0']):
            result = 0
            break
        else:
            i += 1
            if i < tries:
                print('Please enter yes or no')
    return result

