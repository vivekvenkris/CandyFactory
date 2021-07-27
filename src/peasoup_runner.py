from status_manager import StatusManager
from search_operations import SearchOperations
import sys,os, path, glob
import argparse
from config_parser import ConfigurationReader
from log import Logger, init_logging
import datetime
from ledger import Ledger
from app_utils import ensure_correct_processing_status
from gen_utils import run_process, run_with_singularity
import xml.etree.ElementTree as ET
import numpy as np
import itertools
def get_args(args):
    argparser = argparse.ArgumentParser(description="Run peasoup")
    argparser.add_argument("-config", dest="config", help="configuration file")
    argparser.add_argument("-verbose", dest="verbose", help="Enable verbose terminal logging", action="store_true")
    argparser.add_argument("-beam_num", dest="beam_num", help="beam number to process")
    argparser.add_argument("-ledger_file", dest="ledger_file", help="ledger_file")
    argparser.add_argument("-force", dest="force", help="Try to force run peasoup even if status is not as expected")
    argparser.add_argument("-log_file_prefix", dest="log_file_prefix", help="Name of log file",default="candyfactory")


    argparser.add_argument("-search_type", dest="search_type", help="Search time: ZERO_ACC, ACC, SEGMENTED",required=True)

    args = argparser.parse_args(args)
    return args


