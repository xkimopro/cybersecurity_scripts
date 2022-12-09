#!/bin/bash

# This is a script that detects and geolocates failed ssh attempts
# It then does a count aggregation per country
extend_csv_row_with_country(){
    for ROW in ${@}
    do 
        IP_ADDR=`echo $ROW | cut -d ',' -f2`
        COUNT=`echo $ROW | cut -d ',' -f1`
        COUNTRY=`geoiplookup $IP_ADDR | awk -F ','  '{ print $2 }' | awk '{ sub(/^[ \t]+/, ""); print }'`
        echo -e "${IP_ADDR}\t${COUNT}\t${COUNTRY}"
    done
    
}

# If number of arguments is different than 1. Wrong usage
if [ ${#} != 1 ] 
then    
    echo "Usage: ${0} FILENAME"
    exit 1
fi

# Fetch filename
FILENAME=${1}

# Check if filename exists
if [ ! -f "$FILENAME" ]; then
    echo "file ${0} does not exist"
    exit 1
fi
# Match IP Adresses Regex
# Count unique IP's and filter out counts less than 10
echo -e "IP_ADDRESS\tCOUNT\tCOUNTRY"
cat ${FILENAME} | grep -E -o "([0-9]{1,3}[\.]){3}[0-9]{1,3}" \
| sort | uniq -c | awk '$1 >= 10' | sort -nr | extend_csv_row_with_country `awk '{ print $1 "," $2 }'`

  



