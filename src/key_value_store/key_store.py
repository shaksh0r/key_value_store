

import cmd
from key_value_store.store import Store
from .tasks import return_statement,scheduled_set
from datetime import datetime,time, timedelta
import threading
from queue import PriorityQueue
import itertools

cond = threading.Condition()
counter = itertools.count()

def background_worker(task_list:PriorityQueue,store:Store,stop_event): 
    while True:    
        while not task_list.empty():
            top_task = task_list.queue[0]
            top_task_schedule:datetime = top_task[0]
            time_diff = (top_task_schedule-datetime.now()).total_seconds()
            if time_diff < 1:
                urgent_task = task_list.get()
                operation = urgent_task[2][0]
                key = urgent_task[2][1]
                value = urgent_task[2][2]
                if operation == 'set':
                    store.set(key,value)
                elif operation == 'delete':
                    store.delete(key)
            else:
                with cond:
                    cond.wait(timeout=time_diff)

        if task_list.empty():
            with cond:
                cond.wait()





class Shell(cmd.Cmd):
    intro = 'Welcome to the shell'
    prompt = '(store)'

    def __init__(self):
        super().__init__()
        self.shell_store = Store()
        self.task_list = PriorityQueue()
        self.stop_event = threading.Event()
        self.thread = threading.Thread(target=background_worker,args=(self.task_list,self.shell_store,self.stop_event))
        self.thread.start()

    def emptyline(self):
        """Override to prevent repeating the last command on blank lines."""
        pass

    def parse(self,arg):
        return tuple(arg.split())

    def parseline(self,line):
        if line.startswith('scheduled '):
            line = line.replace(' ','_',1)
        return super().parseline(line)

    def do_print(self,arg):
        print("args:",self.parse(arg)[0])
        print(self.parse(arg))

    def do_get(self,arg):
        self.parsed_arg = self.parse(arg)

        key = self.parsed_arg[0]
        print(self.shell_store.get(key))
    
    def do_set(self,arg):
        self.parsed_arg = self.parse(arg)
        key = self.parsed_arg[0]
        value = self.parsed_arg[1]

        print(self.shell_store.set(key,value))
    
    
    def do_delete(self,arg):
        self.parsed_arg = self.parse(arg)
        key = self.parsed_arg[0]

        print(self.shell_store.delete(key))

    def do_scheduled_set(self,arg):
        self.parsed_arg = self.parse(arg)
        key = self.parsed_arg[0]
        value = self.parsed_arg[1]
        delay = int(self.parsed_arg[2])
        if delay < 0:
            print("Can't Schedule for that delay")
        else:
            operation_time = datetime.now() + timedelta(seconds=delay)
            scheduled_tuple = ("set",key,value)
            self.task_list.put((operation_time,next(counter),scheduled_tuple))
            with cond:
                cond.notify()
            print("Done")

    def do_scheduled_delete(self,arg):
        self.parsed_arg = self.parse(arg)
        key = self.parsed_arg[0]
        delay = int(self.parsed_arg[1])

        if delay < 0:
            print("Can't Schedule for that delay")
        else:
            operation_time = datetime.now() + timedelta(seconds = delay)
            scheduled_tuple = ("delete",key,"")
            self.task_list.put((operation_time,next(counter),scheduled_tuple))
            with cond:
                cond.notify()

        print("Done")

    def do_quit(self,arg):
        self.stop_event.set()
        return True



if __name__ == "__main__":
    Shell().cmdloop()
