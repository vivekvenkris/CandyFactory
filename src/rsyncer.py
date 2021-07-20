from log import Logger, init_logging
import os
import time
import threading
from gen_utils import run_process
from constants import STATUS_DICT, StatusManager
from ledger import Ledger
import pathlib
class Rsyncer(object):

	""" Daemon thread to check the number of files in the processing directory"""
	def check_num_processing_files(self, directory):
		while True:
			if(os.path.exists(directory)):
				self._num_processing_files = len([name for name in os.listdir(directory) if os.path.isdir(os.path.join(directory, name))])
				time.sleep(300)


	def __init__(self, file_locations, beam_list, max_beams_on_processing_disk):
		self.logger = Logger.getInstance().logger
		self.ledger = Ledger.getInstance()
		self.status_manager = StatusManager.getInstance()


		self.file_locations = file_locations
		self._num_processing_files_checker = threading.Thread(target=self.check_num_processing_files, args=(file_locations.processing_path,), daemon=True)
		self._num_processing_files_checker.start()
		self.max_beams_on_processing_disk = max_beams_on_processing_disk
		self.beam_list = beam_list
		self.logger.debug("Rsyncer init done")

	def get_rsync_string(self, machine, path):
		if("localhost" in machine or "127.0.0.1" in machine):
			inp_machine = ""
		else:
			inp_machine = "{}:".format(machine)
		rsync_str = "{}{}".format(inp_machine, path)
		return rsync_str



	def from_archive_to_staging(self):
		self.logger.info(" from_archive_to_staging daemon started")

		for i in self.beam_list:

			beam_dir_name="cfbf{:05d}".format(int(i))

			inp = self.get_rsync_string(self.file_locations.tape_machine, os.path.join(self.file_locations.tape_path,beam_dir_name))
			out = self.get_rsync_string("localhost", self.file_locations.staging_path)			

			if self.ledger.has_beam(beam_dir_name):
				self.logger.info("Beam {} is already processed. Skipping rsync from {} to {}".format(beam_dir_name,inp,out))
				continue			

			
			if(self.file_locations.tape_path == self.file_locations.staging_path) and (self.tape_machine == self.staging_machine):
				self.logger.info("Tape Path: {} is the same as staging path: {}, skipping").format(self.file_locations.tape_path,self.file_locations.staging_path)

			else:


				command = "rsync -aPvz {} {}".format(inp, out)
				self.logger.info("Transferring beam: {} from {} to {}".format(beam_dir_name,inp,out ))

				run_process(command)

			self.ledger.add_to_ledger(beam_dir_name)

		self.logger.info(" from_archive_to_staging daemon ended")





	def from_staging_to_processing(self):
		self.logger.info(" from_staging_to_processing daemon started")


		if(self.file_locations.staging_path == self.file_locations.processing_path):
			self.logger.info("Staging Path: {} is the same as processing path: {}, skipping".format(self.file_locations.tape_path,self.file_locations.processing_path))
			return

		while True:

			for i in self.beam_list:
				beam_dir_name="cfbf{:05d}".format(int(i))


				if (self.ledger.get_num_running_beams() >= self.max_beams_on_processing_disk):
					self.logger.info("Number of running beams reached threshold, sleeping for a while")
					break

				if not self.ledger.has_beam(beam_dir_name):
					self.logger.info("Beam {} not in ledger, skipping".format(beam_dir_name))
					break

				inp = self.get_rsync_string("localhost", os.path.join(self.file_locations.staging_path,beam_dir_name))
				out = self.get_rsync_string("localhost", self.file_locations.processing_path)
			

				if self.ledger.has_beam(beam_dir_name) and self.ledger.get_status(beam_dir_name) > self.status_manager.RSYNC_TO_STAGING:
					self.logger.info("Beam {} is already processed. Skipping rsync from {} to {}".format(beam_dir_name,inp,out))
					continue	
				if(self.file_locations.staging_path == self.file_locations.processing_path):
					self.logger.info("Staging Path: {} is the same as processing path: {}, skipping").format(self.file_locations.tape_path,self.file_locations.processing_path)
					self.ledger.update_status(beam_dir_name, self.status_manager.RSYNC_TO_PROCESSING)
					continue

				command = "rsync -aPvz {} {}".format(inp, out)
				run_process(command)

				self.logger.info("Transferring beam: {} from {} to {}".format(beam_dir_name,inp,out))
				self.ledger.update_status(beam_dir_name, self.status_manager.RSYNC_TO_PROCESSING)


			self.logger.info("Sleeping for 900 seconds")
			time.sleep(10)
		self.logger.info(" from_staging_to_processing daemon ended")




	def transfer_files(self):
		pathlib.Path(self.file_locations.staging_path).mkdir(parents=True, exist_ok=True)
		pathlib.Path(self.file_locations.processing_path).mkdir(parents=True, exist_ok=True)

		self._rsync_from_archive_to_staging = threading.Thread(target=self.from_archive_to_staging, daemon=True)
		self._rsync_from_staging_to_processing = threading.Thread(target=self.from_staging_to_processing, daemon=True)
		self._rsync_from_archive_to_staging.start()
		self._rsync_from_staging_to_processing.start()

		




