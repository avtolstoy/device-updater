from Enum import enum
import os

# text "To start updating your device, conenct it to your computer via a USB cable. ??"
# image is electron greyed out and slightly translucent
# when the device is connected, the image moves to the left, a cable and laptop appear
# for now, no device info. later versions will display details of the connected device. 
# text changes "To update your device, click on the update button."
# as the device updates, it blinks the magenta LED
# as the device updates, lights flow along the USB cable. 
# the round updater button fills in as the update progresses. 
# when the update is complete, button changes to complete.
# disconnecting the device resets the system. 

# monitor serial connections every second to determine which devices are available and publish that as donnect/disconnect events. 

# connect/disconenct passed through a filter of interesting devices
# map from VID/PID to device type.  
# maintains a list of USB devices so the same device is featured in the disconnect method.

# refactor ymodem class to provide bytes transferred progress 



class UpdateController:
	
	def __init__(self):
		self.updateEnabled = BooleanProperty()	# bound property
		self.device = None
		self.deviceManager = DeviceManager()
		self.updater = Updater()
		self.state = ProgressState()
	
	void start():
		if not self.updateEnabled or not self.device:
			return
		files = self.device.system_files
		tasks = [UpdateFirmware(f) for f in files]
		self.updater.start(tasks, self.state, self.device)
		
		

class UpdateFirmware:
	# file to update
	# each device class maintains a list of UpdateFirmare instances against version
	# these are flashed in order	
	def __init__(self, file):
		self.file
		self.progress = self.asProgress()

	def asProgress(self):
		size = os.path.getsize(self.file)
		return ProgressSpan(size, name=os.path.basename(self.file))	

	def start(self):
		progress = self.progress
		# run ymodem updating bytes transferred count to progress
		LightYModem modem;
		modem.transfer(self.file, self.progress.update)
		# todo - catch exception and set state to fail

class Updater:
	# queue of update requests. for now, udpate request is flash a firmware file
	
	# manages the flash process
	# progress monitor 
	# status monitor
	# target device
	
	def start(items, progress, device):
		composite = CompositeProgress([i.progress for i in items], progress)
		progress.setStatus("Entering update mode");
		device.listen()
		for i in items:
			progress.setStatus(i.file)
			device.listen()
			i.start()
		progress.setStatus("Update complete")


class FlashState(Enum):
	not_connected = 1
	not_started = 2
	in_progress = 3
	error = 4
	complete = 5


class ProgressState:
"""
maintains the application state
"""
	# status: not connected, not started, in progress, success, error
	# ProgressSpan
	def __init__(self):
		self.onChange = EventHook()
		self.state = None
		self.progress = None
		self.process_max = None
		self.setState(FlashState.not_conencted)
		
	def setState(self,state):
		old = self.state
		self.state = state
		if old!=state:
			self.onChange.fire(self);
		
	def update(self, current):
		self.progress = current
		

