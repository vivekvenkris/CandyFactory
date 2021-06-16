
class Observation (object):
	def __init__(self, source, nbeam, tobs, band, obs_number):
		self.___source = source
		self.__nbeam = nbeam
		self.__tobs = tobs
		self.__band = band
		self.__obs_number = obs_number


	@property
	def source(self):
		return self.__source

	@property
	def nbeam(self):
		return self.__nbeam

	@property
	def tobs(self):
		return self.__tobs

	@property
	def tobs(self):
		return self.__tobs

	@property
	def band(self):
		return self.__band

	@property
	def obs_number(self):
		return self.__obs_number

	def generate_prefix(self):
		return "{}_{}{:02d}".format(self.__source, self.__band, self.__obs_number)


if __name__ == '__main__':
	obs = Observation("NGC6441", 288, 4, "L", 1)
	print(obs.generate_prefix())


class FileLocations(object):
	def __init__(self, tape_path, tape_machine, staging_path, staging_machine,  processing_path):
		self.__tape_path = tape_path
		self.__staging_path = staging_path
		self.__processing_path = staging_path
		self.__tape_machine = tape_machine
		self.__staging_machine = staging_machine

	@property
	def tape_path(self):
		return self.__tape_path

	@property
	def staging_path(self):
		return self.__staging_path

	@property
	def processing_path(self):
		return self.__processing_path

	@property
	def tape_machine(self):
		return self.__tape_machine

	@property
	def staging_machine(self):
		return self.__staging_machine

	def __str__(self):
		return "tape_path {} \n tape_machine {} \n staging_path {} \n staging_machine {} \n  processing_path {} \n".format(self.tape_path, self.tape_machine, self.staging_path, 
											self.staging_machine,  self.processing_path)

	def __repr__(self):
		return __str__()


class PrestoConfig(object):
	def __init__(self, singularity_image, singularity_flags, rfifind_flags, ddplan_flags, accelsearch_flags):

		self.__singularity_image = singularity_image
		self.__rfifind_flags = rfifind_flags
		self.__accelsearch_flags = accelsearch_flags
		self.__ddplan_flags = ddplan_flags
		self.__singularity_flags = singularity_flags


	@property
	def singularity_image(self):
		return self.__singularity_image

	@property 
	def accelsearch_flags(self):
		return self.__accelsearch_flags

	@property 
	def ddplan_flags(self):
		return self.__ddplan_flags

	@property 
	def rfifind_flags(self):
		return self.__rfifind_flags

	@property
	def singularity_flags(self):
		return self.__singularity_flags

	def __str__(self):
		return "singularity_image: {} \n singularity_flags: {} \n rfifind_flags: {} \n ddplan_flags: {} \n accelsearch_flags".format(self.singularity_image, self.singularity_flags, self.rfifind_flags, self.ddplan_flags, self.accelsearch_flags)

	def __repr__(self):
		return __str__()

class SegmentConfig(object):
	def __init__(self, fractional_segment_length, acc_start, acc_end):

		self.__fractional_segment_length = fractional_segment_length # 0 to 1
		self.__acc_start = acc_start
		self.__acc_end = acc_end

	@property
	def fractional_segment_length(self):
		return __fractional_segment_length

	@property
	def acc_start(self):
		return self.__acc_start

	@property
	def acc_end(self):
		return self.__acc_end

	def __str__(self):
		return "fractional_segment_length: {} \n acc_start: {} \n acc_end: {} \n".format(self.fractional_segment_length, self.acc_start, self.acc_end)

	def __repr__(self):
		return __str__()

class PeasoupConfig(object):
	def __init__(self, singularity_image, singularity_flags, segment_configs, start_offset, end_offset, do_zero_acc_birdies, peasoup_flags):
		self.__singularity_image = singularity_image
		self.__segment_configs = segment_configs
		self.__start_offset = start_offset
		self.__segment_configs = segment_configs
		self.__do_zero_acc_birdies = do_zero_acc_birdies
		self.__peasoup_flags = peasoup_flags
		self.__singularity_flags = singularity_flags
		self.__end_offset = end_offset

	@property
	def singularity_image(self):
		return self.__singularity_image

	@property
	def segment_configs(self):
		return self.__segment_configs

	@property
	def do_zero_acc_birdies(self):
		return self.__do_zero_acc_birdies

	@property
	def start_offset(self):
		return self.__start_offset

	@property
	def end_offset(self):
		return self.__end_offset

	@property
	def peasoup_flags(self):
		return self.__peasoup_flags

	@property
	def singularity_flags(self):
		return self.__singularity_flags
	
	def __str__(self):
		return "singularity_image: {} \n singularity_flags: {} \n segment_configs: {} \n start_offset: {} \n end_offset: {} \n do_zero_acc_birdies: {} \n peasoup_flags: {} \n".format(self.singularity_image, self.singularity_flags, self.segment_configs, self.start_offset, self.end_offset, self.do_zero_acc_birdies, self.peasoup_flags)

	def __repr__(self):
		return __str__()

