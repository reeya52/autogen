import re


def get_function_parameters(path):
    ''' get parameters for function definition'''
    sub_path = re.split(r"\/", path)
    arg_str = ''
    object_ids = [i for j, i in enumerate(sub_path) if j % 2 != 0]
    for obj in object_ids:
        if '{' not in obj:
            return path
    if(len(object_ids) >= 1):
        arg_str = object_ids[0].replace('{', '').replace('}', '')
        for i in range(len(object_ids)-1):
                res = object_ids[i+1].replace('{', ', ').replace('}', '')
                arg_str += res
        return arg_str
    else:
        return arg_str

def get_path_parameters(path):
    ''' get path specific parameters to create a either collection path or instance path'''
    sub_path = re.split(r"\/", path)
    object_ids = [i for j, i in enumerate(sub_path) if j % 2 != 0]
    if(len(object_ids) >= 1):
        num = 0
        for res in object_ids:
            if (path.find(res)!=1):
                path = path.replace(res, '{{{0}}}'.format(num))
                num = num +1
        return path
    else:
        return path

def get_wildcard_parameters(arg_str):
    arguments = re.split(', ', arg_str)
    wc_str = ''
    for i in range(len(arguments)):
        wc_str = wc_str + "'{0}':{0}, ".format(arguments[i])
    return wc_str