from threading import Thread
import sys
import json

interfaces = []
endpoints = {}
dialogue_manager = None

def interface(cls):
    interfaces.append(cls)
    return cls

def __init__(self):
    self.endpoints = {}
    self.dialogue_manager = None

def endpoint(command, parameters=None):
    if parameters is None:
        parameters = []
    def decorator(fn):
        def wrapper(*args, **kwargs):
            #try:
            result = fn(dialogue_manager, *args, **kwargs)
            #except KeyError as e:
            #    print(e, flush=True)
            #    result = {"error": "Required parameter " + str(e) + " not found"}
            return result
        endpoints[command] = {"method": wrapper, "parameters": parameters}
        return wrapper
    return decorator

def run(dialogue_manager):
    dialogue_manager = dialogue_manager()

    count = 0
    threads = []

    for i in interfaces:
        threads.append(Thread(target=i.run, args=[i]))
        threads[count].start()
        count = count + 1

def handle(command, data, *args, **kwargs):
    if command in endpoints:
        method = endpoints[command]
        params = method["parameters"]
        keys = list(kwargs.keys())
        keys.sort()

        if len(keys) <= len(params):
            for i in range(len(keys)):
                if params[i] not in data:
                    data[params[i]] = kwargs[keys[i]]

        for p in params:
            if p not in data:
                data[p] = None

        return method["method"](data)
    else:
        return {"Error":"no such endpoint"}
