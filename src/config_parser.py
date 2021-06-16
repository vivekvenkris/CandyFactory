from data_holders import *
from  gen_utils import ensure_file_exists
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
            line = f.read().replace("<ROOT_OUTPUT_DIR>", os.path.basename(cwd))

        with open(dest, "w") as f:
            f.write(line)


    def get_value_if_exists(self, flag, value):
        return flag +" "+ value if value.strip("\\s+") != "" else ""


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
        accelsearch_flags = self.dict_process_config['ACCELSEARCH_FLAGS'] 

        if "zmax" in accelsearch_flags or "wmax" in accelsearch_flags or "ncpus" in accelsearch_flags:
            raise Exception("You have specified zmax, wmax or ncpus which is already fixed.") 


        return  accelsearch_flags


    def get_acc_range_and_segment_fraction(self):
        seg_configs = []
        for i in self.dict_process_config['ACC_SEGMENT_LIST'].strip().split(","):
            acc_start, acc_end, seg_length = i.strip().split(":")
            seg_length = 1 if "full" in seg_length else seg_length
            seg_config = SegmentConfig(seg_length, acc_start, acc_end)
            seg_configs.append(seg_config)

        return seg_configs
          


    def __init__(self, config_filename):
        self._config_filename = config_filename
        self.dict_process_config={}

        ensure_file_exists(config_filename)

        config_file = open( config_filename, "r" )

        for line in config_file:
            if line != "\n" and (not line.startswith("#")):
                chunks = line.split('#')[0].split(None,1)
                key = chunks[0]
                val = chunks[1] if len(chunks) > 1 else ""
                self.dict_process_config[key] = val      #Save parameter key and value in the dictionary 
              
        config_file.close()
     
        
        singularity_flags = "-B {}:{} -B {}:{}".format(self.dict_process_config['PROCESSING_PATH'], 
                                                    self.dict_process_config['PROCESSING_PATH'],
                                                    self.dict_process_config['ROOT'],
                                                    self.dict_process_config['ROOT'])

        pulsarX_flags = " -L {} -n {} {}".format(self.dict_process_config['NSUBINT_FOLD'],
                                                    self.dict_process_config['NCHAN_FOLD'],
                                                    self.dict_process_config['ADDITIONAL_PULSARX_FLAGS'] )


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
                                    self.dict_process_config['START_OFFSET'],
                                    self.dict_process_config['END_OFFSET'],
                                    self.dict_process_config['ACCELSEARCH_BIRDIES'], 
                                    self.dict_process_config['PEASOUP_FLAGS']
                                    ) 

        filelocations = FileLocations(self.dict_process_config['TAPE_PATH'],
                                   self.dict_process_config['TAPE_MACHINE'],  
                                   self.dict_process_config['STAGING_PATH'], 
                                   self.dict_process_config['STAGING_MACHINE'],
                                   self.dict_process_config['PROCESSING_PATH'] 
                                   ) 


        pulsarX_config =  PulsarXConfig( self.dict_process_config['PULSARX_IMAGE'],
                                     singularity_flags,
                                     self.dict_process_config['PULSARX_ZERODM_MATCHED_FILTER'],
                                     pulsarX_flags, 
                                     self.dict_process_config['NBIN_FOLD_FAST'],
                                     self.dict_process_config['NBIN_FOLD_SLOW'])


    

        slurm_config =SlurmConfig(self.dict_process_config['N_SIMULTANEOUS_JOBS'],
                                  self.dict_process_config['PARTITION'],
                                  self.dict_process_config['MAIL_USER'],
                                  self.dict_process_config['MAIL_TYPE']) 
                           

        self.__config =  Config(filelocations, presto_config, peasoup_config, pulsarX_config, slurm_config, self.dict_process_config['DM_FILE'], 
            self.dict_process_config['BEAM_LIST'], self.dict_process_config['MAX_BEAMS_ON_PROCESSING_DISK'])
  
    @property
    def config(self):
        return self.__config;


 

     


if __name__=="__main__":
    config_reader = ConfigurationReader("config_file") 
    

     
