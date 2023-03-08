import os
import sys
import boto3
import subprocess
import json


ROOT_DIRECTORY = "cis4010-gnodwell"
WORKING_DIRECTORY = "/"
DIRECTORY_SET = 1







#example of pathname cis4010-gnodwell:notes/lecture1.docx
def localToCloud(usrInput, s3, my_client):
    if (len(usrInput) < 3) :
        print ("Unsuccessful copy")
        return 1
    if (len(usrInput) > 3) :
        temp = usrInput[2]
        i = 0
        for x in usrInput :
            if (i > 2) :
                temp = temp + " " + x
            i = i + 1
        usrInput[2] = temp

    fileTBU = usrInput[1] #TBU := To Be Uploaded
    pathname = usrInput[2] #path of the aws location
    if (pathname.find(':') != -1) :
        hold = pathname.split(':')
        bucket = hold[0] #Bucket to upload to
        name_of_upload = hold[1] #pathname of file uploaded
        if (name_of_upload.find(".") == -1) :
            print ("Unsuccessful copy")
            return -1

        try :
            my_client.upload_file(fileTBU, bucket, name_of_upload) #uploads file to aws s3
        except Exception as e :
            print("Unsuccessful copy") #Error Messages
            print (e)
            return 1
    else :
        print ("Unsuccessful copy")
        return 1
    return 0



def cloudToLocal(usrInput, my_client) :  #need to deal with the second option of user input#######
    global WORKING_DIRECTORY

    if (len(usrInput) > 3) :
        temp = usrInput[1]
        i = 0
        length = len(usrInput)

        for x in usrInput :
            if (i > 1 and i < length-1) :
                temp = temp + " " + x
            i = i + 1
        usrInput[1] = temp
        usrInput[2] = usrInput[length-1]

    if (usrInput[1].find(':') != -1) :
        hold = usrInput[1].split(':')
        bucket = hold[0]
        fileTBD = hold[1] #file to be downloaded from the cloud
        fileLoc = usrInput[2]

        try :
            my_client.download_file(bucket, fileTBD, fileLoc)
        except Exception as e :
            print ("Unsuccessful copy")
            print(e)
            return 1
    else :
        if (WORKING_DIRECTORY.find(':') == -1) :
            print ("Unsuccessful copy")
            return 1
        else :
            hold = WORKING_DIRECTORY.split(':')
            bucket_name = hold[0]
            file_path = hold[1] + usrInput[1]
            local_file_path = usrInput[2]

            try :
                my_client.download_file(bucket_name, file_path, local_file_path)
            except Exception as e :
                print ("Unsuccessful copy")
                print (e)
                return 1
    return 0



def find_subfolders(s3, bucket_name) :
    directory_list = []
    comp = "aksjdglbasdfjlasdfhs"

    for x in s3.buckets.all() :
        if (x.name == bucket_name) :
            my_bucket = s3.Bucket(bucket_name)
            for y in my_bucket.objects.all() :
                if (y.key.find('/') != -1) :
                    splits = y.key.split('/')
                    if (splits[0] != comp) :
                        comp = splits[0]
                        directory_list.append(comp + "/")
                if (y.key.find('.') == -1) :
                    directory_list.append(y.key)

    return directory_list


def find_subfiles(s3, bucket_name) :
    directory_list = []
    comp = "aksjdglbasdfjlasdfhs"

    for x in s3.buckets.all() :
        if (x.name == bucket_name) :
            my_bucket = s3.Bucket(bucket_name)
            for y in my_bucket.objects.all() :
                directory_list.append(y.key)

    return directory_list



