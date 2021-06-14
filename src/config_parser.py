import data_holders

# Fixed definitions or paths  
PULSARX_TEMPLATE = "/home/psr/software/PulsarX/include/template/meerkat_fold.template"


class Configuration(object):
    def __init__(self, config_filename):
        self._config_filename = config_filename
        self.dict_process_config={}

        config_file = open( config_filename, "r" )

        for line in config_file:
            if line != "\n" and (not line.startswith("#")):
            	key = line.split('#')[0].split(' ')[0]
            	val = line.split('#')[0].split(' ')[1]
                self.dict_process_config[key] = val      #Save parameter key and value in the dictionary 
              
        config_file.close()
     

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


     #cmd_rfifind = "rfifind %s -o %s -time %s -freqsig %s -timesig %s -intfrac %s -chanfrac %s %s %s %s" % (other_flags, infile_basename, time, freqsig, timesig, intfrac, chanfrac, flag_zapints, flag_zapchan, infile) 
     #rfifind_extras =  
     

    # All necessary flags 

    singularity_flags = "-B {}:{} -B {}:{}".format(self.dict_process_config['PROCESSING_PATH'], 
     	                                            self.dict_process_config['PROCESSING_PATH'],
     	                                            self.dict_process_config['OUTPUT_PATH'],
     	                                            self.dict_process_config['OUTPUT_PATH'])

    pulsarX_flags = " -L {} "


    

    observations =  Observation(self.dict_process_config['SOURCE'],
                                 self.dict_process_config['NBEAMS'], 
                                 self.dict_process_config['TOBS'], 
                                 self.dict_process_config['BAND'], 
                                 self.dict_process_config['OBS_NO']) 
   

    presto_config = PrestoConfig(self.dict_process_config['PRESTO_IMAGE'], 
                                  singularity_flags  
     	                          rfifind_flags,
     	                          ddplan_flags,
     	                          accelsearch_flags)  

    peasoup_config = PeasoupConfig(self.dict_process_config['PEASOUP_IMAGE'], 
     	                            singularity_flags 
      	                            self.dict_process_config['ACC_MIN'],
     	                            self.dict_process_config['ACC_MAX'], 
     	                            self.dict_process_config['LIST_SEGMENTS'],  
                                    self.dict_process_config['START_OFFSET']
                                    self.dict_process_config['SCALE_ACC_WITH_SEGMENTS'] 
     	                            ) 

    filelocations = FileLocations(self.dict_process_config['TAPE_PATH'],
                                   self.dict_process_config['TAPE_MACHINE']  
     	                           self.dict_process_config['STAGING_PATH'], 
     	                           self.dict_process_config['STAGING_MACHINE'],
     	                           self.dict_process_config['PROCESSING_PATH'] 
     	                           ) 


    pulsarX_config =  PulsarXConfig(self.dict_process_config['PULSARX_IMAGE'],
     	                             singularity_flags,
     	                             self.dict_process_config['PULSARX_ZERODM_MATCHED_FILTER'],
     	                             self.dict_process_config['NSUBINT_FOLD'], 
                                     self.dict_process_config['NBIN_FOLD'],
                                     self.dict_process_config[])




    slurm_config =SlurmConfig(self.dict_process_config['N_SIMULTANEOUS_JOBS'],
     	                       self.dict_process_conf
     	                       ig['PARTITION'],
     	                       self.dict_process_config['MAIL_USER'],
     	                       self.dict_process_config['MAIL_TYPE'])    




    config =  Config(filelocations, presto_config, peasoup_config, pulsarX_config, slurm_config, self.dict_process_config['DM_FILE'])


     


if __name__=="__main__":
    config = Configuration("config_file") 
    

     
