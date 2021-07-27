from abc import ABCMeta,abstractmethod
from ledger import Ledger
from log import Logger
from status_manager import StatusManager
class SearchOperations(metaclass = ABCMeta):

	def __init__(self, config, out_prefix):
		self.config = config
		self.out_prefix = "" #out_prefix if out_prefix == "" or not out_prefix.endswith("_") else out_prefix+"_"

		self.ledger = Ledger.getInstance()
		self.status_manager = StatusManager.getInstance()
		self.logger = Logger.getInstance().logger		

	@abstractmethod
	def run(self, beam_name, search_type="DEF"):
		pass