def changeDirectory(usrInput, s3, my_client) :
    global DIRECTORY_SET
    global WORKING_DIRECTORY
    check_set = 0
    i = 0
    temp = usrInput[1]

    if (len(usrInput) > 2) :
        for x in usrInput :
            if (i > 1) :
                temp = temp + " " + x
            i = i + 1

    usrInput[1] = temp

    if (usrInput[1] == ".." and DIRECTORY_SET == 0) :
        if (WORKING_DIRECTORY.find(":") == -1) :
            return 0
        elif (WORKING_DIRECTORY.find('/') == -1) :
            check_set = 1
            WORKING_DIRECTORY = "/"
            DIRECTORY_SET = 1
            return 0
        else :
            catch = WORKING_DIRECTORY.split(':')
            bucket_name = catch[0]
            file_path = catch[1]
            file_path = file_path.split('/')
            length = len(file_path)
            i = 0
            new_file_path = ""
            for x in file_path :
                if (i < length-2) :
                    new_file_path = new_file_path + file_path[i] + "/"
                i = i + 1
            WORKING_DIRECTORY = bucket_name + ":" + new_file_path
            check_set = 1
            return 0

    if (usrInput [1] == "/") :
        WORKING_DIRECTORY = "/"
        DIRECTORY_SET = 1
        check_set = 1

    if (usrInput[1].find(':') == -1 and DIRECTORY_SET == 1) :
        for x in s3.buckets.all() :
            if (x.name == usrInput[1]) :
                WORKING_DIRECTORY = usrInput[1] + ':'
                DIRECTORY_SET = 0
                check_set = 1
                return 0

    elif (usrInput[1].find(':') != -1 and DIRECTORY_SET == 1) :
        hold = usrInput[1].split(':')
        bucket_name = hold[0]
        folder_path = hold[1]
        length = len(folder_path)
        if (folder_path[length-1] != '/') :
            folder_path = folder_path + "/"
        directory_list = find_subfolders(s3, bucket_name)

        for x in directory_list :
            if (x == folder_path) :
                WORKING_DIRECTORY = bucket_name + ":" + folder_path
                DIRECTORY_SET = 0
                check_set = 1

    elif(usrInput[1].find(':') == -1 and DIRECTORY_SET == 0) :
        if (WORKING_DIRECTORY.find('/') != -1) :
            hold = WORKING_DIRECTORY.split(':')
            folder_path = hold[1] + usrInput[1]
        else :
            folder_path = usrInput[1]

        length = len(folder_path)

        if (folder_path[length-1] != '/') :
            folder_path = folder_path + "/"

        if (WORKING_DIRECTORY.find(':') != -1) :
            hold = WORKING_DIRECTORY.split(':')
            bucket_name = hold[0]
            directory_list = find_subfolders(s3, bucket_name)

            for x in directory_list :
                if (x == folder_path) :
                    WORKING_DIRECTORY = bucket_name + ":" + folder_path
                    DIRECTORY_SET = 0
                    check_set = 1

        else :
            bucket_name = WORKING_DIRECTORY
            directory_list = find_subfolders(s3, bucket_name)

            for x in directory_list :
                if (x == folder_path) :
                    WORKING_DIRECTORY = bucket_name + ":" + folder_path
                    DIRECTORY_SET = 0
                    check_set = 1

    if (check_set == 0) :
        print ("Cannot change folder")
        return 1
    return 0



def current_working_directory():
    global WORKING_DIRECTORY
    print (WORKING_DIRECTORY)
    return 0



def create_bucket(usrInput, s3, my_client) :
    print("usrInput: ", usrInput[1])
    try :
        response = my_client.create_bucket(Bucket = usrInput[1])
    except Exception as e :
        print ("Cannot crete bucket")
        print (e)
        return 1
    return 0



def create_folder(usrInput, s3, my_client) :
    global WORKING_DIRECTORY
    if(len(usrInput) < 2) :
        print ("Cannot create folder")
        return 1

    if (usrInput[1].find(':') == -1) :
        if (WORKING_DIRECTORY.find(':') == -1) :
            print ("Cannot create folder")
            return 1
        else :
            hold = WORKING_DIRECTORY.split(':')
            bucket_name = hold[0]
            if (hold[1].find('/') != -1) :
                file_path = hold[1] + usrInput[1]
            else :
                file_path = usrInput[1]

    else :
        hold = usrInput[1].split(':')
        bucket_name = hold[0]
        file_path = hold[1]

    length = len(file_path)
    if (file_path[length-1] != '/') :
        file_path = file_path + "/"

    try :
        my_client.put_object(Bucket=bucket_name, Key=file_path)
    except Exception as e :
        print("Cannot create folder")
        print (e)
        return 1
    return 0



