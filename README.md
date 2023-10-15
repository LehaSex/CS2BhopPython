# CS2BhopPython

## 💬 What is this?
This is a program for bhop in CS 2. It automatically emulates the scrolling of the mouse wheel, thereby helping in bhop. To launch executable doesn't need Python.

## 🛠️ Features
- AutoPistol
- Bhop

## 🕹️ How To Use
- To start using, run `.exe` file. 
- Then place the downloaded folder `/temp` in the folder with the configs of CS 2, which is located at `Counter-Strike Global Offensive\game\csgo\cfg\`
- The file structure should look like this:
```
.
└── C/
    └── Program Files (x86)/
        └── Steam/
            └── steamapps/
                └── common/
                    └── Counter-Strike Global Offensive/
                        └── game/
                            └── csgo/
                                └── cfg/
                                    └── temp/
                                        ├── jmp_standart.cfg
                                        ├── jmp_bhop.cfg
                                        ├── atk_standart.cfg
                                        └── atk_auto.cfg
```
- Then, run CS 2 and enter the following commands in the developer console:
```
bind KP_DEL "exec ./temp/atk_auto"
bind KP_0 "exec ./temp/jmp_bhop"
```

- To activate/deactivate bhop, press `0` on the numeric keypad.
- To activate/deactivate autopistol, press `DEL` on the numeric keypad.
  - Activation/Deactivation information will be displayed in the developer console.

- You can close the program by pressing `F1` key.

If the program is closed, it is necessary to deactivate all functions, otherwise the attack and/or jump will not work for you.

You can change the binds to your own in the `*_standard.cfg` files or adapt the program to your needs.

## 💀 VAC and other AC
This program does `NOT` read/modify/write memory to cs2.exe . It only simulates the scrolling of the mouse wheel, the binds to which are exposed in the files in the `/temp` folder. This means that the VAC should not detect this program. But in any case, use it at your own risk. I haven't tested this on other anti-cheats like Faceit, EAC, etc. Most likely you will be banned by these anti-cheats. I am not responsible for your banned accounts.
