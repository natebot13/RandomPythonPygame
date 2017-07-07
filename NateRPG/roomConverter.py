import sys

def header(f):
    line = ""
    while line != "\n":
        line = f.readline()
        if "width" in line and "tile" not in line:
            width = int(line[6:])
        if "height" in line and "tile" not in line:
            height = int(line[7:])
    return width, height, str(width) + "," + str(height) + "\n" + "None,None,None,None" + "\n"

def layer(f):
    tiles = []
    line = f.readline().strip()
    while line != "":
        if line[-1] == ",":
            line = line[:-1]
        tiles += line.split(",")
        line = f.readline().strip()
    return tiles

if __name__ == "__main__":
    stringBuffer = ""
    layers = []
    width, height = 0, 0
    layernames = []
    print("Opening: ", sys.argv[1])
    with open(sys.argv[1]) as f:
        for line in f:
            # print(line)
            if line == "[header]\n":
                print("making header...")
                width, height, stringBuffer = header(f)
                print("Room size:", width, height)
            if line == "[layer]\n":
                l = f.readline()
                layernames.append(l[l.find('=')+1:-1])
                f.readline()
                layers.append(layer(f))
        stringBuffer += ','.join(layernames) + '\n'
    room = zip(*layers)
    x = 1
    for tileArr in room:
        for tile in tileArr:
            stringBuffer += str(tile) + "|"
        stringBuffer = stringBuffer[:-1]
        if x == width:
            x = 1
            stringBuffer += "\n"
        else:
            x += 1
            stringBuffer += ","
    with open(sys.argv[2], 'w') as o:
        o.write(stringBuffer)