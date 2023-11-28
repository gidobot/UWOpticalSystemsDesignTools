# bash script to iterate over files in directory, extract file name, and call script with file name as argument
# Usage: bash experiment_batch_process.sh <path to data files> <path to output directory>

# Set variables
data_path=$1
output_path=$2
# Iterate over files in directory
for file in $data_path/*
do
    # Extract file name without extension
    filename=$(basename $file)
    # remove extension from filename
    exposure=${filename%.*}
    # Print file name
    echo "Processing $filename"
    # Call script with file name as argument
    echo "python3 raytracer.py -i $file -e $exposure -s $output_path" -q
    python3 raytracer.py -i $file -e $exposure -s $output_path -q
done