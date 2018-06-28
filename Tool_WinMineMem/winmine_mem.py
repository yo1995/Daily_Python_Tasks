# -*- coding:utf-8 -*-
#! python3

__author__ = 'cht'
'''
读内存扫雷测试
'''

import win32gui
import win32process
import win32con
import win32api
from ctypes import *
import time


if __name__ == "__main__":
    # maximum rows and columns to contain your board.
    # high level should be 30*16
    MAX_ROWS = 30
    MAX_COLUMNS = 30
    # coordinates for the board and grid in the window.
    MINE_BEGIN_X = 0x0C
    MINE_BEGIN_Y = 0x37
    MINE_GRID_WIDTH = 0x10
    MINE_GRID_HEIGHT = 0x10
    # border, no mine, with mine
    MINE_BORDER = 0x10
    MINE_SAFE = 0x0F
    MINE_DANGER = 0x8F
    # address for board of Winmine.exe of winxp
    BOARD_ADDRESS = 0x1005340

    # to obtain the process id we need to get the hwnd first. just as 2k11
    # https://docs.python.org/3/library/ctypes.html
    class BoardArray(Structure):
        _fields_ = [("board", (c_byte * (MAX_COLUMNS + 2)) * (MAX_ROWS + 2))]
    Array = BoardArray()
    hWnd = win32gui.FindWindow("Minesweeper", "Minesweeper")
    if not hWnd:
        win32api.MessageBox(0, "No Window found. Please run minesweeper first.", "Error!", win32con.MB_ICONERROR)
        exit(0)
    threadID, processID = win32process.GetWindowThreadProcessId(hWnd)
    libload = windll.LoadLibrary("kernel32.dll")
    hProc = libload.OpenProcess(win32con.PROCESS_VM_READ, 0, processID)

    # read mine data from board memory region
    libload.ReadProcessMemory(hProc, BOARD_ADDRESS, byref(Array.board), BoardArray.board.size, 0)

    # read the actual size of board
    rows = 0
    columns = -2  # to exclude the border
    for i in range(0, MAX_COLUMNS + 2):
        if MINE_BORDER == Array.board[0][i]:
            columns += 1
        else:
            break

    for i in range(1, MAX_ROWS + 1):
        if MINE_BORDER == Array.board[i][0]:
            rows += 1
        else:
            break

    # print('本局有' + str(ctrlData.rows - 1) + '行，' + str(ctrlData.columns) + '列。')
    # we can either use numpy to get all the coordinates at once or just iterate over the region
    # iteration version
    for i in range(0, rows):
        for j in range(0, columns):
            if MINE_SAFE == Array.board[i + 1][j + 1]:
                time.sleep(0.03)  # so you can see the process ;-)
                w = int(MINE_BEGIN_X + MINE_GRID_WIDTH * j + MINE_GRID_WIDTH / 2)
                h = int(MINE_BEGIN_Y + MINE_GRID_HEIGHT * i + MINE_GRID_HEIGHT / 2)
                # send msg of mouse
                win32api.SendMessage(hWnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, win32api.MAKELONG(w, h))
                win32api.SendMessage(hWnd, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, win32api.MAKELONG(w, h))

    win32api.MessageBox(0, "Finished.", "Yoho", win32con.MB_ICONINFORMATION)