class PeasoupRunner(SearchOperations):
    def __init__(self, config, out_prefix=""):
        super().__init__(config, out_prefix)

    def get_base_peasoup_command(self, beam_name):
        return  "/usr/local/bin/peasoup --dm_file {} --pad -z {}.birds -k {}.badchan_peasoup {}" \
                        .format(self.config.dm_file, beam_name, beam_name, self.config.peasoup_config.peasoup_flags)


    def __get_known_rfi_indices(self, beam_name, freqs):

        birdies_file = os.path.join(self.config.root_output_dir, beam_name, beam_name+".birdies")
        h = np.arange(1,self.config.birdie_matcher_config.harmonics)
        ratios = np.outer(h,1.0/h)
        all_ratios = np.unique(np.sort(ratios.ravel()))

        known_rfi_freqs = np.loadtxt(birdies_file,dtype=float, usecols=(0)) 


        p_tol = float(self.config.birdie_matcher_config.period_tol)

        w_harmonics=[]

        for number in all_ratios:
           for rfi in known_rfi_freqs:
                for a in freqs:
                    if np.abs(a - number*rfi)/a < p_tol:
                        w_harmonics.append(a)

        all_harmonics=sorted(list(set(list(w_harmonics))))
        rfi_indices = np.array([np.where(freqs==h)[0][0] for h in all_harmonics])   
        return rfi_indices         



    def write_excised_candidate_list(self, beam_name, xml_files, out_file):

        print(xml_files)



        freqs = []
        periods = []
        dms = []
        snrs = []
        accs = []

        for x in xml_files:
            tree = ET.parse(x)
            root = tree.getroot()
            freqs.extend([1/float(a.text) for a in root.findall("candidates/candidate/period")])
            periods.extend([a.text for a in root.findall("candidates/candidate/period")])
            dms.extend([a.text for a in root.findall("candidates/candidate/dm")])
            snrs.extend([a.text for a in root.findall("candidates/candidate/snr")])
            accs.extend([a.text for a in root.findall("candidates/candidate/acc")])

        periods = np.array(periods, dtype=float)
        freqs = np.array(freqs, dtype=float)
        dms = np.array(dms, dtype=float)
        snrs = np.array(snrs, dtype=float)
        accs = np.array(accs, dtype=float)


        rfi_freqs = self.__get_known_rfi_indices(beam_name, freqs)
        self.logger.info("Beam: {} -> num raw cands: {} num rfi: {} residual ncands: {}".format(beam_name, len(periods), len(rfi_freqs), len(periods) - len(rfi_freqs)))
        if len(rfi_freqs) > 0:
            mask = np.ones(len(freqs), np.bool)
            mask[rfi_freqs] = 0

            periods = np.array(periods[mask], dtype=float)
            dms = np.array(dms[mask], dtype=float)
            snrs = np.array(snrs[mask], dtype=float)
            accs = np.array(accs[mask], dtype=float)
        
        ncands = len(periods)



        with open(out_file, 'w') as f:
            f.write("#id DM accel F0 F1 S/N\n")            
            for i in range(ncands):
               f.write("{:d} {:.3f} {} {:.2f} {} {:.2f}\n".format(i, dms[i], periods[i], accs[i], 0, snrs[i]))

            f.close()

        



    def run_peasoup(self, beam_name, search_type):

        status = self.ledger.get_status(beam_name)
        ensure_correct_processing_status(status,self.status_manager.ZERO_DM_ACCELSEARCH)

        base1_peasoup_cmd = self.get_base_peasoup_command(beam_name)
        peasoup_config = self.config.peasoup_config

        if(search_type == self.status_manager.SEARCH_TYPE_ZERO_ACC):
            out_dir = "{}{}_{}".format(self.out_prefix, beam_name, search_type)
            peasoup_cmd = "{} --acc_start 0 --acc_end 0 -o {}".format(base1_peasoup_cmd, out_dir) 
            run_with_singularity(peasoup_config.singularity_image, peasoup_config.singularity_flags, peasoup_cmd)
            self.ledger.update_status(beam_name, self.status_manager.PEASOUP, search_type=self.status_manager.SEARCH_TYPE_ZERO_ACC)

            list_file = os.path.join(self.config.root_output_dir, beam_name, out_dir, "peasoup_cands.list")
            self.write_excised_candidate_list(beam_name, [os.path.join(self.config.root_output_dir, beam_name, out_dir, "overview.xml")], list_file)
            self.ledger.update_status(beam_name, self.status_manager.CANDIDATE_RFI_MATCHING, search_type=self.status_manager.SEARCH_TYPE_ZERO_ACC)



        elif(search_type == self.status_manager.SEARCH_TYPE_ACC):

            segment_config = [x for x in peasoup_config.segment_configs if x.fractional_segment_length == 1][0]
            out_dir = "{}{}_{}".format(self.out_prefix, beam_name, search_type)
            peasoup_cmd = "{} --acc_start {} --acc_end {}  --start {} --end {} -o {}".format(base1_peasoup_cmd, segment_config.acc_start, segment_config.acc_end, peasoup_config.start_fraction, peasoup_config.end_fraction,out_dir)
            run_with_singularity(peasoup_config.singularity_image, peasoup_config.singularity_flags, peasoup_cmd)
            self.ledger.update_status(beam_name, self.status_manager.PEASOUP, search_type=self.status_manager.SEARCH_TYPE_ACC)

            list_file = os.path.join(self.config.root_output_dir, beam_name, out_dir, "peasoup_cands.list")
            self.write_excised_candidate_list(beam_name, [os.path.join(self.config.root_output_dir, beam_name, out_dir, "overview.xml")], list_file)
            self.ledger.update_status(beam_name, self.status_manager.CANDIDATE_RFI_MATCHING, search_type=self.status_manager.SEARCH_TYPE_ACC)




        else:

            for segment_config in peasoup_config.segment_configs:


                base2_peasoup_cmd = "{} --acc_start {} --acc_end {} ".format(base1_peasoup_cmd, segment_config.acc_start, segment_config.acc_end)

                if( segment_config.fractional_segment_length == 1):
                    continue


                else:

                    start = peasoup_config.start_fraction

                    end = None

                    while start + segment_config.fractional_segment_length <=  peasoup_config.end_fraction: 

                        end = start + segment_config.fractional_segment_length

                        dir_str = "{}{}_SEG-{:.3f}_{:.3f}_{:.3f}".format(self.out_prefix, beam_name, segment_config.fractional_segment_length, start, end)

                        peasoup_cmd = "{} --start {:.3f} --end {:.3f} -o {}".format(base2_peasoup_cmd, start, end, dir_str)
                        run_with_singularity(peasoup_config.singularity_image, peasoup_config.singularity_flags, peasoup_cmd)

                        list_file = os.path.join(dir_str, "peasoup_cands.list")
                        self.write_excised_candidate_list(beam_name, [os.path.join(self.config.root_output_dir, beam_name, dir_str, "overview.xml")], list_file)                        

                        start = end

                    if (peasoup_config.end_fraction - start)%segment_config.fractional_segment_length  > 0:

                        #if there are any residual data, choose the last segment from the end
                        start = peasoup_config.end_fraction - segment_config.fractional_segment_length

                        end = peasoup_config.end_fraction

                        dir_str = "{}{}_SEG-{:.3f}_{:.3f}_{:.3f}".format(self.out_prefix, beam_name, segment_config.fractional_segment_length, start, end)

                        peasoup_cmd = "{} --start {:.3f} --end {:.3f} -o {}_{}".format(base2_peasoup_cmd, start, end, beam_name, dir_str)

                        run_with_singularity(peasoup_config.singularity_image, peasoup_config.singularity_flags, peasoup_cmd)

                        list_file = os.path.join(dir_str, "peasoup_cands.list")
                        self.write_excised_candidate_list(beam_name, [os.path.join(self.config.root_output_dir, beam_name, dir_str, "overview.xml")], list_file)                           



            self.ledger.update_status(beam_name, self.status_manager.CANDIDATE_RFI_MATCHING, search_type=self.status_manager.SEARCH_TYPE_SEGMENTED)


    def run(self, beam_name, search_type):
        self.run_peasoup(self, beam_name, search_type)









def main(args=sys.argv[1:]):

    #get args, inititalise logger, config and ledger
    args = get_args(args)    
    logger = init_logging(file_name="{}_{}.log".format(args.log_file_prefix,(datetime.datetime.now()).strftime("%Y-%m-%d-%H:%M:%S")),
                             file_level=logging.DEBUG if args.verbose else None)

    config_reader = ConfigurationReader(args.config) 
    config = config_reader.config

    ledger = Ledger.getInstance() if args.ledger_file is None else Ledger(args.ledger_file)

    peasoup_runner = PeasoupRunner(config, args.out_prefix)



if __name__ == '__main__':
    main()


 


        



















