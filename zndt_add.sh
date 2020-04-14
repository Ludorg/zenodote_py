#!/bin/sh
. ../zndt_env/bin/activate
zndt_add_massive ()
  {
    while read line;
      do
        python3 app/add.py $line
      done < isbn_list.txt
  }

zndt_add_massive 
deactivate
