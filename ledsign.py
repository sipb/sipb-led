# ledsign: Outputs a message to an M-500 led scrolly sign.
# Documentation on the protocol is sparse; but a few good resources are:
#  - http://wls.wwco.com/ledsigns/m-500/
#    (in particular, much of this code is based on the protocol descriptiojn at <http://wls.wwco.com/ledsigns/m-500/m-500-protocol.php>
#  - http://www.avbrand.com/projects/carpc/ledsign/technew.asp
#  - https://github.com/BrightLedSigns/LedSign
#
import serial, io, sys;

# For now, assume we're writing to /dev/ttyUSB0. 
ser = serial.Serial("/dev/ttyUSB0");


# Source for the next section:   http://wls.wwco.com/ledsigns/m-500/m-500-protocol.php

# The first part of any command is the file number. (A file is basically a slot in memory.)
FILE1 = "f01"; # The first file
FILE2 = "f02"; # The second file

# The next part of a command is the transition mode.
transitions = {
	"cyclic": "A",
	"immediate": "B",
	"open right": "C",
	"open left": "D",
	"open out": "E",
	"open in": "F",
	"cover out": "G",
	"cover right": "H",
	"cover left": "I",
	"cover in": "J",
	"scroll up": "K",
	"scroll down": "L",
	"interlace 1": "M",
	"interlace 2": "N",
	"cover up": "O",
	"cover down": "P",
	"scan line": "Q",
	"explode": "R",
	"pacman": "S",
	"stack": "T",
	"shoot": "U",
	"flash": "V",
	"random": "W",
	"slide in": "X",
};

# There are escape sequences for colors and fonts. These can be used anywhere in your message. You can change colors mid-message if you want.
# Note that it actually expects a literal backslash followed by a letter -- these aren't control characters.
colors = {
	"red": "\\a",
	"bright red": "\\b",
	"orange": "\\c",
	"bright orange": "\\d",
	"yellow": "\\e",
	"bright yellow": "\\f",
	"green": "\\g",
	"bright green": "\\h",
	"layer mix": "\\i",
	"bright layer mix": "\\j",
	"vertical mix": "\\k",
	"sawtooth mix": "\\l",
	"green on red": "\\m", # Why would you ever...
	"red on green": "\\n", # Oh god why
	"orange on red": "\\o", # This isn't even readable!
	"yellow on green": "\\p" # Just no.
};

fonts = {
	"default": "\\s",
	"short": "\\q",
	"short and wide": "\\r",
	"wide": "\\t",
	"7x9": "\\u",
	"extra wide": "\\v",
	"small": "\\w"
};

# There are a few specials
graphics = {
	"cityscape": "^Q", #These are big graphics: they fill the whole display
	"traffic": "^R",
	"tea party": "^S",
	"telephone": "^T",
	"sunset": "^U",
	"cargo ship": "^V",
	"swimmers": "^W",
	"mouse": "^X",
	"sun": "^66", #These are little graphics: they're each a few letters wide.
	"cloudy": "^67",
	"rain": "^68",
	"clock": "^69",
	"phone": "^70",
	"specs": "^71",
	"faucet": "^72",
	"rocket": "^73",
	"bug": "^74",
	"key": "^75",
	"shirt": "^76",
	"chopper": "^77",
	"car": "^78",
	"tank": "^79",
	"house": "^80",
	"teapot": "^81",
	"trees": "^82",
	"swan": "^83",
	"mbike": "^84",
	"bike": "^85",
	"crown": "^86",
	"strawberry": "^87",
	"arrow right": "^88",
	"arrow left": "^89",
	"arrow down": "^90",
	"arrow up": "^91",
	"cup": "^92",
	"chair": "^93",
	"shoe": "^94",
	"glass": "^95"
};

specialchars = {
	"^": r"\^",
	"\\": r"\\",
	"EOL": "\r", # A line ends with a carriage return. The next line must begin with a transition.
	"newline": "\r" + transitions["open right"], # This is a shortcut for adding a new line with a reasonable transition.
	"EOM": "\r\r\r" # A command ends with three carriage returns.
}

#For convenience
EOM = specialchars["EOM"];
EOL = specialchars["EOL"];
newline = specialchars["newline"];



def demo():
	#Demo mode

	# This tells the sign to pay attention. 128 addresses all signs -- apparently you can address individual signs by using a device's ID number (whatever that is).
	ser.write("~128~");
	ser.write(FILE1 + transitions["pacman"] + colors["bright red"] + "SIPB " + colors["bright layer mix"]+ "LED!" + newline);

	# Colors demo
	ser.write("Colors:  " + "".join(sorted(colors[s] + "  " + s + "  " for s in colors)) + newline);

	# Fonts demo
	ser.write("Fonts:  " + "".join(sorted(fonts[s] + "  " + s + ": Five hazards! Quickly, exit by jumping down.  " for s in fonts)) + newline);

	# Transitions demo
	ser.write("Transitions:" + "".join(sorted(EOL + transitions[s] + s for s in transitions)) + newline);

	# Graphics demo
	ser.write("Graphics:  " + "".join(sorted(s + " " + graphics[s] + "     " for s in graphics)) + EOM);





#Format a string so that it can specify fonts, graphics, colors, etc.
def format(s):
	for m in (colors, fonts, graphics, specialchars, transitions):
		for k, v in m.items():
			s = s.replace("<"+k+">", v);
	# So that you can pass a "<" or a ">", we use "<lt>" and "<gt>"
	# To avoid edge cases like "<lt>gt>", we want to do these replacements simultaneously.
	# We didn't know an easy way to do this, so we'll use an out-of-band character (\0) instead to avoid issues.
	s = s.replace("<lt>", "<\0");
	s = s.replace("<gt>", ">");
	s = s.replace("<\0", "<");
	return s;

import SocketServer;

class Server(SocketServer.TCPServer):
	allow_reuse_address = True;

class Handler(SocketServer.StreamRequestHandler):
	def handle(self):
		while True:
			line = self.rfile.readline().strip();
			if not line: break;
			elif line == "[[demo]]": demo();
			else:
				ser.write("~128~");
				ser.write(FILE1 + transitions["open right"] + format(line) + EOM);

Server(("", 41337), Handler).serve_forever();

