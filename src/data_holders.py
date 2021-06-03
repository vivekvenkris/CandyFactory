
class Observation (object):
	def __init__(self, source, nbeam, tobs, band, obs_number):
		self._source = source
		self._nbeam = nbeam
		self._tobs = tobs
		self._band = band
		self._obs_number = obs_number


	@property
	def source():
		return _source

	@property
	def nbeam():
		return _nbeam

	@property
	def tobs():
		return _tobs

	@property
	def tobs():
		return _tobs

	@property
	def band():
		return _band

	@property
	def obs_number():
		return _obs_number

	def generate_prefix(self):
		return "{}_{}{:02d}".format(self._source, self._band, self._obs_number)


if __name__ == '__main__':
	obs = Observation("NGC6441", 288, 4, "L", 1)
	print(obs.generate_prefix())


class FileLocations(object):
	def __init__(self, tape_path, tape_machine, staging_path, staging_machine,  processing_path):
		self._tape_path = tape_path
		self._staging_path = staging_path
		self._processing_path = staging_path
		self._tape_machine = tape_machine
		self._staging_machine = staging_machine

	@property
	def tape_path():
		return _tape_path

	@property
	def staging_path():
		return _staging_path

	@property
	def processing_path():
		return _processing_path

	@property
	def tape_machine():
		return _tape_machine

	@property
	def staging_machine():
		return _staging_machine





class PrestoConfig(object):
	def __init__(self, singularity_image, rfifind_flags, ddplan_flags, accelsearch_flags):

		self._singularity_image = singularity_image
		self._rfifind_flags = rfifind_flags
		self._accelsearch_flags = accelsearch_flags
		self._ddplan_flags = ddplan_flags


	@property
	def singularity_image():
		return _singularity_image

	@property 
	def accelsearch_flags:
		return _accelsearch_flags

	@property 
	def ddplan_flags:
		return _ddplan_flags

	@property 
	def rfifind_flags:
		return _rfifind_flags


class SegmentConfig(object):
	def __init__(self, segment_length, acc_start, acc_end):

		self._segment_list = segment_list
		self._acc_start = acc_start
		self._acc_end = acc_end

	@property
	def segment_length():
		return segment_length

	@property
	def acc_start():
		return _acc_start

	@property
	def acc_end():
		return _acc_end



class PeasoupConfig(object):
	def __init__(self, singularity_image, acc_start, acc_end, segment_configs, start_offset, do_zero_acc_birdies):
		self._singularity_image = singularity_image
		self._segment_list = segment_list
		self._acc_start = acc_start
		self._acc_end = acc_end
		self._start_offset = start_offset
		self._segment_configs = segment_configs
		self._do_zero_acc_birdies = do_zero_acc_birdies

	@property
	def singularity_image():
		return _singularity_image

	@property
	def segment_configs():
		return _segment_configs

	@property
	def acc_start():
		return _acc_start

	@property
	def acc_end():
		return _acc_end

	@property
	def scale_acc_with_segments():
		return _scale_acc_with_segments

	@property
	def do_zero_acc_birdies():
		return _do_zero_acc_birdies



class PulsarXConfig(object):
	def __init__(self, singularity_image, do_zero_dm_filter, pulsarX_flags):
		self._singularity_image = singularity_image		
		self.do_zero_dm_filter = do_zero_dm_filter
		self._pulsarX_flags = pulsarX_flags

	@property
	def singularity_image():
		return _singularity_image

	@property
	def do_zero_dm_filter():
		return _do_zero_dm_filter

	@property
	def pulsarX_flags():
		return _pulsarX_flags	


class SlurmConfig(object):
	def __init__(self, num_simultaneous_jobs, partition, mail_user, mail_type):
		self._num_simultaneous_jobs = num_simultaneous_jobs
		self._partition = partition
		self._mail_type = mail_type
		self._mail_user = mail_user

	@property
	def num_simultaneous_jobs():
		return _num_simultaneous_jobs

	@property
	def partition():
		return _partition

	@property
	def mail_type():
		return _mail_type

	@property
	def mail_user():
		return _mail_user


class Config():
	def __init__(self, file_locations, presto_config, peasoup_config, pulsarX_config, slurm_config, dm_file, beam_list):
		self._file_locations = file_locations
		self._presto_config = presto_config
		self._peasoup_config = peasoup_config
		self._pulsarX_config = pulsarX_config
		self._slurm_config = slurm_config
		self._dm_file = dm_file
		self._beam_list = beam_list


	@property
	def file_locations():
		return _file_locations

	@property
	def presto_config():
		return _presto_config

	@property
	def peasoup_config():
		return _peasoup_config

	@property
	def pulsarX_config():
		return _pulsarX_config

	@property
	def slurm_config():
		return _slurm_config

	@property
	def dm_file():
		return _dm_file

	@property
	def beam_list:
		return _beam_list

