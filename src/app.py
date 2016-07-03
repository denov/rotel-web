#!flask/bin/python
from flask import Flask
from flask import render_template

import serial
import binascii


app = Flask(__name__)

ser = serial.Serial(
        port='/dev/ttyAMA0',
        baudrate = 115200,
        timeout=3
)

rsx1505 = {
    "zone2on": "FE 03 C9 16 4B 2D",
    "zone2off":"FE 03 C9 16 4A 2C",
    "zone2volUp":   "FE 03 C9 16 00 E2",
    "zone2volDown": "FE 03 C9 16 00 E3",

	# POWER & VOLUME COMMANDS
	"PowerToggle":	"FE 03 C9 10 0A E6",
	"PowerOff":	"FE 03 C9 10 4A 26",
	"PowerOn": "FE 03 C9 10 4B 27",
	"VolumeUp":	"FE 03 C9 10 0B E7",
	"VolumeDown": "FE 03 C9 10 0C E8",
	"MuteToggle": "FE 03 C9 10 1E FA",
	"PowerOffAllZones":	"FE 03 C9 10 71 4D",
		
	# SOURCE SELECTION COMMANDS	
	"SourceCD":	"FE 03 C9 10 02 DE",
	"SourceTuner":	"FE 03 C9 10 03 DF",
	"SourceTape":	"FE 03 C9 10 04 E0",
	"SourceVideo1":	"FE 03 C9 10 05 E1",
	"SourceVideo2":	"FE 03 C9 10 06 E2",
	"SourceVideo3":	"FE 03 C9 10 07 E3",
	"SourceVideo4":	"FE 03 C9 10 08 E4",
	"SourceVideo5":	"FE 03 C9 10 09 E5",
	"SourceMultiInput":	"FE 03 C9 10 15 F1",
		
	# SURROUND MODE COMMANDS	
	"Stereo": "FE 03 C9 10 11 ED",
	"Dolby3Stereo":	"FE 03 C9 10 12 EE",
	"DolbyProLogic": "FE 03 C9 10 13 EF",
	"DSPToggle": "FE 03 C9 10 14 F0",
	"Dolby3StereoToggle": "FE 03 C9 10 53 2F",
	"dtsNeo6Toggle": "FE 03 C9 10 54 30",
	"DSP1":	"FE 03 C9 10 57 33",
	"DSP2":	"FE 03 C9 10 58 34",
	"DSP3":	"FE 03 C9 10 59 35",
	"DSP4":	"FE 03 C9 10 5A 36",
	"5ChannelStereo": "FE 03 C9 10 5B 37",
	"7ChannelStereo": "FE 03 C9 10 5C 38",
	"DolbyPLIIxCinema":	"FE 03 C9 10 5D 39",
	"DolbyPLIIxMusic": "FE 03 C9 10 5E 3A",
	"DolbyPLIIxGame": "FE 03 C9 10 74 50",
	"DolbyProLogic": "FE 03 C9 10 5F 3B",
	"dtsNeo6Music":	"FE 03 C9 10 60 3C",
	"dtsNeo6Cinema": "FE 03 C9 10 61 3D",
	"PLIIxPanoramaToggle": "FE 03 C9 10 62 3E",
	"PLIIxDimensionUp":	"FE 03 C9 10 63 3F",
	"PLIIxDimensionDown": "FE 03 C9 10 64 40",
	"PLIIxCenterWidthUp": "FE 03 C9 10 65 41",
	"PLIIxCenterWidthDown":	"FE 03 C9 10 66 42",
	"DolbyDigitalEXToggle":	"FE 03 C9 10 68 44",
	"NextSurroundMode":	"FE 03 C9 10 22 FD 01",
		
	# TONE CONTROL COMMANDS
	"TrebleUp": "FE 03 C9 10 0D E9",
	"TrebleDown": "FE 03 C9 10 0E EA",
	"BassUp": "FE 03 C9 10 0F EB",
	"BassDown":	"FE 03 C9 10 10 EC",
	"ToneControlSelectOSD":	"FE 03 C9 10 67 43",
		
	# MENU COMMANDS	
	"OSDMenu": "FE 03 C9 10 18 F4",
	"Enter": "FE 03 C9 10 19 F5",
	"CursorRight": "FE 03 C9 10 1A F6",
	"CursorLeft": "FE 03 C9 10 1B F7",
	"CursorUp":	"FE 03 C9 10 1C F8",
	"CursorDown": "FE 03 C9 10 1D F9",
		
	# TUNER COMMANDS
	"TuneUp": "FE 03 C9 10 28 04",
	"TuneDown":	"FE 03 C9 10 29 05",
	"PresetUp":	"FE 03 C9 10 6F 4B",
	"PresetDown": "FE 03 C9 10 70 4C",
	"FrequencyUp": "FE 03 C9 10 72 4E",
	"FrequencyDown": "FE 03 C9 10 73 4F",
	"Memory": "FE 03 C9 10 27 03",
	"BandToggle": "FE 03 C9 10 24 00",
	"AM": "FE 03 C9 10 56 32",
	"FM": "FE 03 C9 10 55 31",
	"Tune-Preset": "FE 03 C9 10 20 FC",
	"TuningModeSelect":	"FE 03 C9 10 69 45",
	"PresetModeSelect":	"FE 03 C9 10 6A 46",
	"FrequencyDirect": "FE 03 C9 10 25 01",
	"PresetScan": "FE 03 C9 10 21 FD",
	"TunerDisplay":	"FE 03 C9 10 44 20",
	"RDSPTY": "FE 03 C9 10 45 21",
	"RDSTP": "FE 03 C9 10 46 22",
	"RDSTA": "FE 03 C9 10 47 23",
	"FMMono": "FE 03 C9 10 26 02",
		
	# NUMERIC KEY COMMANDS	
	"Number1": "FE 03 C9 10 2A 06",
	"Number2": "FE 03 C9 10 2B 07",
	"Number3": "FE 03 C9 10 2C 08",
	"Number4": "FE 03 C9 10 2D 09",
	"Number5": "FE 03 C9 10 2E 0A",
	"Number6": "FE 03 C9 10 2F 0B",
	"Number7": "FE 03 C9 10 30 0C",
	"Number8": "FE 03 C9 10 31 0D",
	"Number9": "FE 03 C9 10 32 0E",
	"Number0": "FE 03 C9 10 33 0F",
	"RecordFunctionSelect":	"FE 03 C9 10 17 F3",
	"DynamicRange":	"FE 03 C9 10 16 F2",
	"DigitalInput Select": "FE 03 C9 10 1F FB",
	"Zone2Main": "FE 03 C9 10 23 FF",
	"TemporaryCenterTrim":	"FE 03 C9 10 4C 28",
	"TemporarySubwooFErTrim": "FE 03 C9 10 4D 29",
	"TemporarySurroundTrim": "FE 03 C9 10 4E 2A",
	"CinemaEQToggle": "FE 03 C9 10 4F 2B",
	"FrontDisplayToggle": "FE 03 C9 10 52 2E",
	"DisplayRefresh": "FE 03 C9 10 FF DB",
	"PartyModeToggle": "FE 03 C9 10 6E 4A",
	"OutputResolution":	"FE 03 C9 10 75 51",
	"HDMIAmpMode": "FE 03 C9 10 78 54",
	"HDMITVMode": "FE 03 C9 10 79 55",
	#  "ForceFactoryDefault":	"FE 03 C9 10 93 6F",
		
	# MAIN ZONE POWER & VOLUME COMMANDS
	"MainZonePowerToggle":"FE 03 C9 14 0A EA",
	"MainZonePowerOff": "FE 03 C9 14 4A 2A",
	"MainZonePowerOn": "FE 03 C9 14 4B 2B",
	"MainZoneVolumeUp":	"FE 03 C9 14 00 E0",
	"MainZoneVolumeDown":"FE 03 C9 14 01 E1",
	"MainZoneMuteToggle":"FE 03 C9 14 1E FD 01",
	"MainZoneMuteOn": "FE 03 C9 14 6C 4C",
	"MainZoneMute Off":	"FE 03 C9 14 6D 4D",
		
	# MAIN ZONE SOURCE SELECTION COMMANDS
	"MainZoneVolumeDownCD":	"FE 03 C9 14 02 E2",
	"MainZoneVolumeDownTuner": "FE 03 C9 14 03 E3",
	"MainZoneVolumeDownTape": "FE 03 C9 14 04 E4",
	"MainZoneVolumeDownVideo1":	"FE 03 C9 14 05 E5",
	"MainZoneVolumeDownVideo2":	"FE 03 C9 14 06 E6",
	"MainZoneVolumeDownVideo3":	"FE 03 C9 14 07 E7",
	"MainZoneVolumeDownVideo4":	"FE 03 C9 14 08 E8",
	"MainZoneVolumeDownVideo5":	"FE 03 C9 14 09 E9",
	"MainZoneVolumeDownMultiInput":	"FE 03 C9 14 15 F5",
		
	# RECORD SOURCE SELECTION COMMANDS
	"RecordSourceCD": "FE 03 C9 15 02 E3",
	"RecordSourceTuner": "FE 03 C9 15 03 E4",
	"RecordSourceTape":	"FE 03 C9 15 04 E5",
	"RecordSourceVideo1": "FE 03 C9 15 05 E6",
	"RecordSourceVideo2": "FE 03 C9 15 06 E7",
	"RecordSourceVideo3": "FE 03 C9 15 07 E8",
	"RecordSourceVideo4": "FE 03 C9 15 08 E9",
	"RecordSourceVideo5": "FE 03 C9 15 09 EA",
	"RecordFollowMainZoneVolumeDown6": "FE 03 C9 15 6B 4C",

	# Zone2POWER & VOLUME COMMANDS
	"Zone2PowerToggle":	"FE 03 C9 16 0A EC",
	"Zone2PowerOff": "FE 03 C9 16 4A 2C",
	"Zone2PowerOn":	"FE 03 C9 16 4B 2D",
	"Zone2VolumeUp": "FE 03 C9 16 00 E2",
	"Zone2VolumeDown": "FE 03 C9 16 01 E3",
	"Zone2MuteToggle": "FE 03 C9 16 1E 00",
	"Zone2MuteOn": "FE 03 C9 16 6C 4E",
	"Zone2MuteOff":	"FE 03 C9 16 6D 4F",
	"PowerOffAllZones":	"FE 03 C9 16 71 53",
		
	# ZONE 2 SOURCE SELECTION COMMANDS
	"Zone2SourceCD": "FE 03 C9 16 02 E4",
	"Zone2SourceTuner": "FE 03 C9 16 03 E5",
	"Zone2SourceTape": "FE 03 C9 16 04 E6",
	"Zone2SourceVideo1": "FE 03 C9 16 05 E7",
	"Zone2SourceVideo2": "FE 03 C9 16 06 E8",
	"Zone2SourceVideo3": "FE 03 C9 16 07 E9",
	"Zone2SourceVideo4": "FE 03 C9 16 08 EA",
	"Zone2SourceVideo5": "FE 03 C9 16 09 EB",
	"Zone2FollowMainZoneSource": "FE 03 C9 16 6B 4D",

	# ZONE 2 TUNER COMMANDS
	"Zone2TuneUp": "FE 03 C9 16 28 0A",
	"Zone2TuneDown": "FE 03 C9 16 29 0B",
	"Zone2PresetUp": "FE 03 C9 16 6F 51",
	"Zone2PresetDown": "FE 03 C9 16 70 52",
	"Zone2FrequencyUp":	"FE 03 C9 16 72 54",
	"Zone2FrequencyDown": "FE 03 C9 16 73 55",
	"Zone2BandToggle": "FE 03 C9 16 24 06",
	"Zone2AM": "FE 03 C9 16 56 38",
	"Zone2FM": "FE 03 C9 16 55 37",
	"Zone2TunePreset":	"FE 03 C9 16 20 02",
	"Zone2TuningModeSelect": "FE 03 C9 16 69 4B",
	"Zone2PresetModeSelect": "FE 03 C9 16 6A 4C",
	"Zone2PresetScan": "FE 03 C9 16 21 03",
	"Zone2FMMono": "FE 03 C9 16 26 08",
		
	# ZONE 2 NUMERIC KEY COMMANDS
	"Zone2Number1":	"FE 03 C9 16 2A 0C",
	"Zone2Number2":	"FE 03 C9 16 2B 0D",
	"Zone2Number3":	"FE 03 C9 16 2C 0E",
	"Zone2Number4":	"FE 03 C9 16 2D 0F",
	"Zone2Number5":	"FE 03 C9 16 2E 10",
	"Zone2Number6":	"FE 03 C9 16 2F 11",
	"Zone2Number7":	"FE 03 C9 16 30 12",
	"Zone2Number8":	"FE 03 C9 16 31 13",
	"Zone2Number9":	"FE 03 C9 16 32 14",
	"Zone2Number0":	"FE 03 C9 16 33 15",
		
	# ZONE 2 OTHER COMMANDS	
	"PartyModeToggle":	"FE 03 C9 16 6E 50",
		
	# ZONE 3 POWER & VOLUME COMMANDS
	"Zone3PowerToggle":	"FE 03 C9 17 0A ED",
	"Zone3PowerOff": "FE 03 C9 17 4A 2D",
	"Zone3PowerOn":	"FE 03 C9 17 4B 2E",
	"Zone3VolumeUp": "FE 03 C9 17 00 E3",
	"Zone3VolumeDown": "FE 03 C9 17 01 E4",
	"Zone3MuteToggle": "FE 03 C9 17 1E 01",
	"Zone3MuteOn": "FE 03 C9 17 6C 4F",
	"Zone3MuteOff":	"FE 03 C9 17 6D 50",
	"PowerOffAllZones":	"FE 03 C9 17 71 54",
		
	# Zone 3 SOURCE SELECTION COMMANDS
	"Zone3SourceCD": "FE 03 C9 17 02 E5",
	"Zone3SourceTuner":	"FE 03 C9 17 03 E6",
	"Zone3SourceTape":	"FE 03 C9 17 04 E7",
	"Zone3SourceVideo1":"FE 03 C9 17 05 E8",
	"Zone3SourceVideo2":"FE 03 C9 17 06 E9",
	"Zone3SourceVideo3":"FE 03 C9 17 07 EA",
	"Zone3SourceVideo4":"FE 03 C9 17 08 EB",
	"Zone3SourceVideo5":"FE 03 C9 17 09 EC",
	"Zone3FollowMainZoneSource":"FE 03 C9 17 6B 4E",
		
	# ZONE 3 TUNER COMMANDS
	"Zone3TuneUp":	"FE 03 C9 17 28 0B",
	"Zone3TuneDown": "FE 03 C9 17 29 0C",
	"Zone3PresetUp": "FE 03 C9 17 6F 52",
	"Zone3PresetDown":	"FE 03 C9 17 70 53",
	"Zone3FrequencyUp": "FE 03 C9 17 72 55",
	"Zone3FrequencyDown": "FE 03 C9 17 73 56",
	"Zone3BandToggle":	"FE 03 C9 17 24 07",
	"Zone3AM": "FE 03 C9 17 56 39",
	"Zone3FM": "FE 03 C9 17 55 38",
	"Zone3TunePreset":	"FE 03 C9 17 20 03",
	"Zone3TuningModeSelect": "FE 03 C9 17 69 4C",
	"Zone3PresetModeSelect": "FE 03 C9 17 6A 4D",
	"Zone3PresetScan": "FE 03 C9 17 21 04",
	"Zone3FMMono": "FE 03 C9 17 26 09",
		
	# ZONE 3 NUMERIC KEY COMMANDS",	
	"Zone3Number1":	"FE 03 C9 17 2A 0D",
	"Zone3Number2":	"FE 03 C9 17 2B 0E",
	"Zone3Number3":	"FE 03 C9 17 2C 0F",
	"Zone3Number4":	"FE 03 C9 17 2D 10",
	"Zone3Number5":	"FE 03 C9 17 2E 11",
	"Zone3Number6":	"FE 03 C9 17 2F 12",
	"Zone3Number7":	"FE 03 C9 17 30 13",
	"Zone3Number8":	"FE 03 C9 17 31 14",
	"Zone3Number9":	"FE 03 C9 17 32 15",
	"Zone3Number0":	"FE 03 C9 17 33 16",
		
	# ZONE 3 OTHER COMMANDS
	"PartyModeToggle":	"FE 03 C9 17 6E 51",
		
	# ZONE 4 POWER & VOLUME COMMANDS
	"Zone4PowerToggle":	"FE 03 C9 18 0A EE",
	"Zone4PowerOff": "FE 03 C9 18 4A 2E",
	"Zone4PowerOn":	"FE 03 C9 18 4B 2F",
	"Zone4VolumeUp": "FE 03 C9 18 00 E4",
	"Zone4VolumeDown": "FE 03 C9 18 01 E5",
	"Zone4MuteToggle": "FE 03 C9 18 1E 02",
	"Zone4MuteOn": "FE 03 C9 18 6C 50",
	"Zone4MuteOff":	"FE 03 C9 18 6D 51",
	"PowerOffAllZones":	"FE 03 C9 18 71 55",
		
	# ZONE 4 SOURCE SELECTION COMMANDS	
	"Zone4SourceCD": "FE 03 C9 18 02 E6",
	"Zone4SourceTuner":	"FE 03 C9 18 03 E7",
	"Zone4SourceTape": "FE 03 C9 18 04 E8",
	"Zone4SourceVideo 1": "FE 03 C9 18 05 E9",
	"Zone4SourceVideo 2": "FE 03 C9 18 06 EA",
	"Zone4SourceVideo 3": "FE 03 C9 18 07 EB",
	"Zone4SourceVideo 4": "FE 03 C9 18 08 EC",
	"Zone4SourceVideo 5": "FE 03 C9 18 09 ED",
	"Zone 4 Follow Main Zone Source": "FE 03 C9 18 6B 4F",
		
	# ZONE 4 TUNER COMMANDS	
	"Zone4TuneUp":	"FE 03 C9 18 28 0C",
	"Zone 4 TuneDown":	"FE 03 C9 18 29 0D",
	"Zone 4 Preset Up":	"FE 03 C9 18 6F 53",
	"Zone 4 Preset Down": "FE 03 C9 18 70 54",
	"Zone 4 Frequency Up": "FE 03 C9 18 72 56",
	"Zone 4 Frequency Down": "FE 03 C9 18 73 57",
	"Zone 4 Band Toggle": "FE 03 C9 18 24 08",
	"Zone 4 AM": "FE 03 C9 18 56 3A",
	"Zone 4 FM": "FE 03 C9 18 55 39",
	"Zone 4 Tune / Preset":	"FE 03 C9 18 20 04",
	"Zone 4 Tuning Mode Select": "FE 03 C9 18 69 4D",
	"Zone 4 Preset Mode Select": "FE 03 C9 18 6A 4E",
	"Zone 4 Preset Scan": "FE 03 C9 18 21 05",
	"Zone 4 FM Mono": "FE 03 C9 18 26 0A",
		
	# ZONE 4 NUMERIC KEY COMMANDS	
	"Zone4Number1":	"FE 03 C9 18 2A 0E",
	"Zone4Number2":	"FE 03 C9 18 2B 0F",
	"Zone4Number3":	"FE 03 C9 18 2C 10",
	"Zone4Number4":	"FE 03 C9 18 2D 11",
	"Zone4Number5":	"FE 03 C9 18 2E 12",
	"Zone4Number6":	"FE 03 C9 18 2F 13",
	"Zone4Number7":	"FE 03 C9 18 30 14",
	"Zone4Number8":	"FE 03 C9 18 31 15",
	"Zone4Number9":	"FE 03 C9 18 32 16",
	"Zone4Number0":	"FE 03 C9 18 33 17",
		
	# ZONE 4 OTHER COMMANDS	
	"Party Mode Toggle Table":	"FE 03 C9 18 6E 52",
		
	# VOLUME DIRECT COMMANDS 	
	"VolumeMin":	"FE 03 C9 30 00 FC",
	"Volume1":	"FE 03 C9 30 01 FD",
	"Volume2":	"FE 03 C9 30 02 FD",
	"Volume3":	"FE 03 C9 30 03 FF",
	"Volume4":	"FE 03 C9 30 04 00",
	"Volume5":	"FE 03 C9 30 05 01",
	"Volume6":	"FE 03 C9 30 06 02",
	"Volume 7":	"FE 03 C9 30 07 03",
	"Volume8":	"FE 03 C9 30 08 04",
	"Volume9":	"FE 03 C9 30 09 05",
	"Volume10":	"FE 03 C9 30 0A 06",
	"Volume11":	"FE 03 C9 30 0B 07",
	"Volume12":	"FE 03 C9 30 0C 08",
	"Volume13":	"FE 03 C9 30 0D 09",
	"Volume14":	"FE 03 C9 30 0E 0A",
	"Volume15":	"FE 03 C9 30 0F 0B",
	"Volume16":	"FE 03 C9 30 10 0C",
	"Volume32":	"FE 03 C9 30 20 1C",
	"Volume48":	"FE 03 C9 30 30 2C",
	"Volume64":	"FE 03 C9 30 40 3C",
	"Volume80":	"FE 03 C9 30 50 4C",
	"Volume95":	"FE 03 C9 30 5F 5B",
		
	#"ZONE 2 VOLUME DIRECT COMMANDS",	
	"Zone2VolumeMin":"FE 03 C9 32 00 FD",
	"Zone2Volume1":	"FE 03 C9 32 01 FF",
	"Zone2Volume2":	"FE 03 C9 32 02 00",
	"Zone2Volume3":	"FE 03 C9 32 03 01",
	"Zone2Volume4":	"FE 03 C9 32 04 02",
	"Zone2Volume5":	"FE 03 C9 32 05 03",
	"Zone2Volume6":	"FE 03 C9 32 06 04",
	"Zone2Volume7":	"FE 03 C9 32 07 05",
	"Zone2Volume8":	"FE 03 C9 32 08 06",
	"Zone2Volume9":	"FE 03 C9 32 09 07",
	"Zone2Volume10":"FE 03 C9 32 0A 08",
	"Zone2Volume11":"FE 03 C9 32 0B 09",
	"Zone2Volume12":"FE 03 C9 32 0C 0A",
	"Zone2Volume13":"FE 03 C9 32 0D 0B",
	"Zone2Volume14":"FE 03 C9 32 0E 0C",
	"Zone2Volume15":"FE 03 C9 32 0F 0D",
	"Zone2Volume16":"FE 03 C9 32 10 0E",
	"Zone2Volume32":"FE 03 C9 32 20 1E",
	"Zone2Volume48":"FE 03 C9 32 30 2E",
	"Zone2Volume64":"FE 03 C9 32 40 3E",
	"Zone2Volume80":"FE 03 C9 32 50 4E",
	"Zone2Volume89":"FE 03 C9 32 5F 57",
		
	# ZONE 3 VOLUME DIRECT COMMANDS
	"Zone3NumberMin":	"FE 03 C9 33 00 FF",
	"Zone3Number1":	"FE 03 C9 33 01 00",
	"Zone3Number2":	"FE 03 C9 33 02 01",
	"Zone3Number3":	"FE 03 C9 33 03 02",
	"Zone3Number4":	"FE 03 C9 33 04 03",
	"Zone3Number5":	"FE 03 C9 33 05 04",
	"Zone3Number6":	"FE 03 C9 33 06 05",
	"Zone3Number7":	"FE 03 C9 33 07 06",
	"Zone3Number8":	"FE 03 C9 33 08 07",
	"Zone3Number9":	"FE 03 C9 33 09 08",
	"Zone3Number10":"FE 03 C9 33 0A 09",
	"Zone3Number16": "FE 03 C9 33 10 0F",
	"Zone3Number32": "FE 03 C9 33 20 1F",
	"Zone3Number48": "FE 03 C9 33 30 2F",
	"Zone3Number64": "FE 03 C9 33 40 3F",
	"Zone3Number80": "FE 03 C9 33 50 4F",
	"Zone3Number89": "FE 03 C9 33 5F 58",
		
	# ZONE 4 VOLUME DIRECT COMMANDS
	"Zone4NumberMin": "FE 03 C9 34 00 00",
	"Zone4Number1":	"FE 03 C9 34 01 01",
	"Zone4Number2":	"FE 03 C9 34 02 02",
	"Zone4Number3":	"FE 03 C9 34 03 03",
	"Zone4Number4":	"FE 03 C9 34 04 04",
	"Zone4Number5":	"FE 03 C9 34 05 05",
	"Zone4Number6":	"FE 03 C9 34 06 06",
	"Zone4Number7":	"FE 03 C9 34 07 07",
	"Zone4Number8":	"FE 03 C9 34 08 08",
	"Zone4Number9":	"FE 03 C9 34 09 09",
	"Zone4Number10": "FE 03 C9 34 0A 0A",
	"Zone4Number16": "FE 03 C9 34 10 10",
	"Zone4Number32": "FE 03 C9 34 20 20",
	"Zone4Number48": "FE 03 C9 34 30 30",
	"Zone4Number64": "FE 03 C9 34 40 40",
	"Zone4Number80": "FE 03 C9 34 50 50",
		
	# TRIGGER DIRECT COMMANDS
	"MainZone12VTrigger1Toggle": "FE 03 C9 40 00 0C",
	"MainZone12VTrigger2Toggle": "FE 03 C9 40 01 0D",
	"MainZone12VTrigger3Toggle": "FE 03 C9 40 02 0E",
	"MainZone12VTrigger4Toggle": "FE 03 C9 40 03 0F",
	"MainZone12VTrigger5Toggle": "FE 03 C9 40 04 10",
	"MainZone12VTrigger6Toggle": "FE 03 C9 40 05 11",
	"Zone212VTrigger1Toggle": "FE 03 C9 40 06 12",
	"Zone212VTrigger2Toggle": "FE 03 C9 40 07 13",
	"Zone212VTrigger3Toggle": "FE 03 C9 40 08 14",
	"Zone212VTrigger4Toggle": "FE 03 C9 40 09 15",
	"Zone212VTrigger5Toggle": "FE 03 C9 40 0A 16",
	"Zone212VTrigger6Toggle": "FE 03 C9 40 0B 17",
	"Zone312VTrigger1Toggle": "FE 03 C9 40 0C 18",
	"Zone312VTrigger2Toggle": "FE 03 C9 40 0D 19",
	"Zone312VTrigger3Toggle": "FE 03 C9 40 0E 1A",
	"Zone312VTrigger4Toggle": "FE 03 C9 40 0F 1B",
	"Zone312VTrigger5Toggle": "FE 03 C9 40 10 1C",
	"Zone312VTrigger6Toggle": "FE 03 C9 40 11 1D",
	"Zone412VTrigger1Toggle": "FE 03 C9 40 12 1E",
	"Zone412VTrigger2Toggle": "FE 03 C9 40 13 1F",
	"Zone412VTrigger3Toggle": "FE 03 C9 40 14 20",
	"Zone412VTrigger4Toggle": "FE 03 C9 40 15 21",
	"Zone412VTrigger5Toggle": "FE 03 C9 40 16 22",
	"Zone412VTrigger6Toggle": "FE 03 C9 40 17 23"		
}


@app.route('/')
def index():
    return render_template("index.html")

	
@app.route('/commands')
def commands():
    return render_template("commands.html", cmds=rsx1505)
	

@app.route('/rsx1505/<cmd>')
def sendCmd(cmd):
   global rsx1505
   if cmd in rsx1505:
      ser.write(formatData(rsx1505[cmd]))
      return cmd
   else:
      return "cmd not found. see /commands for list"


def formatData(data):
   data = data.replace(" ", "")
   return binascii.a2b_hex(data)



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
