

import cmd
from key_value_store.store import Store
from .tasks import return_statement,scheduled_set
from datetime import datetime,time, timedelta
import threading




def background_worker(task_list:list[tuple[datetime,str,str,str]],store:Store,stop_event):
    while not stop_event.is_set():
        for task in task_list[:]:
            current_time = datetime.now()
            task_time = task[0]
            time_diff = (task_time - current_time).total_seconds()

            if time_diff <= 1:
                operation = task[1]
                key = task[2]
                value = task[3]
                if operation == 'set':
                    store.set(key,value)
                elif operation == 'delete':
                    store.delete(key)

                try:
                    task_list.remove(task)
                except ValueError as e:
                    raise
                    
        
        stop_event.wait(1)




class Shell(cmd.Cmd):
    intro = 'Welcome to the shell'
    prompt = '(store)'

    def __init__(self):
        super().__init__()
        self.shell_store = Store()
        self.task_list = []
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
            scheduled_tuple = (operation_time,"set",key,value)
            self.task_list.append(scheduled_tuple)

            print("Done")

        #TODO: need to implement Internal Scheduler Thread

    def do_scheduled_delete(self,arg):
        self.parsed_arg = self.parse(arg)
        key = self.parsed_arg[0]
        delay = int(self.parsed_arg[1])

        if delay < 0:
            print("Can't Schedule for that delay")
        else:
            operation_time = datetime.now() + timedelta(seconds = delay)
            scheduled_tuple = (operation_time,"delete",key,"")
            self.task_list.append(scheduled_tuple)

        print("Done")

    def do_quit(self,arg):
        self.stop_event.set()
        return True



if __name__ == "__main__":
    Shell().cmdloop()
