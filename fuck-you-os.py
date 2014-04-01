#!/usr/bin/env python
import sys
import os

if len(sys.argv) == 1:
  print "Usage:"
  print "\t%s /path/to/image.pbm"%(os.path.basename(sys.argv[0]))
  sys.exit(1)

image = open(sys.argv[1])
lines = image.readlines()

print """
[BITS 16]
[ORG 0x7C00]
jmp main

TIMES 510 - ($ - $$) db 0
DW 0xAA55

main:
; enter video mode 13h
mov ax,0x13
int 0x10
mov al,0x00

redraw:
mov edi,0x0A0000
inc al
"""

run = 1
runNum = 0
lastChar = "1"
for line in lines[3:]:
  for char in line.strip():
    if char == lastChar:
      run += 1
    else:
      print "not al"
      print "mov ecx,", run
      print "run%d:"%(runNum)
      print "mov [edi],al"
      print "inc edi"
      print "loop run%d"%(runNum)
      print ""
      runNum += 1
      lastChar = char
      run = 1

print "not al"
print "mov ecx,", run
print "run%d:"%(runNum)
print "mov [edi],al"
print "inc edi"
print "loop run%d"%(runNum)
print ""
runNum += 1
lastChar = char
run = 1

print """
mov ax,0
mov ds,ax
mov cx,18
mov bx,[46Ch]
WaitForAnotherChange:
NoChange:
mov ax,[46Ch]
cmp ax, bx
je NoChange
mov bx,ax
loop WaitForAnotherChange

jmp redraw
"""
