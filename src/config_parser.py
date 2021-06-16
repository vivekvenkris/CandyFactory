import data_holders
from  gen_utils import ensure_file_exists
from shutil import copyfile
import os
from pathlib import Path

# Fixed definitions or paths  
PULSARX_TEMPLATE = "/home/psr/software/PulsarX/include/template/meerkat_fold.template"


class Configuration(object):

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


    def get_value_if_exists(flag, value):
        return flag +" "+ value if value.strip("\\s+") != "" else ""


    def generate_ddplan_flags():

         return "-l {} -d {} -c {} -s {}".format(self.dict_process_config['DM_MIN'], self.dict_process_config['DM_MAX'], self.dict_process_config['DM_COHERENT_DEDISPERSION'], self.dict_process_config['N_SUBBANDS'])  

     
    def generate_rfifind_flags():

        zapint_flag = get_value_if_exists("-zapints", self.dict_process_config['RFIFIND_TIME_INTERVALS_TO_ZAP'])
        chanzap_flag = get_value_if_exists("-zapchan", self.dict_process_config['RFIFIND_CHANS_TO_ZAP'])
        time_stats_flag = get_value_if_exists("-time",self.dict_process_config['RFIFIND_TIME']) 
        ignorechan_flag = get_value_if_exists("-ignorechan", self.dict_process_config['IGNORECHAN_LIST'])
        timesig_flag = get_value_if_exists("-timesig", self.dict_process_config['RFIFIND_TIMESIG'])
        freqsig_flag = get_value_if_exists("-freqsig", self.dict_process_config['RFIFIND_FREQSIG'])

        return zapint_flag + chanzap_flag + time_stats_flag + ignorechan_flag +timesig_flag + freqsig_flag
          
    def generate_accelsearch_flags():
        accelsearch_flags = self.dict_process_config['ACCELSEARCH_FLAGS'] 

        if "zmax" in accelsearch_flags or "wmax" in accelsearch_flags or "ncpus" in accelsearch_flags:
            raise Exception("You have specified zmax, wmax or ncpus which is already fixed.") 


        return  accelsearch_flags

          


    def __init__(self, config_filename):
        self._config_filename = config_filename
        self.dict_process_config={}

        ensure_file_exists(config_filename)

        config_file = open( config_filename, "r" )

        for line in config_file:
            if line != "\n" and (not line.startswith("#")):
                key = line.split('#')[0].split(' ')[0]
                val = line.split('#')[0].split(' ')[1]
                self.dict_process_config[key] = val      #Save parameter key and value in the dictionary 
              
        config_file.close()
     
        
        singularity_flags = "-B {}:{} -B {}:{}".format(self.dict_process_config['PROCESSING_PATH'], 
                                                    self.dict_process_config['PROCESSING_PATH'],
                                                    self.dict_process_config['OUTPUT_PATH'],
                                                    self.dict_process_config['OUTPUT_PATH'])

        pulsarX_flags = " -L {} -n {} -b {}".format(self.dict_process_config['NSUBINT_FOLD'],
                                                    self.dict_process_config['NCHAN_FOLD'],
                                                    self.dict_process_config['NBIN_FOLD'])


        all_segment_configs = []


        get_acc_range_and_segment_fraction(self.dict_process_config['ACC_SEGMENT_LIST'])


        observations =  Observation(self.dict_process_config['SOURCE'],
                                 self.dict_process_config['NBEAMS'], 
                                 self.dict_process_config['TOBS'], 
                                 self.dict_process_config['BAND'], 
                                 self.dict_process_config['OBS_NO']) 
   

        presto_config = PrestoConfig(self.dict_process_config['PRESTO_IMAGE'], 
                                  singularity_flags,  
                                  rfifind_flags,
                                  ddplan_flags,
                                  accelsearch_flags)  

        peasoup_config = PeasoupConfig(self.dict_process_config['PEASOUP_IMAGE'], 
                                    singularity_flags,
                                    all_segment_configs,
                                    self.dict_process_config['START_OFFSET'],
                                    self.dict_process_config['END_OFFSET'],
                                    self.dict_process_config['DO_ZERO_ACC_BIRDIES'], 
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
                                     self.dict_process_config['NSUBINT_FOLD'], 
                                     self.dict_process_config['NBIN_FOLD'],
                                     self.dict_process_config['NCHAN_FOLD'],
                                     self.dict_process_config['ADDITIONAL_PULSARX_FLAGS'])


    

        slurm_config =SlurmConfig(self.dict_process_config['N_SIMULTANEOUS_JOBS'],
                                  self.dict_process_config['PARTITION'],
                                  self.dict_process_config['MAIL_USER'],
                                  self.dict_process_config['MAIL_TYPE']) 


        # Assign segment_fractions from lengths 


        self.dict_process_config['LIST_SEGMENTS']

        # Convert acc segment list to segment config object

        configs = []

        segments_config = SegmentConfig(self.dict_process_config['LIST_SEGMENTS'],
                                        self.dict_process_config['ACC_MIN'],
                                        self.dict_process_config['ACC_MAX'])                              

        config =  Config(filelocations, presto_config, peasoup_config, pulsarX_config, slurm_config, self.dict_process_config['DM_FILE'])
  



 

     


if __name__=="__main__":
    config = Configuration("config_file") 
    

     
