# Network Attached Mouse

A serial mouse driver capable of connecting to a serial mouse over the network via a terminal server
(and I guess a local COM port too, but where's the fun in that?).

**TL;DR**: A python script to connect to a network port (or COM port) and let you use a serial mouse on Windows[^1].

```cmd
python main.py --microsoft --ip=192.168.1.2 --port=3008
# or
NetMouse.exe --microsoft --ip=192.168.1.2 --port=3008
```
![Serial mouse attached to a terminal server](https://my.computers.pictures/file/genEricComputers/NetworkAttachedMouse/P_20260621_183113.jpg)

## Backstory

At a swap meet, I'd picked up a terminal server, specifically a [Lantronix ETS8P](https://www.lantronix.com/wp-content/uploads/pdf/ets_ref.pdf).
A terminal server is a device with multiple serial/RS-232 ports that lets you access those ports over the network.

You configure the baud rate and other serial settings on the device - via telnet or by accessing it over a serial console/terminal - and then
you can access each of its serial ports through a network port.  In my case ports 3001 - 3008.

Anyway, I was using to access my home server by its serial console when I was curious about something.  Does it only work with serial consoles?
Or could I connect _any_ serial device and access that over the network?

## Initial tests

I wanted to try this, but I wasn't really sure where to start.  First, I'd need to find/create a serial mouse driver, I guess...

I didn't really want to create my own driver, as I'm sure _someone_ must've created this already.  After plenty of searching, I found the
`inputattach` command for Linux (part of the [`linuxconsoletools` package on Fedora](https://packages.fedoraproject.org/pkgs/linuxconsoletools/linuxconsoletools/)).

Let's see if my mouse even works at all, so I used my trusty USB to serial adapter and ran
```bash
sudo inputattach --microsoft /dev/ttyUSB0
```
and it just worked!  I'm using a KeyTronic branded 2-button mouse, but lots of mice used the "Microsoft Serial Mouse" command set.

Ok, this bodes well for it working over the terminal server, so let's configure that.  According to [`inputattach.c`](https://sourceforge.net/p/linuxconsole/code/ci/master/tree/utils/inputattach.c#l822),
the mouse communicates at 1200 baud, 7N1.  I configured port 8 on my terminal server, and connected the mouse[^2] and a null-modem adapter.
I then set the termianl server's IP and used one of my favorite linux tools, `socat`.
```bash
socat -d -d pty,rawer,echo=0,link=/tmp/sermouse tcp:192.168.1.2:8008
sudo inputattach --microsoft /tmp/sermouse
```

This got me... a permission error!  Not sure why, but `inputattach` can't attach to symlinks - which is what `/tmp/sermouse` is.
But, if you look at the symlink it goes to `/dev/pts/2` and using that...
```bash
socat -d -d pty,rawer,echo=0,link=/tmp/sermouse tcp:192.168.1.2:3008
sudo inputattach --microsoft /dev/pts/2
```
worked!  Now I could move my serial mouse, connected to the terminal server, wait a bit and see the cursor move on my screen!

## What about Windows?

`inputattach` is very much a Linux tool, so what about Windows.  Well, it turns out that Windows 11 _still_ has a serial mouse driver built-in!
You can enable it like this:
```cmd
sc config sermouse start=demand
```
after running this, nothing seems to have happened.  Even with my USB to serial adapter and mouse connected.

After a reboot, however... the mouse just started working!  Device manager even showed "Microsoft Serial Mouse".
Cool, that's awesome, now to connect to a network port.

I think there is `socat` for Windows, and I even found something like [`com0com`](https://com0com.sourceforge.net/) to create a virtual COM port,
but I couldn't figure out how to attach it to the `sermouse` driver.  Just like on Windows 9x, the Windows 11 `sermouse` scans the COM ports for mice on boot up.
There's no way to manually enable it on a arbitrary COM port, at least I couldn't figure out how.

So, I gave in and decided to make my own driver for the mouse.

[^1]: Should also work on MacOS and Linux, but I only tested it on Windows.
[^2]: This terminal server only has RJ-45 ports, according to the docs the pinout matches that of a Cisco console/rollover cable.
      I do have one of those, but I used a generic RJ-45 to DB-25 adapter to make my own.
