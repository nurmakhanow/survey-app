from importlib import import_module


def my_import(name):
    """
    This function is for importing python object (class, function or whatever) by string, BUT NOT A PACKAGE
    :param name: string path to python object
    :return: wanted object
    """
    p, m = name.rsplit('.', 1)
    module = import_module(p)
    obj = getattr(module, m)
    return obj