class PulsarXConfig(object):
	def __init__(self, singularity_image, singularity_flags, do_zero_dm_filter, pulsarX_flags, fast_nbin, slow_nbin):
		self.__singularity_image = singularity_image		
		self.__do_zero_dm_filter = do_zero_dm_filter
		self.__pulsarX_flags = pulsarX_flags
		self.__fast_nbin = fast_nbin
		self.__slow_nbin = slow_nbin
		self.__singularity_flags = singularity_flags

	@property
	def singularity_image(self):
		return self.__singularity_image

	@property
	def do_zero_dm_filter(self):
		return self.__do_zero_dm_filter

	@property
	def pulsarX_flags(self):
		return self.__pulsarX_flags	

	@property
	def fast_nbin(self):
		return self.__fast_nbin

	@property
	def slow_nbin(self):
		return self.__slow_nbin

	@property
	def singularity_flags(self):
		return self.__singularity_flags

	def __str__(self):
		return "singularity_image: {} \n singularity_flags: {} \n do_zero_dm_filter: {} \n pulsarX_flags: {} \n fast_nbin: {} \n slow_nbin: {} \n".format(self.singularity_image, self.singularity_flags, self.do_zero_dm_filter, self.pulsarX_flags, self.fast_nbin, self.slow_nbin)

	def __repr__(self):
		return __str__()

class SlurmConfig(object):
	def __init__(self, num_simultaneous_jobs, partition, mail_user, mail_type):
		self.__num_simultaneous_jobs = num_simultaneous_jobs
		self.__partition = partition
		self.__mail_type = mail_type
		self.__mail_user = mail_user

	@property
	def num_simultaneous_jobs(self):
		return self.__num_simultaneous_jobs

	@property
	def partition(self):
		return self.__partition

	@property
	def mail_type(self):
		return self.__mail_type

	@property
	def mail_user(self):
		return self.__mail_user

	def __str__(self):
		return " num_simultaneous_jobs {} \n partition {} \n mail_user {}  \n mail_type {} \n".format(self.num_simultaneous_jobs, self.partition, self.mail_user, self.mail_type)

	def __repr__(self):
		return __str__()

class Config(object):
	def __init__(self, file_locations, presto_config, peasoup_config, pulsarX_config, slurm_config, dm_file, beam_list, max_beams_on_processing_disk):
		self.__file_locations = file_locations
		self.__presto_config = presto_config
		self.__peasoup_config = peasoup_config
		self.__pulsarX_config = pulsarX_config
		self.__slurm_config = slurm_config
		self.__dm_file = dm_file
		self.__beam_list = beam_list
		self.__max_beams_on_processing_disk = max_beams_on_processing_disk


	@property
	def file_locations(self):
		return self.__file_locations

	@property
	def presto_config(self):
		return self.__presto_config

	@property
	def peasoup_config(self):
		return self.__peasoup_config

	@property
	def pulsarX_config(self):
		return self.__pulsarX_config

	@property
	def slurm_config(self):
		return self.__slurm_config

	@property
	def dm_file(self):
		return self.__dm_file

	@property
	def beam_list(self):
		return self.__beam_list

	@property
	def max_beams_on_processing_disk(self):
		return self.__max_beams_on_processing_disk;


	def __str__(self):
		return "\n Configurations: \n File locations: {} Presto config: {} \n PulsarX config: {} \n, Slurm config: {} \n dm_file: {} \n beam_list: {} \n \
			max_beams_on_processing_disk: {}".format(self.file_locations,self.presto_config, self.peasoup_config, self.pulsarX_config, self.slurm_config, self.dm_file, self.beam_list, self.max_beams_on_processing_disk)

	def __repr__(self):
		return __str__()
