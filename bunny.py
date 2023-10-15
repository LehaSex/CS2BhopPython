import os
import ctypes as ct
import ctypes.wintypes as wt
import win32con as wc
import win32api as wa
import win32process as wp
import win32gui as wg
import asyncio
from art import *

winmm       = ct.WinDLL('winmm')
kernel32    = ct.WinDLL('kernel32')
STD_OUTPUT_HANDLE = -11

PUL = ct.POINTER(ct.c_ulong)
class KeyBdInput(ct.Structure):
    _fields_ = [("wVk", ct.c_ushort),
                ("wScan", ct.c_ushort),
                ("dwFlags", ct.c_ulong),
                ("time", ct.c_ulong),
                ("dwExtraInfo", PUL)]

class HardwareInput(ct.Structure):
    _fields_ = [("uMsg", ct.c_ulong),
                ("wParamL", ct.c_short),
                ("wParamH", ct.c_ushort)]

class MouseInput(ct.Structure):
    _fields_ = [("dx", ct.c_long),
                ("dy", ct.c_long),
                ("mouseData", ct.c_ulong),
                ("dwFlags", ct.c_ulong),
                ("time",ct.c_ulong),
                ("dwExtraInfo", PUL)]

class Input_I(ct.Union):
    _fields_ = [("ki", KeyBdInput),
                 ("mi", MouseInput),
                 ("hi", HardwareInput)]

class Input(ct.Structure):
    _fields_ = [("type", ct.c_ulong),
                ("ii", Input_I)]

class c_time_tracker:
    __starting_time        = wt.LARGE_INTEGER()
    __ending_time          = wt.LARGE_INTEGER()
    __elapsed_microseconds = wt.LARGE_INTEGER()
    __frequency            = wt.LARGE_INTEGER()

    def __init__(self):
        self.refresh()
        

    def refresh(self):
        kernel32.QueryPerformanceFrequency(ct.byref(self.__frequency))
        kernel32.QueryPerformanceCounter(ct.byref(self.__starting_time))

    def elapsed_time(self):
        kernel32.QueryPerformanceCounter(ct.byref(self.__ending_time))
        kernel32.QueryPerformanceFrequency(ct.byref(self.__frequency))
        self.__elapsed_microseconds.value = self.__ending_time.value - self.__starting_time.value
        return self.__elapsed_microseconds.value * 1000 / self.__frequency.value
    
def send_left_control(key_down:bool):
    ii_ = Input_I()
    ii_.ki.dwFlags = wc.KEYEVENTF_SCANCODE if key_down else wc.KEYEVENTF_KEYUP | wc.KEYEVENTF_SCANCODE
    ii_.ki.wScan = wa.MapVirtualKey(wc.VK_LCONTROL, 0)
    x = Input( ct.c_ulong(1), ii_ )
    ct.windll.user32.SendInput(1, ct.pointer(x), ct.sizeof(x))

def release_space():
    ii_ = Input_I()
    ii_.ki.dwFlags = wc.KEYEVENTF_KEYUP | wc.KEYEVENTF_SCANCODE
    ii_.ki.wScan = wa.MapVirtualKey(wc.VK_SPACE, 0)
    x = Input( ct.c_ulong(1), ii_ )
    ct.windll.user32.SendInput(1, ct.pointer(x), ct.sizeof(x))

async def custom_sleep(ms):
    excess = c_time_tracker()
    expected_time:float = 2.0
    while excess.elapsed_time() < ms - expected_time:
        await asyncio.sleep(0.001)
    while excess.elapsed_time() < ms:
        await asyncio.sleep(0)
        
async def bhop():
    while ( not (wa.GetAsyncKeyState(wc.VK_F1) & 0x8000) ):
        if wg.GetWindowText(wg.GetForegroundWindow()) == "Counter-Strike 2":
            if wa.GetAsyncKeyState(wc.VK_SPACE) & 0x8000:
                while (wa.GetAsyncKeyState(wc.VK_SPACE) & 0x8000):
                    wa.mouse_event(wc.MOUSEEVENTF_WHEEL, 0, 0, -wc.WHEEL_DELTA, 0)
                    await custom_sleep( TICK_64_MS * 2.0 )
            else:
                await asyncio.sleep(0.001)
    winmm.timeEndPeriod(1)
    return os.EX_OK

async def autofire():
    while ( not (wa.GetAsyncKeyState(wc.VK_F1) & 0x8000) ):
        if wg.GetWindowText(wg.GetForegroundWindow()) == "Counter-Strike 2":
            if wa.GetAsyncKeyState(0x01) & 0x8000:
                while (wa.GetAsyncKeyState(0x01) & 0x8000): 
                    wa.mouse_event(wc.MOUSEEVENTF_WHEEL, 0, 0, wc.WHEEL_DELTA, 0)
                    
                    await custom_sleep( TICK_64_MS * 2.0 )
                    
            else:
                await asyncio.sleep(0.001)
    winmm.timeEndPeriod(1)
    return os.EX_OK

def PrintInColor(text, color):
    # The color is an int and text is simply passed through
    hout = kernel32.GetStdHandle(ct.c_void_p(STD_OUTPUT_HANDLE))
    x = kernel32.SetConsoleTextAttribute(hout, color)
    print(text, end='', flush=True)

async def main():
    await asyncio.gather(bhop(), autofire())

if __name__ == "__main__":
    PrintInColor(text2art("BunnyHop"), 0x5)
    tprint("& AutoFire")
    # setconsole text attribute
    PrintInColor("Version 1.0", 0xE)
    PrintInColor("\nMade by ", 0xE)
    PrintInColor("LehaSex", 0x0060 )
    PrintInColor("\n\nPress F1 to exit", 0x2)
    winmm.timeBeginPeriod(1)
    wp.SetPriorityClass(wp.GetCurrentProcess(), wp.REALTIME_PRIORITY_CLASS)
    ct.windll.kernel32.SetConsoleTitleW("BunnyHop & AutoFire by LehaSex")
    # reset style
    PrintInColor("", 0xF)
    print("\n\nLaunched successfully!!!")
    TICK_64_MS:float = 15.6
    asyncio.run(main())
    