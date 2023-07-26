# Folder Synchronization

import os
import shutil
import time
import datetime

folder_path = input('Enter the path: ')
print('You Entered:', folder_path)

sync_time = input("Enter the synchronization time period: ")

log_path = input("Enter the path to the log file: ")

# Define the folder path and file name
# Open log file in write mode

file_name = "log_file.txt"

# Get the file to the specific path
file_path = log_path + "/" + file_name

# Create the file
log_file = open(file_path, 'w')

# We define a function that does synchronization because we need backtracking
# for when we'll find a folder which has content, and probably subfolders
def folder_synchronization(source_dir, replica_dir):

    #Check if there already is content in replica directory
    replica_cont = os.listdir(replica_dir)
    if len(replica_cont) > 0:

        # Loop through the replica content to find what we need to keep and/or delete
        for item in replica_cont:

            # Path to the item in the source dir
            source_path = os.path.join(source_dir, item)

            # Path to the item in the replica dir
            replica_path = os.path.join(replica_dir, item)

            # Verify if this item is in the source folder too
            if os.path.exists(source_path) == False:

                # If it doesnt exist, delete it
                # Check if this is a file or directory
                if os.path.isfile(replica_path):
                    os.remove(replica_path)
                    print(item, "got deleted from", replica_dir)
                    log_file.write("{} got deleted from {}\n".format(item, replica_dir))

                elif os.path.isdir(replica_path):
                    shutil.rmtree(replica_path)
                    print(item, "got deleted from", replica_dir)
                    log_file.write("{} got deleted from {}\n".format(item, replica_dir))

    # We loop through the source directory to copy its content to the replica directory
    # I chose to sort the content such as files will be the first to copy and then the folders
    # Because I find cases which give me errors otherwise
    for item in sorted(os.listdir(source_dir), key=lambda x: os.path.isfile(x), reverse=True):

        # Path to the item, 'item' variable is just a string of the name of the file/directory
        path = os.path.join(source_dir, item)

        # Check if it is a file
        isFile = os.path.isfile(path)

        # Check if it's a folder
        isFolder = os.path.isdir(path)

        # If it's a file
        if isFile:

            # Check if it doesn't exist already in the replica folder
            if os.path.exists(os.path.join(replica_dir, item)) == False:
                shutil.copy(item, replica_dir)
                print(item, "was copied to:", replica_dir)
                log_file.write("{} was copied to: {}\n".format(item, replica_dir))

        # If it's a directory
        if isFolder:

            # Create an empty folder to the replica folder

            # Get the location where the folder needs to be created
            # When non empty folder is found call again the function

            # Get folder's path from source directory
            new_source_dir = source_dir + '\\' + item
            os.chdir(source_dir)

            # We check if we need Backtracking
            # By checking the length of content listed from the directory
            call = 0
            if len(os.listdir()) > 0:
                call = 1

            # Path where the new folder needs to be created in the replica directory
            os.chdir(replica_dir)

            # Create the empty folder only if it doesnt exist already
            # Because it could already be in the replica folder
            if os.path.exists(os.path.join(replica_dir, item)) == False:
                os.mkdir(item)
                print("Folder", item, "was created to", os.path.join(replica_dir, item))
                log_file.write("Folder {} was created to: {}\n".format(item, os.path.join(replica_dir, item)))

            # Update the path to the replica folder
            # We will call the function again if we found the non-empty folder
            new_replica_dir = replica_dir + "\\" + item

            # Go to the source folder that needs to be checked for content
            os.chdir(new_source_dir)

            # If we need to call the function again
            # We will do so by giving the new paths for the source folder and the replica folder
            if call == 1:
                folder_synchronization(new_source_dir, new_replica_dir)


# Current directory
os.chdir(folder_path)
root = os.getcwd()

os.chdir("replica")
replica = os.getcwd()

# The replica folder
replica_dir = replica

# Look into source folder
source_dir = root + "\source"
os.chdir(source_dir)

print("Folder source:", os.listdir())

# Every 'sync_time' seconds the synchronization of folders happens
while True:
    time.sleep(int(sync_time))
    print(sync_time, " has passed...")
    folder_synchronization(source_dir, replica_dir)

    # Request input from the user
    user_input = input("Press 'f' to quit or enter to continue: ")

    # Check if user wants to quit
    if user_input == 'f':
        break

#folder_synchronization(source_dir, replica_dir)

# Now go to the replica folder
os.chdir(root + "/replica")

print("Folder replica:", os.listdir())

log_file.close()