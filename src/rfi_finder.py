from gen_utils import run_with_singularity
from status_manager import StatusManager
from search_operations import SearchOperations
from ledger import Ledger
import glob
import os

import re
class RfiFinder(SearchOperations):

	def __init__(self, config, out_prefix):
		super().__init__(config, out_prefix)

	def do_accelsearch(self, input_file, beam_name):

		prepdata_outfile_prefix = "{}_{}_DM0.00".format(self.out_prefix, beam_name)

		prepdata_cmd = "prepdata -dm 0 -nobary -o {} {}".format(prepdata_outfile_prefix, input_file)

		run_with_singularity(self.config.presto_config.singularity_image, 
						self.config.presto_config.singularity_flags, prepdata_cmd)


		realfft_cmd = "realfft {}.dat".format(prepdata_outfile_prefix)

		run_with_singularity(self.config.presto_config.singularity_image, 
						self.config.presto_config.singularity_flags, realfft_cmd )


		accelsearch_command = "accelsearch {} -zmax 0 -numharm 8 {}.fft".format(self.config.presto_config.accelsearch_flags, prepdata_outfile_prefix)

		run_with_singularity(self.config.presto_config.singularity_image, 
						self.config.presto_config.singularity_flags, accelsearch_command)


	def run_rfifind(self, input_file, beam_name):

		rfifind_cmd = "rfifind -o {}_{} {} {}".format(self.out_prefix, beam_name, self.config.presto_config.rfifind_flags, input_file)

		run_with_singularity(self.config.presto_config.singularity_image, 
						self.config.presto_config.singularity_flags, rfifind_cmd)



	def run_filtool(self, input_file, beam_name):
		beam_num = int(re.findall('\\d+', beam_name)[0])
		filtools_cmd ="filtool -t 16  -z kadaneF 8 4 zdot -i {} -telescope Meerkat -o {}_{} -f {}".format(beam_num, self.out_prefix,beam_name, input_file)
		run_with_singularity(self.config.pulsarX_config.singularity_image, 
	 					self.config.pulsarX_config.singularity_flags,filtools_cmd)



	def make_birds_file(self, ACCEL_0_filename, width_Hz, flag_grow=1, sigma_birdies_threshold=4):
		infile_nameonly = os.path.basename(ACCEL_0_filename)
		infile_basename = infile_nameonly.replace("_ACCEL_0", "")
		birds_filename = ACCEL_0_filename.replace("_ACCEL_0", ".birds")


		#Skip first three lines

		print ("make_birds_file:: Opening the candidates: %s") % (ACCEL_0_filename)
		candidate_birdies = sifting.candlist_from_candfile(ACCEL_0_filename)
		candidate_birdies.reject_threshold(sigma_birdies_threshold)

		#Write down candidates above a certain sigma threshold
		list_birdies = candidate_birdies.cands

		print ("make_birds_file:: Number of birdies = %d") % (len(list_birdies))
		file_birdies = open(birds_filename, "w")
		print ("make_birds_file:: File_birdies: %s") % (birds_filename)

		for cand in list_birdies:
		        file_birdies.write("%.3f     %.20f \n" % (cand.f, width_Hz)  )
		file_birdies.close()

		return birds_filename	




	def find_rfi(self, beam_name):

		file_name = glob.glob(os.path.join(self.config.file_locations.processing_path, beam_name)+ "/*.fil")[0]
		self.run_filtool(file_name, beam_name)
		self.ledger.update_status(beam_name, self.status_manager.FILTOOLS)

		self.run_rfifind(file_name, beam_name)
		self.ledger.update_status(beam_name, self.status_manager.RFIFIND_MASK)


		self.do_accelsearch(file_name, beam_name)
		self.ledger.update_status(beam_name, self.status_manager.ZERO_DM_ACCELSEARCH)


	def run(self, beam_name, search_type):
	    self.find_rfi(self, beam_name)


			



		

