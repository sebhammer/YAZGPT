


logfile = None;

def log(arg):
    if logfile:
        with open(logfile, 'a') as f:
            f.write(arg + '\n')
