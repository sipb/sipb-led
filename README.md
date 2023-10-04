# sipb-led

## Setup

On doorpi.mit.edu, symlink `led.service` to `/etc/systemd/system` and enable and start the service. The TCP server runs on port 41337.

## Usage

`echo message | nc doorpi.mit.edu 41337 -c`

See https://wls.wwco.com/ledsigns/m-500/m-500-protocol.php for docs on how to change the text color and font and other useless fluff.

On doorpi.mit.edu, you can check `journalctl -xeu led` for this program's logs.
