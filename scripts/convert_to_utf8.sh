#!/bin/bash
upload_dir="upload_files"  # Define the upload directory
cd unzipped_csv_files/
for file in *; do
    charset=$(file -I "$file" | grep -o 'charset=[^;]*' | cut -d= -f2)
    if [[ "$charset" == "iso-8859-1" ]]; then
        converted_file="${file}_converted.csv"
        iconv -f ISO-8859-1 -t UTF-8 -c "$file" > "$converted_file" #> /dev/null 2>&1
        mv "$converted_file" "../$upload_dir/$file"
        rm -f "$file"
    elif [[ "$charset" == "us-ascii" ]]; then
        mv "$file" "../$upload_dir/"  # ASCII is compatible with UTF-8
    fi
done
# iconv -f LATIN1 -t utf-8 -c teste.csv -o teste_ok.csv > /dev/null 2>&1