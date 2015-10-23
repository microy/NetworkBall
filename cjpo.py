#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Application cliente JPO IUT Auxerre
#
# 
#
# (c)2011eB@uB

# python JPOclnt.py server_address port_number

import socket  # networking module
import sys
from Tkinter import *

# Création de la fenêtre graphique
root = Tk()
sw = root.winfo_screenwidth()
sh = root.winfo_screenheight()
print "screen width  =", sw
print "screen height =", sh 
# set to full screen use this:
root.geometry("%dx%d+0+0" % (sw, sh))

can = Canvas(root, width =sw, height=sh-100, bg="white")
can.pack()
balle = can.create_oval(0,0,0,0, fill='red')
Button(root, text='Quitter', command =root.quit).pack(side =BOTTOM, pady =30)

# create Internet TCP socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = sys.argv[1]  # server address
port = int(sys.argv[2])  # server port

try:
    s.connect((host, port))
except socket.error:
    print "La connexion a échoué."
    sys.exit()    
print "Connexion établie avec le serveur."    

while 1:
    msg = s.recv(256)
    if not msg: break 
    print "trame %s" % msg
    (car,sep,cdr) = msg.partition(".")
    (sx,sep,sy) = car.partition(",")
    x = int(sx)
    y = int(sy)
    print "x=%d et y=%d" % (x,y)
    can.coords(balle, x-30, y-30, x+30, y+30)
    root.update()

#root.mainloop()

print "Connexion interrompue."
s.close()

        
        
