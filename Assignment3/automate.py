import configparser
import os
import subprocess
from subprocess import PIPE, run
from datetime import datetime

if (os.path.isfile('./GCP.conf')):
    gcpParser = configparser.RawConfigParser()
    gcpFilePath = "./GCP.conf"
    gcpParser.read(gcpFilePath)
elif (os.path.isfile('./gcp.conf')):
    gcpParser = configparser.RawConfigParser()
    gcpFilePath = "./gcp.conf"
    gcpParser.read(gcpFilePath)

if (os.path.isfile('./Azure.conf')):
    azParser = configparser.RawConfigParser()
    azFilePath = "./Azure.conf"
    azParser.read(azFilePath)
elif (os.path.isfile('./azure.conf')):
    azParser = configparser.RawConfigParser()
    azFilePath = "./azure.conf"
    azParser.read(azFilePath)



GCP_possible_specifications = ["accelerator", "type", "boot-disk-device-name", "boot-disk-provisioned-iops", "boot-disk-size",
        "create-disk", "description", "disk", "boot", "device-name", "mode", "name", "scope", "hostname", "ipv6-network-tier",
        "ipv6-public-ptr-domain", "labels", "local-ssd", "interface", "machine-type", "maintenance-policy", "metadata", "metadata-from-file",
        "min-cpu-platform", "min-node-cpu", "network", "network-interface", "network-tier", "private-ipv6-google-access-type",
        "private-network-ip", "resource-policies", "shielded-integrity-monitoring", "source-instance-template", "stack-type", "subnet", "tags",
        "threads-per-core", "zone", "address", "boot-disk-kms-key", "boot-disk-kms-keyring", "boot-disk-mks-location", "boot-disk-kms-project",
        "custom-cpu", "custom-memory", "custom-extensions", "custom-vm-type", "image-family-scope", "image-project", "image", "image-family",
        "source-snapshot", "node", "node-affinity-file", "node-group", "public-ptr-domain", "reservation", "reservation-affinity", "default",
        "scopes", "service-account"]

azure_possible_specifications = ["name", "n", "resource-group", "g", "availability-set", "boot-diagnostic-storage", "capacity-reservation-group",
        "crg", "computer-name", "count", "custom-date", "edge-zone", "enable-agent", "enable-auto-update", "enable-hotpatching", "enable-secure-boot",
        "enable-vtpm", "eviction-policy", "image", "license-type", "location", "l", "max-price", "no-wait", "patch-mode", "platform-fault-domain",
        "ppg", "priority", "secrets", "security-type", "size", "ssh-key-name", "tags", "user-data", "validate", "vmss", "zone", "z", "admin-password",
        "admin-username", "authentication-type", "generate-ssh-keys", "ssh-dest-key-path", "ssh-key-values", "host", "host-group", "assign-identity",
        "role", "scope", "plan-name", "plan-product", "plan-promotion-code", "plan-publisher", "workspace", "accelerated-networking", "asgs",
        "nic-delete-option", "nics", "nsg", "nsg-rule", "private-ip-address", "public-ip-address", "public-ip-address-allocation", "subnet",
        "public-ip-address-dns-name", "public-ip-sku", "subnet-address-prefix", "vnet-address-prefix", "vnet-name", "attach-data-disks", "attach-os-disk",
        "data-disk-caching", "data-disk-delete-option", "data-disk-encryption-sets", "data-disk-sizes-gb", "encryption-at-host", "ephemeral-os-disk",
        "ephemeral-os-disk-placement", "ephemeral-placement", "os-disk-caching", "os-disk-delete-option", "os-disk-delete-option",
        "os-disk-encryption-set", "os-disk-name", "os-disk-size-gb", "os-type", "specialized", "storage-account", "storage-container-name",
        "storage-sku", "ultra-ssd-enabled", "use-unmanaged-disk"]


gcpStr = "gcloud compute instances create "
statuses = {}
tempName = "temp"


try:
    for section in gcpParser.sections():
        for item, value in gcpParser.items(section):
            if (item == "name"):
                gcpStr = gcpStr + value + " "
                tempName = value
        for item, value in gcpParser.items(section):
            if (item in GCP_possible_specifications and item != "name"):
                gcpStr = gcpStr + "--" + item + "=" + value + " "
        print ("Command sent to cloud service:")
        print (gcpStr)
        result = subprocess.run(gcpStr, capture_output=True, shell=True, text=True)
        print ("Result:")
        print (result.stdout)

        returnStr = str(result.stdout)
        if ("RUNNING" in returnStr):
           statuses[tempName] = "RUNNING"
        else :
            statuses[tempName] = "NOT RUNNING"

        gcpStr = "gcloud compute instances create "
except Exception as e:
    doNothing = 1




