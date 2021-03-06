from data_holders import *
from  gen_utils import ensure_file_exists, strip_quotes_and_spaces, guess_and_change_dtype
from shutil import copyfile
import os
from pathlib import Path

# Fixed definitions or paths  
PULSARX_TEMPLATE = "/home/psr/software/PulsarX/include/template/meerkat_fold.template"


class ConfigurationReader(object):

    @staticmethod
    def init_default():
        cwd = os.getcwd()
        dest = os.path.join(cwd, "default.cfg")
        file_path=Path(__file__)
        src = os.path.join(file_path.parent.parent, "defaults", "config_file")
        line = None
        with open(src) as f:
            line = f.read().replace("<ROOT_OUTPUT_DIR>", os.path.abspath(cwd))

        with open(dest, "w") as f:
            f.write(line)


    def get_value_if_exists(self, flag, value):
        return "{} {} ".format(flag, value) if value != "" else ""



    def generate_ddplan_flags(self):

         return "-l {} -d {} -c {} -s {}".format(self.dict_process_config['DM_MIN'], self.dict_process_config['DM_MAX'], self.dict_process_config['COHERENT_DM'], self.dict_process_config['N_SUBBANDS'])  

     
    def generate_rfifind_flags(self):
        zapint_flag = self.get_value_if_exists("-zapints", self.dict_process_config['RFIFIND_TIME_INTERVALS_TO_ZAP'])
        chanzap_flag = self.get_value_if_exists("-zapchan", self.dict_process_config['RFIFIND_CHANS_TO_ZAP'])
        time_stats_flag = self.get_value_if_exists("-time",self.dict_process_config['RFIFIND_TIME']) 
        ignorechan_flag = self.get_value_if_exists("-ignorechan", self.dict_process_config['IGNORECHAN_LIST'])
        timesig_flag = self.get_value_if_exists("-timesig", self.dict_process_config['RFIFIND_TIMESIG'])
        freqsig_flag = self.get_value_if_exists("-freqsig", self.dict_process_config['RFIFIND_FREQSIG'])

        return zapint_flag + chanzap_flag + time_stats_flag + ignorechan_flag +timesig_flag + freqsig_flag
          
    def generate_accelsearch_flags(self):
        accelsearch_flags = strip_quotes_and_spaces(self.dict_process_config['ACCELSEARCH_FLAGS'])

        if "zmax" in accelsearch_flags or "wmax" in accelsearch_flags or "ncpus" in accelsearch_flags:
            raise Exception("You have specified zmax, wmax or ncpus which is already fixed.") 

        return  accelsearch_flags


    def get_acc_range_and_segment_fraction(self):
        seg_configs = []
        for i in self.dict_process_config['ACC_SEGMENT_LIST'].strip().split(","):
            acc_start, acc_end, seg_length = i.strip().split(":")
            seg_length = 1 if "full" in seg_length else float(seg_length)
            seg_config = SegmentConfig(seg_length, float(acc_start), float(acc_end))
            seg_configs.append(seg_config)

        return seg_configs
          


    def __init__(self, config_filename):
        self._config_filename = config_filename
        self.dict_process_config={}

        ensure_file_exists(config_filename)

        config_file = open( config_filename, "r" )

        lines = None

        with open( config_filename, "r" ) as f:
            lines =  f.read().splitlines()

        for line in lines:

            if not line or line.startswith("#"):
                continue;
                
            chunks = line.split('#')[0].strip().split(None,1)
            key = chunks[0]
            val = guess_and_change_dtype(strip_quotes_and_spaces(chunks[1])) if len(chunks) > 1 else ""

            self.dict_process_config[key] = val  #Save parameter key and value in the dictionary 
              
        config_file.close()
     
        
        singularity_flags = "-B {}:{} -B {}:{}".format(self.dict_process_config['PROCESSING_PATH'], 
                                                    self.dict_process_config['PROCESSING_PATH'],
                                                    self.dict_process_config['ROOT'],
                                                    self.dict_process_config['ROOT'])

        pulsarX_flags = " -L {} -n {} -nbinplan {} {}".format(self.dict_process_config['NSUBINT_FOLD'],
                                                    self.dict_process_config['NCHAN_FOLD'],
                                                    self.dict_process_config['ADDITIONAL_PULSARX_FLAGS'],
                                                    self.dict_process_config['NBIN_PLAN'])


        all_segment_configs = self.get_acc_range_and_segment_fraction()


        observations =  Observation(self.dict_process_config['SOURCE'],
                                 self.dict_process_config['NBEAMS'], 
                                 self.dict_process_config['TOBS'], 
                                 self.dict_process_config['BAND'], 
                                 self.dict_process_config['OBS_NO']) 
   

        presto_config = PrestoConfig(self.dict_process_config['PRESTO_IMAGE'], 
                                  singularity_flags,  
                                  self.generate_rfifind_flags(),
                                  self.generate_ddplan_flags(),
                                  self.generate_accelsearch_flags())  

        peasoup_config = PeasoupConfig(self.dict_process_config['PEASOUP_IMAGE'], 
                                    singularity_flags,
                                    all_segment_configs,
                                    self.dict_process_config['START_FRACTION'],
                                    self.dict_process_config['END_FRACTION'],
                                    self.dict_process_config['ACCELSEARCH_BIRDIES'], 
                                    self.dict_process_config['PEASOUP_FLAGS']
                                    ) 

        filelocations = FileLocations(self.dict_process_config['TAPE_PATH'],
                                   self.dict_process_config['TAPE_MACHINE'],  
                                   self.dict_process_config['STAGING_PATH'], 
                                   self.dict_process_config['PROCESSING_PATH'] 
                                   ) 


        pulsarX_config =  PulsarXConfig( self.dict_process_config['PULSARX_IMAGE'],
                                     singularity_flags,
                                     self.dict_process_config['PULSARX_ZERODM_MATCHED_FILTER'],
                                     pulsarX_flags)


        birdie_matcher_config = BirdieMatcherConfig(self.dict_process_config['MATCHER_PERIOD_TOLERANCE'],self.dict_process_config['MATCHER_HARMONICS'])

    

        slurm_config =SlurmConfig(self.dict_process_config['N_SIMULTANEOUS_JOBS'],
                                  self.dict_process_config['SHORT_CPU_PARTITION'],
                                  self.dict_process_config['LONG_CPU_PARTITION'],
                                  self.dict_process_config['GPU_PARTITION'],
                                  self.dict_process_config['MAIL_USER'],
                                  self.dict_process_config['MAIL_TYPE']) 

        beam_list = None if self.dict_process_config['BEAM_LIST'] == "" else self.dict_process_config['BEAM_LIST'].split(",")
                           

        self.__config =  Config(self.dict_process_config['ROOT'], observations, filelocations, presto_config, peasoup_config, birdie_matcher_config, pulsarX_config, slurm_config, self.dict_process_config['DM_FILE'], 
            beam_list, int(self.dict_process_config['MAX_BEAMS_ON_PROCESSING_DISK']))
  
    @property
    def config(self):
        return self.__config;


 

     


if __name__=="__main__":
    config = ConfigurationReader("../defaults/config_file").config 

    print(config.birdie_matcher_config.period_tol)

     
