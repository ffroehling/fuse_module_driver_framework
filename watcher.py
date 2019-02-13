import inotify.adapters
import inotify.constants as const
import random
import time
from thread import WorkerThread

#two small constants
READ = 0
WRITE = 1
BOTH = 2

#list of current watches
watches = []


#init the variable
i = inotify.adapters.Inotify()

def get_id():
    result = random.randint(1,100000)
    for watch in watches:
        if watch['id'] == result:
            return get_id()

    return result

#adds a read listener and returns a random but unique identifier
def add_read_listener(path, on_read):
    watches.append(dict(path=path,mode=READ,on_read=on_read, id=get_id()))
    i.add_watch(path)
    print("added watch")
    pass

#adds a write listener and returns a random but unique identifier
def add_write_listener(path, on_write):
    watches.append(dict(path=path,mode=WRITE,on_read=on_read, id=get_id()))

#adds a read_write listener and returns a random but unique identifier
def add_read_write_listener(path, on_read, on_write):
    watches.append(dict(path=path,mode=BOTH,on_read=on_read,on_write=on_write, id=get_id()))
    pass

#unwatches
def remove_watch(watch):
    i.remove_watch(watch['path'])
    watches.remove(watch)

def remove_watch_by_id(identifier):
    for watch in watches:
        if watch['id'] == identifier:
            remove_watch(watch)


def get_watch_for_path(path):
    for watch in watches:
        if watch['path'] == path:
            return watch
    return None

#perfoms loop to listen in seperate thread
#thread needs to be killed on program close
def listen():
    events = i.event_gen(yield_nones=False, timeout_s=1)

    for event in events:
        (_, type_names, path, filename) = event
        watch = get_watch_for_path(path)

        if not watch:
            continue

        #get_proper action
        if watch['mode'] == READ and 'IN_ACCESS' in type_names:
            watch['on_read']()
        elif watch['mode'] == WRITE and 'IN_MODIFY' in type_names:
            watch['on_write']()
        elif watch['mode'] == BOTH:
            if 'IN_ACCESS' in type_names:
                watch['on_read']()
            elif 'IN_MODIFY' in type_names:
                watch['on_write']()

def start_listening():
    worker.start()

def stop_listening():
    #unregister everything
    for watch in watches:
        remove_watch(watch)

    worker.stop()

#thread module
worker = WorkerThread(method=listen, delay=1)
