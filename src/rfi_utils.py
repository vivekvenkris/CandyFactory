from utils import run_with_singularity
from constants import STATUS_DICT
from ledger import Ledger

Class RFIUtils(Object):

	def __init__(config, out_prefix, ledger):
		self.config = config
		self.out_prefix = prefix
		self.ledger = Ledger.getInstance()


	def do_accelsearch(input_file, beam_num):

		prepdata_cmd = "prepdata -dm 0 -nobary -o {}_{:02d}_DM0 {}".format(out_prefix, beam_num, input_file)

		run_with_singularity(self.config.presto_config.singularity_image, 
						self.presto_config.singularity_flags, prepdata_cmd)


		realfft_cmd = "realfft {}".format(infile)

		run_with_singularity(self.config.presto_config.singularity_image, 
						self.presto_config.singularity_flags, realfft_cmd )


		accelsearch_command = "accelsearch %s -zmax 0 -numharm 8 %s" % (self.presto_config.accelsearch_flags, input_file)

		run_with_singularity(self.config.presto_config.singularity_image, 
						self.presto_config.singularity_flags, accelsearch_command)


	def run_rfifind(input_file, beam_num):

		rfifind_cmd = "rfifind -o {} {} {}".format(prefix, self.presto_config.rfifind_flags, input_file)

		run_with_singularity(self.config.presto_config.singularity_image, 
						self.presto_config.singularity_flags, rfifind_cmd)



	def run_filtool(input_file, beam_num):
		ledger.update_status(STATUS_DICT["03_ZERO_DM_FILTER"])
	 	filtools_cmd ="filtool -t 16  -z kadaneF 8 4 zdot -i {} -telescope Meerkat -o {} -f {}".format(beam_num, prefix, input_file)

	 	run_with_singularity(self.config.pulsarX_config.singularity_image, 
	 					self.config.pulsarX_config.singularity_flags,filtools_cmd)



	def make_birds_file(ACCEL_0_filename, width_Hz, flag_grow=1, sigma_birdies_threshold=4):
		infile_nameonly = os.path.basename(ACCEL_0_filename)
		infile_basename = infile_nameonly.replace("_ACCEL_0", "")
		birds_filename = ACCEL_0_filename.replace("_ACCEL_0", ".birds")


		#Skip first three lines

		print "make_birds_file:: Opening the candidates: %s" % (ACCEL_0_filename)
		candidate_birdies = sifting.candlist_from_candfile(ACCEL_0_filename)
		candidate_birdies.reject_threshold(sigma_birdies_threshold)

		#Write down candidates above a certain sigma threshold
		list_birdies = candidate_birdies.cands

		print "make_birds_file:: Number of birdies = %d" % (len(list_birdies))
		file_birdies = open(birds_filename, "w")
		print "make_birds_file:: File_birdies: %s" % (birds_filename)

		for cand in list_birdies:
		        file_birdies.write("%.3f     %.20f \n" % (cand.f, width_Hz)  )
		file_birdies.close()

		return birds_filename	