try :
    azStr = "az vm create "
    for section in azParser.sections():
        for item, value in azParser.items(section):
            if (item in azure_possible_specifications):
                azStr = azStr + "--" + item + " " + value + " "
                if (item == "name"):
                    tempName = value
        print ("Command sent to cloud service:")
        print (azStr)
        result = subprocess.run(azStr, capture_output=True, shell=True, text=True)
        print ("Result:")
        print(result.stdout)


        returnStr = str(result.stdout)
        if ("VM running" in returnStr):
            statuses[tempName] = "RUNNING"
        else:
            statuses[tempName] = "NOT RUNNING"
        azStr = "az vm create "
except Exception as e:
    doNothing = 2


dateOBJ = datetime.now()
dateStamp = str(dateOBJ.year) + "-" + str(dateOBJ.month) + "-" + str(dateOBJ.day) + ":" + str(dateOBJ.hour) + ":" + str(dateOBJ.minute) + ":" + str(dateOBJ.second)
myUsr = os.getenv('USER')

filename = "VMcreation_" + dateStamp + ".txt"
with open(filename, 'w') as fp:
    try:
        for section in gcpParser.sections():
            for item, value in gcpParser.items(section):
                if (item == 'name'):
                    current = value
                    outString = "Name: " + value + "\n"
                    fp.write(outString)
            for item, value in gcpParser.items(section):
                if (item not in GCP_possible_specifications):
                    outString = item + ": " + value + "\n"
                    fp.write(outString)
            for item, value in gcpParser.items(section):
                if (item != 'name' and item in GCP_possible_specifications):
                    outString = item + ": " + value + "\n"
                    fp.write(outString)

            outString = "Status: " + statuses[current] + "\n"
            fp.write(outString)
            fp.write("\n")
    except Exception as e:
        doNothing = 3

    try:
        for section in azParser.sections():
            for item, value in azParser.items(section):
                if (item == 'name'):
                    current = value
                    outString = "Name: " + value + "\n"
                    fp.write(outString)
            for item, value in azParser.items(section):
                if (item not in azure_possible_specifications):
                    outString = item + ": " + value + "\n"
                    fp.write(outString)
            for item, value in azParser.items(section):
                if (item != 'name' and item in azure_possible_specifications):
                    outString = item + ": " + value + "\n"
                    fp.write(outString)
            outString = "Status: " + statuses[current] + "\n"
            fp.write(outString)
            fp.write("\n")
    except Exception as e:
        doNothing = 4




if (os.path.isfile('./GCP.conf')):
    commandStr = "mv ./GCP.conf ./GCP.conf_" + dateStamp + ".conf"
    result = subprocess.run(commandStr, capture_output=True, shell=True, text=True)
elif (os.path.isfile('/gpc.conf')):
    commandStr = "mv ./gcp.conf ./gcp.conf_" + dateStamp + ".conf"
    result = subprocess.run(commandStr, capture_output=True, shell=True, text=True)

if (os.path.isfile('/Azure.conf')):
    commandStr = "mv ./Azure.conf ./Azure_" + dateStamp + ".conf"
    result = subprocess.run(commandStr, capture_output=True, shell=True, text=True)
elif (os.path.isfile('./azure.conf')):
    commandStr = "mv ./azure.conf ./azure_" + dateStamp + ".conf"
    result = subprocess.run(commandStr, capture_output=True, shell=True, text=True)


usrInput = input("Would you like to open ports to your Azure VM? (y/n)")
usrInput = usrInput.lower()


if (usrInput == 'y'):
    while (True):
        port = input("What port would you like to open? ")
        group = input("What resource group would you like the port to be open to? ")
        vm = input("What VM would you like the port to be open to? ")

        commandStr = "az vm open-port --port " + str(port) + " --resource-group " + str(group) + " --name " + str(vm)
        result = subprocess.run(commandStr, capture_output=True, shell=True, text=True)
        print ("Result:")
        print (result.stdout)

        cont = input ("Would you like to open another port in Azure? (y/n)")
        cont = cont.lower()
        if (cont == 'n'):
            break



usrInput = input ("Would you like to open ports to your GCP? (y/n) ")
usrInput = usrInput.lower()
counter = 1
if (usrInput == 'y'):
    while (True):
        port = input("What port would you like to open? ")
        protocol = input("What protocol would you like to open ? (tcp, udp, icmp, esp, ah, sctp) ")

        commandStr = "gcloud compute firewall-rules create MY-RULE-" + str(counter) + "--allow " + str(protocol) + ":" + str(port)
        result = subprocess.run(commandStr, capture_output=True, shell=True, text=True)
        counter = counter + 1

        cont = input ("Would you like to open another port in Azure? (y/n)")
        cont = cont.lower()
        if (cont == 'n'):
            break

