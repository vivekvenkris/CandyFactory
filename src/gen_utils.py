import sys, os, os.path, glob, subprocess, multiprocessing, shlex, shutil, copy
from log import Logger, init_logging
import datetime, time
from configparser import ConfigParser
from subprocess import call, PIPE, STDOUT
from errno import ENOENT

def get_nearest_even_number(number_int):
        return number_int if int(number_int) % 2 == 0 else number_int-1


def strip_quotes_and_spaces(value):
    return value.replace("\"","").strip("\\s+")       


def run_process(command):

        logger = Logger.getInstance().logger

        command_chunks = command.split()

        time_start = time.time()

        logger.info("\n RUNNING COMMAND: {}\n".format(command))
        #print(command_chunks)
        #proc = subprocess.Popen(command_chunks, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env = os.environ.copy())
        #proc.communicate()  #Wait for the process to complete                                                                                                                                                    

        time_end = time.time()

        logger.info("TOTAL TIME TAKEN: %d s\n" % (time_end - time_start))



def guess_and_change_dtype(value):

    if "." in value:

        try:
            return float(value)
        except ValueError:
            pass
    else:
        try:
            return int(value)
        except ValueError:
            pass

    return value



def run_with_singularity(image, singularity_flags, command):

        command = "singularity exec " + singularity_flags + " " + image + " " + command
        run_process(command)


def dir_exists(dir):
    return os.path.exists(dir) and os.path.isdir(dir)


def file_exists(file):
    return os.path.exists(file) and os.path.isfile(file)


def log_subprocess_output(pipe):
    for line in iter(pipe.readline, b''): # b'\n'-separated lines
        logging.info('got line from subprocess: %r', line)


def run_subprocess(str_id, cmd_string, logger):
    chunks = shlex.split(cmd_string)
    p = subprocess.Popen(chunks, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env = os.environ.copy())
    with p.stdout:
        log_subprocess_output(p.stdout)
    #exit_code = p.wait()

def is_file_empty(file_name):

    return os.stat(file_name).st_size == 0


def ensure_file_exists(file_name):
    if not file_exists(file_name):
        raise IOError(ENOENT, 'No file found', file_name)


def ensure_directory_exists(directory_name):
    if not dir_exists(directory_name):
        raise IOError(ENOENT, 'No directory found', directory_name)


def ensure_directory_is_not_empty(directory_name):
    if len(os.listdir(directory_name)) == 0:
        raise IOError(ENOENT, 'No files in directory', directory_name)

def backup_if_exists(source, logger):

    if file_exists(source):
        logger.warn(source + " exists.")
        logger.warn("moving older file: " + source + " to " + source+".old")
        os.rename(source, source+".old")

def move_file(source, destination):
    os.rename(source, destination)


def get_path(dir, file):
    os.path.join(dir, file)

def write_array_pretty(file_name, array, logger):
    
    widths = [max(map(len, col)) for col in zip(*array)]

    text_to_save= ""

    for row in array:
        text_to_save = text_to_save + "  ".join((val.ljust(width) for val, width in zip(row, widths))) + " \n"

    logger.info("Writing to " +file_name)

    with  open(file_name, 'w') as f:
        f.write(text_to_save)


