

import cmd
from key_value_store.store import Store




class Shell(cmd.Cmd):
    intro = 'Welcome to the shell'
    prompt = '(store)'
    shell_store = Store()

    def parse(self,arg):
        return tuple(arg.split())

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
    def do_quit(self,arg):
        return True



