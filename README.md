# sipb-led

## Setup

On doorpi.mit.edu, symlink `led.service` to `/etc/systemd/system` and enable and start the service. The TCP server runs on port 41337.

## Usage

`echo message | nc doorpi.mit.edu 41337 -c`

See https://wls.wwco.com/ledsigns/m-500/m-500-protocol.php for docs on how to change the text color and font and other useless fluff.

On doorpi.mit.edu, you can check `journalctl -xeu led` for this program's logs.

You can also use the sign interactively by SSHing into doorpi and running in a Python console:
```
import serial
ser = serial.Serial("/dev/ttyUSB0")
ser.write(b"~128~Hi")
```

## Sequencer module

Copied from Mattermost:

```
tl;dr: sign has 10 sequencer slots, each of which can be programmed with (a subset of days of week, a time span 0000-2359, a list of message slots).
sequencer slots are swept left to right, lower index takes higher priority; if date and time matches, it loops the contents of the message slots in sequence
if no slots match, default to last-set page (which is what the sign's currently been doing)
protocol string is S[slot][daysofweek][starttime][endtime][slot#*] where:
slot ::= 0-9, slot id
daysofweek = (0-1){7}, each number corresponds to one day
startime, endtime ::= 0000 thru 2359, obvious parse
each slot# ::= a 2-number ID that can be set through the f prefix
```
