from Log import Logger
import os
import time
import threading
from utis import run_process

class Rsyncer(object):

	""" Daemon thread to check the number of files in the processing directory"""
	def _check_num_processing_files(directory):
		while True:
			if(os.path.exists(directory)):
				self._num_processing_files = len([name for name in os.listdir(directory) if os.path.isdir(os.path.join(directory, name))])
				time.sleep(300)


	def __init__(self, file_locations, beam_list, max_beams_on_processing_disk):
		self.file_locations = file_locations
		self.logger = Logger.getInstance().logger
		self._num_processing_files_checker = threading.Thread(target=_check_num_processing_files, args=(file_locations.processing_path,), daemon=True)
		self._num_processing_files_checker.start()
		self.ledger = Ledger.getInstance()
		self.max_beams_on_processing_disk = max_beams_on_processing_disk

	def from_archive_to_staging():

		for i in beam_list:

			beam_dir_name="cfbf{:05}".format(i)
			inp = "{}:{}".format(file_locations.tape_machine, os.path.join(file_locations.tape_path,beam_dir_name))
			out = "{}:{}".format(file_locations.staging_machine, os.path.join(file_locations.staging_path,beam_dir_name))

			if self.ledger.has_beam(i):
				logger.info("Beam {} is already processed. Skipping rsync from {} to {}").format(beam_dir_name,inp,out)
				continue			

			command = "rsync -aPvz {} {}".format(inp, out)
			logger.info("Transferring beam: {:02d} from {} to {}".format(beam_dir_name,inp,out ))

			run_process(command)

			self.ledger.add_to_ledger(i)


	def from_staging_to_processing():

		while True:

			for i in beam_list:


				if (self.ledger.get_num_running_beams() >= self.max_beams_on_processing_disk):
					break

				beam_dir_name="cfbf{:05}".format(i)
				inp = "{}:{}".format(file_locations.staging_machine, os.path.join(file_locations.staging_path,beam_dir_name))
				out = "{}".format(os.path.join(file_locations.processing_path,beam_dir_name))

				if self.ledger.has_beam(i) and self.ledger.get_status(i) > 1:
					logger.info("Beam {} is already processed. Skipping rsync from {} to {}").format(beam_dir_name,inp,out)
					continue	

				command = "rsync -aPvz {} {}".format(inp, out)
				logger.info("Transferring beam: {:02d} from {} to {}".format(beam_dir_name,inp,out))

		time.sleep(900)



	def transfer_files():

		self._rsync_from_archive_to_staging = threading.Thread(target=from_archive_to_staging, daemon=True)
		self._rsync_from_staging_to_processing = threading.Thread(target=from_staging_to_processing, daemon=True)



		




