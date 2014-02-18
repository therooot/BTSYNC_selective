#!/usr/bin/python

import sys
import subprocess

paths = sys.argv[1:]
print paths;

bashCommand = "cp config_start.txt config_done.txt"
process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
dirs_string = process.communicate()[0].strip()

configFile = open("config_done.txt", "a")
shareFile = open("share.csv", "w")



for i_path in paths:

    path = i_path

    bashCommand = "tree --noreport -din -L 1 " + path # "./btsync --generate-secret"
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    dirs_string = process.communicate()[0].strip()

    shareFile.write("\n" + path.split("/")[-1] + "\n")
    dirs = dirs_string.split("\n");
    print (dirs)

    for i_dir in dirs:
    
        if i_dir == dirs[0]:
            continue;

# config file

        bashCommand = "./btsync --generate-secret"
        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        new_secret = process.communicate()[0].strip()

        config_to_write = "    {\n\
      \"secret\" : \"" + new_secret + "\",\n\
      \"dir\" : \"" + path.replace("\\","") + "/" + i_dir.replace("\\","") + "\",\n\
      \n\
      \"use_relay_server\" : true,\n\
      \"use_tracker\" : true, \n\
      \"use_dht\" : false,\n\
      \"search_lan\" : true,\n\
      \"use_sync_trash\" : true,\n\
      \"known_hosts\" :\n\
      [\n\
        \"192.168.1.2:44444\"\n\
      ]\n\
    }"

        if (i_dir == dirs[-1]) and (i_path ==  paths[-1]):
            config_to_write += "\n  ]\n}"
        else:
            config_to_write += ",\n"

        configFile.write(config_to_write)

# share file

        bashCommand = "./btsync --get-ro-secret " + new_secret
        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        read_only_secr = process.communicate()[0].strip()
        shareFile.write(i_dir + ";" + read_only_secr + "\n")

configFile.close()
shareFile.close()
print("done.\n\nNow run: ./btsync --config config_done.txt\n\nshare generated >share.csv< with your (imaginary) friends")
