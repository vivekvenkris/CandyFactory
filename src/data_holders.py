
class Observation (object):
	def __init__(self, source, nbeams, tobs, band, obs_number):
		self.__source = source
		self.__nbeams = nbeams
		self.__tobs = tobs
		self.__band = band
		self.__obs_number = obs_number


	@property
	def source(self):
		return self.__source

	@property
	def nbeams(self):
		return self.__nbeams

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
	def __init__(self, tape_path, tape_machine, staging_path,  processing_path):
		self.__tape_path = tape_path
		self.__staging_path = staging_path
		self.__processing_path = processing_path
		self.__tape_machine = tape_machine

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



	def __str__(self):
		return "tape_path {} \n tape_machine {} \n staging_path {} \n   processing_path {} \n".format(self.tape_path, self.tape_machine, self.staging_path, 
											  self.processing_path)

	def __repr__(self):
		return self.__str__()


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
		return self.__str__()

class SegmentConfig(object):
	def __init__(self, fractional_segment_length, acc_start, acc_end):

		self.__fractional_segment_length = fractional_segment_length # 0 to 1
		self.__acc_start = acc_start
		self.__acc_end = acc_end

	@property
	def fractional_segment_length(self):
		return self.__fractional_segment_length

	@property
	def acc_start(self):
		return self.__acc_start

	@property
	def acc_end(self):
		return self.__acc_end

	def __str__(self):
		return "fractional_segment_length: {} \n acc_start: {} \n acc_end: {} \n".format(self.fractional_segment_length, self.acc_start, self.acc_end)

	def __repr__(self):
		return self.__str__()



class PulsarXConfig(object):
	def __init__(self, singularity_image, singularity_flags, do_zero_dm_filter, pulsarX_flags):
		self.__singularity_image = singularity_image		
		self.__do_zero_dm_filter = do_zero_dm_filter
		self.__pulsarX_flags = pulsarX_flags
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
	def singularity_flags(self):
		return self.__singularity_flags

	def __str__(self):
		return "singularity_image: {} \n singularity_flags: {} \n do_zero_dm_filter: {} \n pulsarX_flags: {} \n fast_nbin: {} \n slow_nbin: {} \n".format(self.singularity_image, self.singularity_flags, self.do_zero_dm_filter, self.pulsarX_flags, self.fast_nbin, self.slow_nbin)

	def __repr__(self):
		return self.__str__()

class PeasoupConfig(object):
	def __init__(self, singularity_image, singularity_flags, segment_configs, start_fraction, end_fraction, do_zero_acc_birdies, peasoup_flags):
		self.__singularity_image = singularity_image
		self.__segment_configs = segment_configs
		self.__start_fraction = start_fraction
		self.__segment_configs = segment_configs
		self.__do_zero_acc_birdies = do_zero_acc_birdies
		self.__peasoup_flags = peasoup_flags
		self.__singularity_flags = singularity_flags
		self.__end_fraction = end_fraction

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
	def start_fraction(self):
		return self.__start_fraction

	@property
	def end_fraction(self):
		return self.__end_fraction

	@property
	def peasoup_flags(self):
		return self.__peasoup_flags

	@property
	def singularity_flags(self):
		return self.__singularity_flags
	
	def __str__(self):
		return "singularity_image: {} \n singularity_flags: {} \n segment_configs: {} \n start_fraction: {} \n end_fraction: {} \n do_zero_acc_birdies: {} \n peasoup_flags: {} \n".format(self.singularity_image, self.singularity_flags, self.segment_configs, self.start_fraction, self.end_fraction, self.do_zero_acc_birdies, self.peasoup_flags)

	def __repr__(self):
		return self.__str__()

class BirdieMatcherConfig(object):
	def __init__(self,period_tolerance, matcher_harmonics):
		self.__period_tol = period_tolerance
		self.__harmonics = matcher_harmonics;

	@property
	def period_tol(self):
		return self.__period_tol

	@property
	def harmonics(self):
		return self.__harmonics

class SlurmConfig(object):
	def __init__(self, num_simultaneous_jobs, short_cpu_partition, long_cpu_partition, gpu_partition, mail_user, mail_type):
		self.__num_simultaneous_jobs = num_simultaneous_jobs
		self.__long_cpu_partition = long_cpu_partition
		self.__short_cpu_partition = short_cpu_partition
		self.__gpu_partition = gpu_partition
		self.__mail_type = mail_type
		self.__mail_user = mail_user

	@property
	def num_simultaneous_jobs(self):
		return self.__num_simultaneous_jobs

	@property
	def long_cpu_partition(self):
		return self.__long_cpu_partition

	@property
	def short_cpu_partition(self):
		return self.__short_cpu_partition

	@property
	def gpu_partition(self):
		return self.__gpu_partition	


	@property
	def mail_type(self):
		return self.__mail_type

	@property
	def mail_user(self):
		return self.__mail_user

	def __str__(self):
		return " num_simultaneous_jobs {} \n partition {} \n mail_user {}  \n mail_type {} \n".format(self.num_simultaneous_jobs, self.partition, self.mail_user, self.mail_type)

	def __repr__(self):
		return self.__str__()

class Config(object):
	def __init__(self, root_output_dir, observations, file_locations, presto_config, peasoup_config, birdie_matcher_config, pulsarX_config, slurm_config, dm_file, beam_list, max_beams_on_processing_disk):
		self.__observations = observations
		self.__root_output_dir = root_output_dir
		self.__file_locations = file_locations
		self.__presto_config = presto_config
		self.__peasoup_config = peasoup_config
		self.__pulsarX_config = pulsarX_config
		self.__slurm_config = slurm_config
		self.__dm_file = dm_file
		self.__beam_list = beam_list
		self.__max_beams_on_processing_disk = max_beams_on_processing_disk
		self.__birdie_matcher_config = birdie_matcher_config

	@property
	def observations(self):
		return self.__observations
	@property
	def file_locations(self):
		return self.__file_locations
		
	@property
	def root_output_dir(self):
		return self.__root_output_dir

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
	def birdie_matcher_config(self):
		return self.__birdie_matcher_config

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
		return "\n Configurations: \n Observations: {} \n File locations: {} Presto config: {} \n PulsarX config: {} \n,  Peasoup config: {} \n Slurm config: {} \n dm_file: {} \n beam_list: {} \n \
			max_beams_on_processing_disk: {}".format(self.observations, self.file_locations,self.presto_config, self.pulsarX_config, self.peasoup_config, self.slurm_config, self.dm_file, self.beam_list, self.max_beams_on_processing_disk)

	def __repr__(self):
		return self.__str__()