def list_content(usrInput, s3, my_client) :
    global WORKING_DIRECTORY

    i = 0
    for x in usrInput :
        if (x == "-l") :
            del usrInput[i]
        i = i + 1

    if (len(usrInput) > 2) :
        temp = usrInput[1]
        i = 0
        for x in usrInput :
            if (i > 1) :
                temp = temp + " " + x
            i = i + 1
        usrInput[1] = temp

    print_string = ""
    files_in_directory = []

    if (len(usrInput) == 1) :
        if (WORKING_DIRECTORY == "/") :
            for x in s3.buckets.all() :
                print_string = print_string + x.name + "    "
        else :
            hold = WORKING_DIRECTORY.split(':')
            bucket_name = hold[0]
            directory_list = find_subfiles(s3, bucket_name)

            if (hold[1] == "") :
                for x in directory_list :
                    if (x.find('/') != -1) :
                        hold = x.split('/')
                        files_in_directory.append(hold[0] + "/")
                    else :
                        files_in_directory.append(x)
            else :
                pathway = hold[1].split('/')
                count = 0
                for i in pathway :
                    if (i != '') :
                        count = count + 1
                for x in directory_list :
                    hold = x.split('/')
                    if (len(hold) >= count) :
                        if (hold[count-1] == pathway[count-1]) :
                            if (hold[count].find('.') != -1) :
                                files_in_directory.append(hold[count])
                            elif (hold[count] != '') :
                                files_in_directory.append(hold[count] + "/")

            if (len(files_in_directory) == 0) :
                return 0

            files_in_directory = list(dict.fromkeys(files_in_directory))
            for x in files_in_directory :
                print_string = print_string + x + "    "


    else :
        if (usrInput[1].find(':') == -1) :
            usrInput[1] = usrInput[1] + ":"

        hold = usrInput[1].split(":")
        bucket_name = hold[0]
        directory_list = find_subfiles(s3, bucket_name)
        if (hold[0] == "/") :
            for x in s3.buckets.all() :
                print_string = print_string + x.name + "    "
        elif (hold[1] != "") :
            length = len(hold[1])
            if (hold[1][length-1] != '/') :
                hold[1] = hold[1] + '/'

            pathway = hold[1].split("/")
            count = 0
            for i in pathway :
                if (i != '') :
                    count = count + 1
            for x in directory_list :
                hold = x.split('/')
                if (len(hold) >= count) :
                    if (hold[count-1] == pathway[count-1]) :
                        if (hold[count].find('.') != -1) :
                            files_in_directory.append(hold[count])
                        elif (hold[count] != '') :
                            files_in_directory.append(hold[count] + "/")
            if (len(files_in_directory) == 0) :
                return 0
            files_in_directory = list(dict.fromkeys(files_in_directory))
            for x in files_in_directory :
                print_string = print_string + x + "    "
        else :
            for x in directory_list :
                if (x.find('/') != -1) :
                    hold = x.split('/')
                    files_in_directory.append(hold[0] + "/")
                else :
                    files_in_directory.append(x)


            if (len(files_in_directory) == 0) :
                return 0

            files_in_directory = list(dict.fromkeys(files_in_directory))
            for x in files_in_directory :
                print_string = print_string + x + "    "

    print(print_string)
    return 0



def copy_object(usrInput, s3, my_client) :
    global WORKING_DIRECTORY

    if (usrInput[1].find(':') != -1) :
        hold = usrInput[1].split(':')
        source_bucket_name = hold[0]
        source_key = hold[1]
    else :
        if (WORKING_DIRECTORY == '/') :
            print ("Cannot perform copy")
            return 1
        else :
            hold = WORKING_DIRECTORY.split(":")
            source_bucket_name = hold[0]
            source_key = usrInput[1]

    if (usrInput[2].find(":") != -1) :
        hold = usrInput[2].split(':');
        dest_bucket_name = hold[0]
        dest_key = hold[1]
    else :
        if (WORKING_DIRECTORY == '/'):
            print ("Cannot perform copy")
            return 1
        else :
            hold = WORKING_DIRECTORY.split(':')
            dest_bucket_name = hold[0]
            dest_key = hold[1] + usrInput[2]


    copy_source = {'Bucket':source_bucket_name, 'Key':source_key}

    try :
        my_client.copy(copy_source, dest_bucket_name, dest_key)
    except Exception as e :
            print ("Cannot perform copy")
            print (e)
            return 1
    return 0



