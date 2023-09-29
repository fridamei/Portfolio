#!/bin/bash

function move {
   src=$1
   dst=$2
   file_type=$3
   
   # Check if there are two or more arguments
   if ! [ "$#" -ge 2 ]; then
      echo $'\nImproper number of arguments. Please enter source folder as first argument and destination folder as second argument'
      exit
   fi
   
   # Check if entered source folder exists
   if ! [ -d "$1" ]; then
      echo $'\nThe source folder does not exist'
      exit
   fi    
      
   # Loop that runs until valid answer has been entered
   valid_ans=false
   while [ $valid_ans = false ]
   do
      if ! [ -d "$2" ]; then
         echo $'\nThe destination folder does not exist. Would you like to create one? (Yes/yes/Y/y or No/no/N/n)'
         read value
         
         # If yes
         if [ $value = Yes -o $value = yes -o $value = Y -o $value = y ]; then
            # Decide whether to name destination as current date or as argument
            echo $'\nName directory as current date and time (YYYY-MM-DD-hh-mm)? (y/n)'
            read ans
            
            # Create directory with date name
            if [ $ans = y ]; then
               date_time=$(date +%F-%H-%M-%S)
               echo $'\nYes has been chosen, directory $date_time has been created'
               mkdir $date_time
               
               mv -v "$src"/*"$file_type" "$date_time" || echo $'\nMove failed, please check that file type is entered correct (eg. "txt"). If no filetype is entered, all files will be moved'
               exit
            
            # Create directory with dst argument name
            elif [ $ans = n ]; then
               echo $'\nNo has been chosen, directory $dst has been created'
               mkdir $dst
               valid_ans=true
            
            # Else loop back to start of while loop
            else
               echo $'\nInvalid answer, choose y or n'
            fi
         
         # If no
         elif [ $value = No -o $value = no -o $value = N -o $value = n ]; then
            echo $'\nNo has been chosen, exiting program'
            exit
         
         # If invalid input loop back to start of while loop
         else
            echo $'\nInvalid answer. Please enter Yes/yes/Y/y for yes and No/no/N/n for no\n'
         fi
      else
         valid_ans=true
         
      fi
   done
   
   mv -v "$src"/*"$file_type" "$dst" || echo $'\nMove failed, please check that file type is entered correctly (eg. ".txt"). If no filetype is entered, all files will be moved'
}

move $@ # Run function with every argument entered in terminal
