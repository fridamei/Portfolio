#!/bin/bash

function tracker() {
   if [[ -z "$LOGFILE" ]]; then # Check if LOGFILE-variable is of zero length, in which case is set
      export LOGFILE=~/.local/share/.timer_logfile
   fi 

   case "$1" in 
      start) 
         if [[ $(tail -n1 $LOGFILE | cut -d' ' -f1) == "LABEL" ]]; then # Check if the first word of the last sentence is LABEL (then the previous task is still running)
            echo "Error. A process is already running"
         else # Update logfile with date and label
            echo -e "Started process $2" 
            echo -e "\nSTART $(date)\nLABEL $2" >> $LOGFILE
            
         fi
      ;;
     
      stop)
         if [[ $(tail -n1 $LOGFILE | cut -d' ' -f1) == "LABEL" ]]; then
            echo "Ended process: $(tail -n1 $LOGFILE | cut -d' ' -f2-)"
            echo -e "END $(date)" >> $LOGFILE
        else 
            echo "No process is currently running"
         fi
      ;;
      
      status)
         if [[ $(tail -n1 $LOGFILE | cut -d' ' -f1) == "LABEL" ]]; then # If first word of last sentence in file is LABEL, we are running an unfinished process
            echo "The following process is running: $(tail -n1 $LOGFILE | cut -d' ' -f2-)"
         
         elif [[ $(tail -n1 $LOGFILE | cut -d' ' -f1) == "END" ]]; then
            echo "No process is currently running"
         else
            echo "Error, please consult logfile"
         fi
      ;;
      
      
      log)
         while read line
         do
            if [[ $(echo $line | cut -d " " -f1) == "START" ]]; then
               start=$(echo $line | cut -d " " -f2-)
            
            elif [[ $(echo $line | cut -d " " -f1) = "LABEL" ]]; then
               label=$(echo $line | cut -d " " -f2-)
               
            elif [[ $(echo $line | cut -d " " -f1) = "END" ]]; then
               end=$(echo $line | cut -d " " -f2-)
               
               seconds_end=$(date --date "$end" +%s)
               seconds_start=$(date --date "$start" +%s)
               
               diff=$((seconds_end-seconds_start))
               readable=$(date -ud "@$diff" +'%H:%M:%S') # Convert back to hh:mm:ss (can replace : with descriptive text if wanted)
               
               echo "${label}: $readable"
            fi
            
         done < $LOGFILE
      ;;
      
      *) echo -e "\nTo use the time tracker, please enter one of the following in the command line: \"tracker start + label\" to start new task, \"tracker status\" to see current status, \"tracker stop\" to end current task or \"tracker log\""
   esac
}

tracker $@