



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




class StatusManager(object):

	__INIT = "0"
	__RSYNC_TO_STAGING = "1"
	__RSYNC_TO_PROCESSING = "2"
	__FILTOOLS = "3"
	__RFIFIND_MASK = "4"
	__ZERO_DM_ACCELSEARCH = "5"

	__PEASOUP_ZERO_ACC = "6"
	__CANDIDATE_RFI_MATCHING = "7"
	__FOLD_ZERO_ACC = "8"
	__PICS_SCORER = "9"
	__CSV_GEN = "10"

	__SEARCH_TYPES = "ZERO_ACC, ACC, SEGMENTED"

	__SEARCH_TYPE_ZERO_ACC = "ZERO_ACC"
	__SEARCH_TYPE_ACC = "ACC"
	__SEARCH_TYPE_SEGMENTED = "SEGMENTED"

	@property
	def INIT(self):
		return __INIT

	@property
	def SEARCH_TYPES(self):
		return __SEARCH_TYPES

	@property
	def RSYNC_TO_STAGING(self):
		return __RSYNC_TO_STAGING
	@property
	def RSYNC_TO_PROCESSING(self):
		return __RSYNC_TO_PROCESSING
	@property
	def FILTOOLS(self):
		return __FILTOOLS
	@property
	def RFIFIND_MASK(self):
		return __RFIFIND_MASK
	@property
	def ZERO_DM_ACCELSEARCH(self):
		return __ZERO_DM_ACCELSEARCH
	@property
	def PEASOUP_ZERO_ACC(self):
		return __PEASOUP_ZERO_ACC
	@property
	def CANDIDATE_RFI_MATCHING(self):
		return __CANDIDATE_RFI_MATCHING
	@property
	def FOLD_ZERO_ACC(self):
		return __FOLD_ZERO_ACC
	@property
	def PICS_SCORER(self):
		return __PICS_SCORER
	@property
	def CSV_GEN(self):
		return __CSV_GEN 

	@property
	def SEARCH_TYPE_SEGMENTED(self):
		return self.__SEARCH_TYPE_ZERO_ACC
	
	@property
	def SEARCH_TYPE_ACC(self):
		return self.__SEARCH_TYPE_ACC
	
	@property
	def SEARCH_TYPE_SEGMENTED(self):
		return self.__SEARCH_TYPE_SEGMENTED
	


	




 