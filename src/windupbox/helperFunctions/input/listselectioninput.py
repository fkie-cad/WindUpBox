# external imports
import math

#configure logging
import logging
log = logging.getLogger(__name__)


def listselectinput(question: str, selection_list: list, tries: int or None = 2):
    i = 0
    result = -1
    list_len = len(selection_list)
    if not tries:
        tries = math.inf
    while i < tries:
        print(f'{question}')
        for index, value in enumerate(selection_list):
            print(f'{index + 1}.) {value}')
        answer = input('Please enter your choice (by entering the number):  ')
        if any(int(answer) == f+1 for f in range(0, list_len)):
            result = int(answer)-1
            break
        else:
            i += 1
            if i < tries:
                print(f'Please enter a number between 1 and {list_len}')
    if result == -1:
        return None
    print('\n')
    return selection_list[result]


# def listoftuplesselectinput(selection_list: list, request: str, index_display_value=0, index_ret_value=1):
#     for index, value in enumerate(selection_list):
#         print(f'{index + 1}.) {value[index_display_value]}')
#     chosen_input = len(selection_list)
#     while chosen_input >= len(selection_list):
#         chosen_input = int(input(f'{request} : ')) - 1
#     return selection_list[chosen_input][index_ret_value]