#!/bin/bash

# Create the upload_files directory in the root of the project if it doesn't exist
upload_dir='upload_files'
if [ ! -d "$upload_dir" ]; then
    mkdir "$upload_dir"
fi

for file in unzipped_csv_files/*; do
    charset=$(file -I "$file" | grep -o 'charset=[^;]*' | cut -d= -f2)
    if [[ "$charset" == "iso-8859-1" ]]; then
        converted_file="${file%.csv}_converted.csv"
        iconv -f ISO-8859-1 -t UTF-8 "$file" -o "$converted_file" > /dev/null
        mv "$converted_file" "$upload_dir/"
    elif [[ "$charset" == "us-ascii" ]]; then
        mv "$file" "$upload_dir/"  # ASCII is compatible with UTF-8
    fi
done
