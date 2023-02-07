import os
import datetime


def logger(path):

    def __logger(old_function):
        def new_function(*args, **kwargs):
            start = datetime.datetime.now()
            name = old_function.__name__
            arg = f'{args}, {kwargs}'
            result = old_function(*args, **kwargs)
            with open(path, 'a', encoding='utf-8') as file:
                res = f'{start}\n{name}\n{arg}\n{result}'
                file.writelines(res)
            return result
        return new_function
    return __logger