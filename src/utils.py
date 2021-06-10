import sys, os, os.path, glob, subprocess, multiprocessing, shlex, shutil, copy
from Log import logger


def get_nearest_even_number(number_int):
        return number_int if int(number_int) % 2 == 0 else number_int-1


       


def run_process(command):

        logger = Logger().logger

        command_chunks = command.split()

        datetime_start = (datetime.datetime.now()).strftime("%Y/%m/%d  %H:%M")
        time_start = time.time()

        logger.info("****************************************************************\n")
        logger.info("START DATE AND TIME: %s\n" % (datetime_start))
        logger.info("\nCOMMAND:\n")
        logger.info("%s\n\n" % (command))
        logger.info("WORKING DIRECTORY: %s\n" % (work_dir))
        logger.info("****************************************************************\n")
        log_file.flush()

        proc = subprocess.Popen(command_chunks, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, envs = os.environ.copy())
        proc.communicate()  #Wait for the process to complete                                                                                                                                                    

        datetime_end = (datetime.datetime.now()).strftime("%Y/%m/%d  %H:%M")
        time_end = time.time()

        logger.info("\nEND DATE AND TIME: %s\n" % (datetime_end))
        logger.info("\nTOTAL TIME TAKEN: %d s\n" % (time_end - time_start))


def run_with_singularity(image, singularity_flags, command):


        command = "singularity exec" + singularity_flags + " " + image + " " + command
        run_process(command)