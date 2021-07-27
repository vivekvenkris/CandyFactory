class StatusManager(object):

	__instance = None
	@staticmethod
	def getInstance():
		""" Static access method. """
		if StatusManager.__instance == None:
			StatusManager()
		return StatusManager.__instance


	def __init__(self):

		if StatusManager.__instance != None:
			raise Exception("This class is a singleton! use StatusManager.getInstance()")
		else:
			StatusManager.__instance = self

		self.__INIT = 0
		self.__RSYNC_TO_STAGING = 1
		self.__RSYNC_TO_PROCESSING = 2
		self.__FILTOOLS = 3
		self.__RFIFIND_MASK = 4
		self.__ZERO_DM_ACCELSEARCH = 5

		self.__PEASOUP = 6
		self.__CANDIDATE_RFI_MATCHING = 7
		self.__FOLD = 8
		self.__PICS_SCORER = 9
		self.__CSV_GEN = 10

		self.__SEARCH_TYPES = "ZERO_ACC, ACC, SEGMENTED"

		self.__SEARCH_TYPE_ZERO_ACC = "ZERO_ACC"
		self.__SEARCH_TYPE_ACC = "ACC"
		self.__SEARCH_TYPE_SEGMENTED = "SEG"

	@property
	def INIT(self):
		return self.__INIT

	@property
	def SEARCH_TYPES(self):
		return self.__SEARCH_TYPES

	@property
	def RSYNC_TO_STAGING(self):
		return self.__RSYNC_TO_STAGING
	@property
	def RSYNC_TO_PROCESSING(self):
		return self.__RSYNC_TO_PROCESSING
	@property
	def FILTOOLS(self):
		return self.__FILTOOLS
	@property
	def RFIFIND_MASK(self):
		return self.__RFIFIND_MASK
	@property
	def ZERO_DM_ACCELSEARCH(self):
		return self.__ZERO_DM_ACCELSEARCH
	@property
	def PEASOUP(self):
		return self.__PEASOUP
	@property
	def CANDIDATE_RFI_MATCHING(self):
		return self.__CANDIDATE_RFI_MATCHING
	@property
	def FOLD(self):
		return self.__FOLD
	@property
	def PICS_SCORER(self):
		return self.__PICS_SCORER
	@property
	def CSV_GEN(self):
		return self.__CSV_GEN 

	@property
	def SEARCH_TYPE_ZERO_ACC(self):
		return self.__SEARCH_TYPE_ZERO_ACC
	
	@property
	def SEARCH_TYPE_ACC(self):
		return self.__SEARCH_TYPE_ACC
	
	@property
	def SEARCH_TYPE_SEGMENTED(self):
		return self.__SEARCH_TYPE_SEGMENTED
	


	
STATUS_DICT ={
	"00_INIT": "0", 
	"01_RSYNC_TO_STAGING": "1", 
	"02_RSYNC_TO_PROCESSING": "2", 
	"03_FILTOOLS": "3", 
	"04_RFIFIND_MASK": "4", 
	"05_ZERO_DM_ACCELSEARCH": "5", 

	"06a_PEASOUP_ZERO_ACC": "6",  # 288 beams 0 acc, multiple DM candidates
	"07a_CANDIDATE_RFI_MATCHING":"7", # multibeam filter -> 1. rfi list 2. isolated pulsar list
	"08a_FOLD_ZERO_ACC":"8", # Pngs generated
	"09a_PICS_SCORER": "9",  # pngs shortlisted
	"10a_CSV_GEN": "10",  # pngs viewed 

	"06b_PEASOUP_ACC": "6",  # 288 beams all acc, multiple DM candidates
	"07b_CANDIDATE_RFI_MATCHING":"7", # multibeam filter -> 1. rfi list 2. isolated pulsar list
	"08b_FOLD_ACC":"8", # Pngs to look
	"09b_PICS_SCORER": "9",  # pngs shortlisted
	"10b_CSV_GEN": "10",  # pngs viewed 


	"06c_PEASOUP_SEGMENT_ACC": "6",  # 288 beams all acc, multiple DM candidates
	"07c_CANDIDATE_RFI_MATCHING":"7", # multibeam filter -> 1. rfi list 2. isolated pulsar list
	"08c_FOLD_ACC":"8", # Pngs to look
	"09c_PICS_SCORER": "9",  # pngs shortlisted
	"10c_CSV_GEN": "10"  # pngs viewed 

}






 