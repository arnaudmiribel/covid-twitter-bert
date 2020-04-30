from subprocess import PIPE, run
import sys

def out(command):
    result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
    return result


tpu_name = "auto4"#Should be unique and not allocated previously. Can be autogenerated but should consist only of lowercase, numbers and hyphens
zone = "us-central1-f" 

#Allocate a preemptible TPU
print(f"Starting to create a TPU in zone {zone} called \'{tpu_name}\'")
result = out(f"gcloud compute tpus create {tpu_name} --preemptible --zone={zone} --accelerator-type=v2-8 --version=nightly")

if result.returncode == 1:
    print(f"Failed creating the TPU with the message: {result}")
    sys.exit()
else:
    print(f"Successfully created a new TPU called \'{tpu_name}\'")

#List ip address for TPU name
result = out(f"gcloud compute tpus describe {tpu_name} --zone=us-central1-f --format='get(ipAddress)'")

if result.returncode == 1:
    print(f"Something went wrong when looking up the IP of the TPU. Following error was returned: {result.stderr}")
    sys.exit()
else:
    tpu_ip = result.stdout
    print(f"TPU ipAddress is {tpu_ip}")


#Destroy the TPU
print(f"Attempting to destroy TPU named {tpu_name}")
result = out(f"gcloud compute tpus delete {tpu_name} --zone={zone} --quiet")

if result.returncode == 1:
    print(f"Something went wrong when trying to destroy the TPU. Following error was returned: {result.stderr}")
    sys.exit()
else:
    print(f"TPU ipAddress is {tpu_ip}")




