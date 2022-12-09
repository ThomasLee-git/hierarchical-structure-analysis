#!/bin/bash

input_root="/tmp/thomas_ramdisk/hooktheory_deserialized_patterns"
output_root="/tmp/thomas_ramdisk/hooktheory_analyzed_patterns"
analyzer_path="/home/thomas/git/github/pattern_analyzer/_build/test_main"
declare -a input_dir_list=($(ls "${input_root}"))
# printf "${input_dir_list}"
for d in "${input_dir_list[@]}"; do
    # printf "$d" && exit 1
    src_dir="${input_root}/${d}"
    dst_dir="${output_root}/${d}"
    mkdir -p "${dst_dir}"
    ${analyzer_path} ${src_dir} ${dst_dir} || exit 1
done
