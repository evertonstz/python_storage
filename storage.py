import subprocess
import os

#variables#
color = True
folders = [{"dir":"/home/everton/media/.plex/", "name":"Plex Folder"}, \
{"dir":"/home/everton/media/.transmission/downloads/", "name":"Torrent Downloads"}]

home = os.getenv("HOME")

if color == True:
	NC='\033[0m'
	BLACK, GREY='\033[0;30m', '\033[1;30m'
	RED, LRED='\033[0;31m', '\033[1;31m'
	GREEN, LGREEN = '\033[0;32m', '\033[1;32m'
	BROWN, YELLOW = '\033[0;33m', '\033[1;33m'
	BLUE, LBLUE='\033[0;34m', '\033[1;34m'
else:
	NC = ''
	BLACK, GREY = '', ''
	RED, LRED = '', ''
	GREEN, LGREEN = '', ''
	BROWN, YELLOW = '', ''
	BLUE, LBLUE = '', '' 

#functions#
def break_str(string, length, dots=True, fill=True, fill_symbol=" ", align="left"):
	if len(string) >= length:
		if dots == 1:
			return(string[:length-3]+"...")
		if dots == 0:
			return(string[:length])
	elif len(string) == length:
		return(string)
	else:
		if align.lower() in ["left", "l"]:
			return(string+fill_symbol*(length-len(string)))
		elif align.lower() in ["right", "r"]:
			return(fill_symbol*(length-len(string))+string)
		if align.lower() in ["center", "c"]:
			sobra = length - len(string)
			if sobra%2 == 0:
				filling = int(sobra/2)*fill_symbol
				return( filling+string+filling )
			else:
				filling_l = (int(sobra/2)+1)*fill_symbol
				filling_r = (length-len(string)-int(sobra/2)-1)*fill_symbol
				return( filling_l+string+filling_r )
			
def progress_bar(number, symbol="#", fill_width=20,open_symbol="[", close_symbol="]", color=True, unfilled_symbol="-"):
	if color == 0:
		slice = int(number*fill_width/100)
		return(open_symbol+symbol*slice+unfilled_symbol*(fill_width-slice)+close_symbol)
	else:
		
		slice = int(number*fill_width/100)
		if fill_width%4 == 0:
			chunks = int(fill_width/4)
			chunks_dir = ""
			for i in range(0, slice):
				if i in range(0, chunks):
					chunks_dir+=LBLUE+symbol
				elif i in range(chunks, chunks*2):
					chunks_dir+=LGREEN+symbol
				elif i in range(chunks*2, chunks*3):
					chunks_dir+=YELLOW+symbol
				elif i in range(chunks*3, chunks*4):
					chunks_dir+=LRED+symbol

			return(open_symbol+chunks_dir+GREY+unfilled_symbol*(fill_width-slice)+close_symbol+NC)
		else:
			print('ERROR: Use a number divisible by 4 in "fill_width".')
			exit(1)
		
def terminal_size():
    import fcntl, termios, struct
    th, tw, hp, wp = struct.unpack('HHHH',
        fcntl.ioctl(0, termios.TIOCGWINSZ,
        struct.pack('HHHH', 0, 0, 0, 0)))
    return tw

term_size = terminal_size()
name_size = int(30/100*term_size)
dir_size = term_size - name_size

df = subprocess.Popen(['df', "-h", "/"], stdout=subprocess.PIPE).stdout.read().decode().split("\n")
total_disk_stats = [x for x in df[1].split(" ") if x != ""]
disk_name = "DISK"

hd_used = break_str(total_disk_stats[2], 5)
hd_total = break_str(total_disk_stats[1], 5)
hd_perc = break_str(total_disk_stats[4], length=6,dots=0, align="r")

print(break_str("- o -", length=term_size, align="c", fill_symbol="-"))
print("\n"+LBLUE+break_str(disk_name, name_size)+LRED+break_str(total_disk_stats[0], dir_size)+NC)
print(BROWN+"└Usage: "+NC, hd_used, \
	GREY+"of "+NC, hd_total, \
	GREY+"|"+NC+hd_perc+ \
	progress_bar( int(total_disk_stats[4][:-1]), \
	symbol="/", open_symbol=BROWN+"["+NC, close_symbol=BROWN+"]"+NC ),"\n" ) 


for i in folders:
	used_mb = subprocess.Popen(['du', "-sh", "--block-size=1M", i["dir"]], stdout=subprocess.PIPE).stdout.read().decode().split("\t")[0]
	name = break_str(i["name"], name_size).upper()
	
	dir = i["dir"]
	if dir.endswith("\\") or dir.endswith("/"):
		dir = dir[:-1]
	if dir.startswith(home):
		dir = dir.replace(home, "~")
	
	#todo: detect the partition were the folder is to calculate the percentage
	folder_used = break_str(str(round(int(used_mb)/1024, 1))+"G", 15)
	folder_perc = int(int(used_mb)/1024*100/int(total_disk_stats[1][:-1]))
	
	print(LBLUE+name+LRED+break_str(dir, dir_size)+NC)
	print(BROWN+"└Usage: "+NC,folder_used, GREY+"|"+NC+ \
	break_str(str(folder_perc)+"%", length=6,dots=0, align="r")+ \
	progress_bar( folder_perc, symbol="/", open_symbol=BROWN+"["+NC, close_symbol=BROWN+"]"+NC ), "\n")
print(break_str("- o -", length=term_size, align="c", fill_symbol="-"))	

#proc = subprocess.Popen(['du', "-sh", "--block-size=1M", folder], stdout=subprocess.PIPE).stdout.read().decode().split("\t")[0]
#print(proc)

