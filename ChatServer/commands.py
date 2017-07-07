def handle(line, session):
    args = line.split(' ')
    command = args[0]
    args = args[1:-1]
    if command == '{nick':
        if args:
            nick(session, args)
        else:
            session.push('{warning Wrong number of arguments... end}\r\n')
        return True
    if command == '{message':
        session.server.broadcast(command + ' ' + session.player + ': ' + ' '.join(args) + ' end}\r\n', session)
        return True
    return False

def displayhelp(session):
    session.push(COMMANDS)

def nick(session, args):
    names = [s.player for s in session.server.sessions]
    if args[0] not in names:
        print 'changing name...'
        session.server.broadcast('{announce ' + session.player + ' is now nicknamed: ' + args[0] + ' end}\r\n', session)
        session.player = args[0]
        session.push('{info Your new nickname is: ' + args[0] + ' end}\r\n')
    else:
        session.push('{warning Sorry, ' + args[0] + ' is taken. end}\r\n')