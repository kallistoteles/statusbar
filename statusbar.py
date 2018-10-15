#!/usr/bin/python
import tkinter
import time
import subprocess
import alsaaudio

m = alsaaudio.Mixer()
global vol_before_mute 
vol_before_mute = 0
global last_active
last_active = time.time()

def tick():
	#get current battery status
	f = open('/sys/class/power_supply/BAT0/capacity', 'r')
	battery_capacity = int(f.read().strip())
	f.close()
	if battery_capacity > 100: battery_capacity = 100
	battery_capacity = 'b' + str(battery_capacity) + '%'

	#get current wifi quality
	proc = subprocess.Popen(["iwconfig", "wlp2s0"],stdout=subprocess.PIPE, universal_newlines=True)
	out, err = proc.communicate()

	wifi_quality='?%'
	for line in out.split("\n"):
		if line.find("Quality") > 0:
			wifi_quality = 'w'+str(int(int(line[23:25])*100 / int(line[26:28]))) + '%'
    
	# get the current local time from the PC
	#    time_string = time.strftime('%Y-%m-%d %H:%M:%S')
	time_string = time.strftime('%H:%M')

	output_string = '| ' + time_string + ' | ' + battery_capacity + ' | ' + wifi_quality + ' |'
	#print(output_string)
	# if time string has changed, update it
	clock.config(text=output_string)
	clock.after(1000, tick)

	# Remove bar after x seconds inactivity
	time_to_close = 2*60
	if (time.time() - last_active) > time_to_close: root.destroy()
	
def end_application(event):
	root.destroy()

def volume_up(event):
	print('turning volume up')
	vol = int(m.getvolume()[0])
	newVol = vol + 1
	if newVol > 100: newVol = 100
	m.setvolume(newVol)

def volume_down(event):
	print('turning volume down')
	vol = int(m.getvolume()[0])
	newVol = vol - 1
	if newVol < 0: newVol = 0
	m.setvolume(newVol)

def volume_mute(event):
	print('volume mute/unmute')
	global vol_before_mute
	vol = int(m.getvolume()[0])
	if vol > 0:
		vol_before_mute = vol
		m.setvolume(0)
	else:
		m.setvolume(vol_before_mute)


root = tkinter.Tk()
root.overrideredirect(1)
#root.wait_visibility(root)
root.wm_attributes("-alpha", 0.0)
root.configure(background='#1B1B1F')
root.geometry('155x15+%d+0' % int(root.winfo_screenwidth()*.8))
clock = tkinter.Label(root, font=('arial', 8), bg='#1B1B1F', fg="#AEA684")
#clock = tkinter.Label(root, font=('arial', 8), fg="#AEA684")
clock.bind("<Button-1>", volume_mute)
clock.bind("<Button-3>", end_application)
clock.bind("<Button-4>", volume_up)
clock.bind("<Button-5>", volume_down)
clock.grid(row=0, column=1) 
tick()
root.mainloop()

