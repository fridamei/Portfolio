## Bash-script to move files

### Functionality
Moves files from one directory to another.

### Missing functionality
Both source and destination must be preexisting directories. 
Can not discriminate on file types. 


### Usage
Run chmod a+x to make the script executable
To move files run ./move "source directory" "destination directory"


## Task 2.1 a)

### Functionality
Moves files from one directory to another. Possible to specify file type, default is all file types

### Missing functionality
Both source and destination must be preexisting directories. 

### Usage
To move files run ./move "source directory" "destination directory" "file type"*
*Optional


Takes two (/three) arguments, where the two first are a source directory and the second a destination 
directory. The third argument is used for specifying the file type (if nothing is entered all file types are chosen).

The format of file type argument is .type, eg. .txt



## Task 2.1 b)

### Functionality
Moves files from one directory to another. Possible to specify file type, default is all file types.
Option to create destination directory if non-existing

### Missing functionality:
Can not choose different name than the directory argument when creating new directory


### Usage
Run chmod a+x to make the script executable
To move files run ./move "source directory" "destination directory" "file type"*
*Optional


Takes two (/three) arguments, where the two first are a source directory and the second a destination 
directory. The third argument is used for specifying the file type (if nothing is entered all file types are chosen).

The format of file type argument is .type, eg. .txt

If directory is non-existing, choose yes/y/Yes/Y or no/No/n/N to create directory or exit program, respectively.
Will loop until valid answer is provided.



## Task 2.1 b)

### Functionality
Moves files from one directory to another. Possible to specify file type, default is all file types.
Option to create destination directory if non-existing

### Missing functionality:
Can not choose different name than the directory argument when creating new directory.
The format of the date and time can not be chosen, but is given as YYYY-MM-DD-hh-mm 


### Usage
Run chmod a+x to make the script executable
To move files run ./move "source directory" "destination directory" "file type"*
*Optional


Takes two (/three) arguments, where the two first are a source directory and the second a destination 
directory. The third argument is used for specifying the file type (if nothing is entered all file types are chosen).

The format of file type argument is .type, eg. .txt

If directory is non-existing, choose yes/y/Yes/Y or no/No/n/N to create directory or exit program, respectively.
Will loop until valid answer is provided.

If option to create new directory is chosen, one is asked if the directory is to be named after
the current date and time. y will toggle this option, n will create directory with same name as entered destination argument. 
Invalid input will redirect the user to top of decision loop.



## Task 2.2

### Functionality
Lets the user manually log the start time and date and end time and date for processes (or other events)

### Missing functionality
Does not start or stop automatically when starting or ending a process. 

### Usage
source the file (source tracker.sh). The function can now be accessed directly from the command line 
by entering "tracker start "label"" to start logging an event, "tracker status" to view status of tracker or 
"tracker stop" to stop logging an event. 

The LOGFILE contains the path to the time log file. The file is created automatically upon running the script. 
The script checks if the environment varibale LOGFILE exists (by checking if it is of zero length) and 
creates it if it does not. 

## Task 2.3

### Functionality
Lets the user manually log the start time and date and end time and date for processes (or other events).
Echos duration of tasks

### Missing functionality
Does not start or stop automatically when starting or ending a process. 

### Usage
source the file (source tracker.sh). The function can now be accessed directly from the command line 
by entering "tracker start "label"" to start logging an event, "tracker status" to view status of tracker,
"tracker stop" to stop logging an event and "tracker log" to get duration of all run tasks. 

The LOGFILE contains the path to the time log file. The file is created automatically upon running the script. 
The script checks if the environment varibale LOGFILE exists (by checking if it is of zero length) and 
creates it if it does not. 
