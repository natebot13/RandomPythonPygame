import pygame, pygame.camera, sys, os
import socket, eztext, textrect

from threading import Thread

COMMANDS = """
/help for this help info.
/nick <nickname> to change your nickname.
Buttons:
t: opens chat
a, d: look through history of your sent images
q, e: look through history of other player's sent iamges
space: take a snapshot
f: send snapshot
s: save the entire screen into an image"""

class receiver(Thread):
    def __init__(self, sock):
        Thread.__init__(self)
        self.sock = sock
        self.buffer = ''
        self.fullmessage = False

    def run(self):
        while True:
            newMessage = self.sock.recv(4096)
            if '\r\n' in newMessage:
                self.fullmessage = True
            self.buffer += newMessage

    def getFullMessage(self):
        i = self.buffer.find(' end}')
        if i > 0:
            message = self.buffer[:i + 5]
            self.buffer = self.buffer[i + 5:]
            if ' end}' not in self.buffer:
                self.fullmessage = False
            return message
        return ''

def handle_command(line, sock):
    if line:
        args = line.split(' ')
        if args[0] == '/help':
            return '\n' + COMMANDS
        if args[0] == '/nick':
            sock.send('{' + line[1:] + ' end}\r\n')
            return ''
        else:
            sock.send('{message ' + line + ' end}\r\n')
            return '\nMe: ' + line
    return ''

def log(line, history):
    print line
    return history + line + '\n'

if __name__ == "__main__":

    pygame.init()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if len(sys.argv) == 3:
        sock.connect((sys.argv[1], int(sys.argv[2])))
    else:
        sock.connect(('nathanp.me', 30736))
    print sock.recv(4096)
    for n in range(5):
        sock.send('\r\n')

    SIZE = (960,960)
    WIDTH, HEIGHT = SIZE
    FPS = 30
    CLOCK = pygame.time.Clock()
        
    SCREEN = pygame.display.set_mode(SIZE)
    pygame.display.set_caption('MTGWF Client')

    pygame.camera.init()
    cameras = pygame.camera.list_cameras()
    if len(cameras) > 1:
        print "Looks like you have more than one camera. Which one would you like to use?"
        cam = int(raw_input("Choose from " + str(cameras) + ": "))
    else:
        cam = pygame.camera.Camera(cameras[0])
    cam.start()

    theirhistory = [None]
    myhistory = [None]
    theirID = 0
    myID = 0
    tempimg = None

    r = receiver(sock)
    r.start()

    prompt = eztext.Input(maxlength=36, font=pygame.font.Font(None, 24), color=(255, 255, 255))
    prompt.set_pos(642, HEIGHT - 24)
    promptopen = False
    messagehistory = ''
    chat = pygame.font.Font(None, 24)
    scroll = 0
    lines = 1


    while True:

        if r.fullmessage:
            message = r.getFullMessage()
            message = message[message.find('{'):]
            if message[:6] == '{image':
                between = message.find(' ', 7)
                end = message.find(' ', between + 1)
                width = int(message[7:between])
                height = int(message[between + 1:end])
                image = message[end + 1:-5]
                theirhistory.append(pygame.image.frombuffer(image, (width, height), 'RGB'))
                theirID = len(theirhistory) - 1
            elif message[:9] == '{announce':
                messagehistory += '\n~~~ ' + message[10:-5] + ' ~~~'
            elif message[:8] == '{message':
                messagehistory += '\n' + message[9:-5]
            elif message[:5] == '{info':
                messagehistory += '\n>> ' + message[6:-5] + ' <<'
            elif message[:8] == '{warning':
                messagehistory += '\n!!! ' + message[9:-5] + ' !!!'
        for event in pygame.event.get(pygame.MOUSEBUTTONDOWN):
            if event.button == 4:
                scroll -= chat.get_height()
            if event.button == 5:
                scroll += chat.get_height()
        events = pygame.event.get()
        if promptopen:
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        typed = prompt.get_value()
                        messagehistory += handle_command(typed, sock)
                        prompt.clear_value()
                        promptopen = False
                    if event.key == pygame.K_ESCAPE:
                        promptopen = False
                        prompt.clear_value()
            prompt.update(events)
        else:
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        if theirID > 0:
                            theirID -= 1
                    if event.key == pygame.K_e:
                        if theirID < len(theirhistory) - 1:
                            theirID += 1
                    if event.key == pygame.K_a:
                        if myID > 0:
                            myID -= 1
                    if event.key == pygame.K_d:
                        if myID < len(myhistory) - 1:
                            myID += 1
                    if event.key == pygame.K_s:
                        pygame.image.save(SCREEN, os.path.join('screenshots','board-' + str(theirID) + '-' + str(myID) + '.bmp'))
                    if event.key == pygame.K_SPACE:
                        tempimg = cam.get_image()
                    if event.key == pygame.K_f:
                        if tempimg:
                            m = str(tempimg.get_width()) + ' ' + str(tempimg.get_height())
                            sock.send('{image ' + m + ' '+ pygame.image.tostring(tempimg, 'RGB') + ' end}\r\n')
                            myhistory.append(tempimg)
                            myID = len(myhistory) - 1
                            tempimg = None
                    if event.key == pygame.K_t:
                        promptopen = True

        SCREEN.fill((222, 203, 177))
        if theirhistory[theirID]:
            SCREEN.blit(theirhistory[theirID], (0,0))
        if myhistory[myID]:
            SCREEN.blit(myhistory[myID], (0,480))
        success = False
        pygame.draw.rect(SCREEN, (255,255,255), pygame.Rect(640, 0, 320, 960))
        while not success:
            try:
                chatsurf = textrect.render_textrect(messagehistory, chat, pygame.Rect(0, 0, 320, lines * chat.get_height()), (0,0,0), (255,255,255))
                success = True
            except textrect.TextRectException:
                lines += 1
        SCREEN.blit(chatsurf, (640, 240 - scroll))
        if promptopen:
            pygame.draw.rect(SCREEN, (0,0,0), pygame.Rect(640, HEIGHT - 26, 320, 36))
            prompt.draw(SCREEN)
        if tempimg:
            SCREEN.blit(pygame.transform.scale(tempimg, (320, 240)), (640, 0))
        else:
            pygame.draw.rect(SCREEN, (100,100,100), pygame.Rect(640, 0, 320, 240))

        pygame.display.update()
        CLOCK.tick(FPS)