def delete_object(usrInput, s3, my_client) :
    global WORKING_DIRECTORY
    flag = 0

    if (len(usrInput) > 2) :
        temp = usrInput[1]
        i = 0
        for x in usrInput :
            if (i > 1) :
                temp = temp + " " + x
            i = i + 1
        usrInput[1] = temp

    if (usrInput[1].find(':') != -1) :
        hold = usrInput[1].split(':')
        bucket_name = hold[0]
        key = hold[1]
    else :
        if (WORKING_DIRECTORY == '/') :
            print("Cannot perform delete")
            return 1

        hold = WORKING_DIRECTORY.split(':')
        bucket_name = hold[0]
        if (hold[1] != '') :
            key = hold[1] + usrInput[1]
        else :
            key = usrInput[1]



    if (key.find('.') == -1) :
        length = len(key)
        if (key[length-1] != '/') :
            key = key + '/'

        folder_contents = find_subfiles(s3, bucket_name)
        for x in folder_contents :
            if (key != x and key in x) :
                splits = x.split("/")
                splits2 = key.split("/");
                if (splits[0] == splits2[0]) :
                    flag = 1
                    print ("Cannot perform delete")
                    return 1



    try :
        result = my_client.delete_object(Bucket=bucket_name, Key=key)
    except Exception as e :
        print ("Cannot perform delete")
        print (e)
        return 1
    return 0



def delete_bucket(usrInput, s3, my_client) :
    try :
        my_client.delete_bucket(Bucket=usrInput[1])
    except Exception as e :
        print ("Cannot delete bucket")
        print (e)
        return 1
    return 0






#START OF MAIN PROGRAM

fp = open("S5-S3conf", "r")
access_key = fp.readline()
secret_access = fp.readline()
str1 = access_key.split(" ", 2)
str2 = secret_access.split(" ", 2)

try :
    my_session = boto3.Session(
            aws_access_key_id=str1[2].strip(),
            aws_secret_access_key=str2[2].strip()
            )

    my_client = boto3.client('s3',
            aws_access_key_id=str1[2].strip(),
            aws_secret_access_key=str2[2].strip()
            )
    s3 = my_session.resource('s3')
    for bucket in s3.buckets.all() :
        hold = bucket

    print("Welcome to the AWS S3 Storage Shell (S5)")
    print("You are now connected to your S3 storage")

    usrInput = input("S5> ");
    usrInput = usrInput.split(" ")
    command = usrInput[0]

    while (command != "quit" and command != "exit") :

        if (command == "lc_copy") :
            result = localToCloud(usrInput, s3, my_client)

        elif (command == "cl_copy") :
            result = cloudToLocal(usrInput, my_client)

        elif (command == "create_bucket") :
            result = create_bucket(usrInput, s3, my_client)

        elif (command == "create_folder") :
            result = create_folder(usrInput, s3, my_client)

        elif (command == "ch_folder") :
            result = changeDirectory(usrInput, s3, my_client)

        elif (command == "cwf") :
            result = current_working_directory()

        elif (command == "list") :
            result = list_content(usrInput, s3, my_client)

        elif (command == "ccopy") :
            result = copy_object(usrInput, s3, my_client)

        elif (command == "cdelete") :
            result = delete_object(usrInput, s3, my_client)

        elif (command == "delete_bucket") :
            result = delete_bucket(usrInput, s3, my_client)

        else:
            try :
                if (len(usrInput) > 1) :
                    string = usrInput[0] + " " + usrInput [1]
                else :
                    string = usrInput[0]
                #os.system(string)
                subprocess.call(string, shell=True)
            except subprocess.CalledProcessError :
                print ("Incorrect input")

        usrInput = input("S5> ")
        usrInput = usrInput.split(" ")
        command = usrInput[0]

except Exception as e :
    print (e)
    print("Welcome to the AWS S3 Storage Shell (S5)")
    print("You could not be connected to your S3 storage")
    print("Please review procedures for authenticating your account on AWS S3")






















