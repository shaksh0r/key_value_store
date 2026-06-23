import cmd


def print_back(statement):
    print(statement)



class Shell(cmd.Cmd):
    intro = 'Welcome to the shell'
    prompt = '(shell)'

    def do_print(self,arg):
        print("args:",parse(arg)[0])
        print(parse(arg))

    def do_get(self,arg):
        parsed_arg = parse(arg)

        key = parsed_arg[0]
        


def parse(arg):
    return tuple(arg.split())


if __name__ == '__main__':
    Shell().cmdloop()