import re
import turtle


# top left corner of the picture
ZERO_LANTITUDE = 49.21863
ZERO_LONGTITUDE = 16.59469
LEFT_TOP_X = -400   # turtle coordinations
LEFT_TOP_Y = 400

# crossroad Domazlicka and Stefanikova
cross_lantitude = 49.215486
cross_longtitude = 16.599775
cross_x = -161
cross_y = 169

# ratios
LANTITUDE_TO_Y = (ZERO_LANTITUDE - cross_lantitude) / (LEFT_TOP_Y - cross_y)
LONGTITUDE_TO_X = (ZERO_LONGTITUDE - cross_longtitude) / (LEFT_TOP_X - cross_x)


def chksum_nmea(sentence):
    cksum = sentence[len(sentence) - 2:]
    chksumdata = re.sub("(\n|\r\n)","", sentence[sentence.find("$")+1:sentence.find("*")])
    csum = 0 
    for c in chksumdata:
       csum ^= ord(c)
    if hex(csum) == hex(int(cksum, 16)):
       return True

    return False


def input_data():
    with open("log.txt", "r") as f:
        list_cor = []
        for index, line in enumerate(f.readlines()):
            if line.startswith("$GPRMC"):
                if chksum_nmea(line.rstrip()):
                    list_all = line.split(",")
                    cor_num = lan_long_num(list_all[3], list_all[5])
                    list_cor.append(cor_num)
                else:
                    print(f"ERROR ON LINE {index}")

            elif line.startswith("$GPRMB"):
                if chksum_nmea(line.rstrip()):
                    pass
                else:
                    print(f"ERROR ON LINE {index}")

            elif line.startswith("$GPGGA"):
                if chksum_nmea(line.rstrip()):
                    list_all = line.split(",")
                    cor_num = lan_long_num(list_all[2], list_all[4])
                    list_cor.append(cor_num)
                else:
                    print(f"ERROR ON LINE {index}")

            elif line.startswith("$GPGSA"):
                if chksum_nmea(line.rstrip()):
                    pass
                else:
                    print(f"ERROR ON LINE {index}")

            elif line.startswith("$PGRME"):
                if chksum_nmea(line.rstrip()):
                    pass   
                else:
                    print(f"ERROR ON LINE {index}") 

            elif line.startswith("$GPGSV"):
                if chksum_nmea(line.rstrip()):
                    pass  
                else:
                    print(f"ERROR ON LINE {index}")
    return list_cor


def lan_long_num(lantitude, longtitude):
    lan_num = float(lantitude[:2]) + float(lantitude[2:])/60
    long_num = float(longtitude[:3]) + float(longtitude[3:])/60

    return lan_num, long_num


def pixels(lantitude, longtitude):
    y = (LANTITUDE_TO_Y * LEFT_TOP_Y + lantitude - ZERO_LANTITUDE)/LANTITUDE_TO_Y
    x = (LONGTITUDE_TO_X * LEFT_TOP_X + longtitude - ZERO_LONGTITUDE)/LONGTITUDE_TO_X

    return x, y


def main():
    tr = turtle.Turtle()
    wn = turtle.Screen()
    wn.bgpic("map.gif")
    tr.speed(0)
    tr.width(2.5)
    cor = input_data()
    tr.penup()
    tr.setpos(pixels(cor[0][0], cor[0][1]))
    tr.pendown()
    for index, i in enumerate(cor[1:]):
        tr.setpos(pixels(i[0], i[1]))
        print(index, pixels(i[0], i[1]))

    wn.mainloop()


if __name__ == "__main__":
    main()

