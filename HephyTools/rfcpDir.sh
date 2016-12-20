#!/bin/bash
###################################################
#TO DO: check that you can run this script several times without cross deleting files
###################################################

contains() {
    string="$1"
    substring="$2"
    if test "${string#*$substring}" != "$string"
    then
        return 0    # $substring is in $string                                                                                   
    else
        return 1    # $substring is not in $string                                                                               
    fi
}

if [ $# -gt 0 ]; then
  dir=${1}
  localDir=${2}
  copyFiles=${3:-0}
  extractNumber=${4:-0}
else
  echo "No input dir given"
  exit
fi

if [[ "$copyFiles" = 1 ]]; then
#mkdir $2
    if [ -d "$localDir" ]; then
	echo "Given directory already exists!"
    else 
	mkdir $localDir
    fi

    ind=0
    total=`dpns-ls $dir | wc -l`
    echo Number of subdirectories: $total
    for j in `seq 1 $total`; do
	ctr=0
	for i in `dpns-ls ${dir}000$((j-1))`; do 
	    echo $i
	    let ctr=$ctr+1
	    if [[ ! -s $i ]]; then #true if file exists and size>0
		if [[ $i == "tree"* ]]
		then
		    ind0="$ind"
		    echo $ctr / `dpns-ls ${dir}000$((j-1)) | wc -l` : $i
		    echo $LCG_LOCATION

		    if [ $ind -lt 1000 ]; then ind0="0${ind}"; fi
		    if [ $ind -lt 100 ]; then ind0="00${ind}"; fi
		    if [ $ind -lt 10 ]; then ind0="000${ind}"; fi
		    echo $i
		    lcg-cp srm://hephyse.oeaw.ac.at${dir}000$((j-1))/$i ${localDir}tree_unmerged_${ind0}.root
		    echo ${localDir}tree_unmerged_${ind0}.root
		    let ind=$ind+1
		fi
  #else
  #  if [ $# -lt 2 ]; then echo $ctr / $total : $i  --- skipping, already exists; fi
	    fi
	done
    done

    total=`ls $localDir | wc -l`
    ind=0
    if [ $((${total}%10)) != 0 ]; then
	for i in `seq 1 $((total/10+1))`; do
	    ind0="$ind"
	    
	    if [ $ind -lt 100 ]; then ind0="0${ind}"; fi
	    if [ $ind -lt 10 ]; then ind0="00${ind}"; fi
	    
	    hadd ${localDir}tree_merged_${ind0}.root ${localDir}tree_unmerged_${ind0}*
	    rm ${localDir}tree_unmerged_${ind0}*
	    
	    let ind=$ind+1

	done
	
    else
	for i in `seq 1 $((total/10))`; do
            ind0="$ind"
	    
            if [ $ind -lt 100 ]; then ind0="0${ind}"; fi
            if [ $ind -lt 10 ]; then ind0="00${ind}"; fi
	    
            hadd ${localDir}tree_merged_${ind0}.root ${localDir}tree_unmerged_${ind0}*
            rm ${localDir}tree_unmerged_${ind0}*
	    
            let ind=$ind+1

	done
    fi

fi



if [[ "$extractNumber" = 1 ]]; then
    weight=0
    total=`dpns-ls $dir | wc -l`
    for j in `seq 1 $total`; do
        ctr=0
        for i in `dpns-ls ${dir}000$((j-1))`; do
            if [[ $i == "SkimReport"* ]]; then
                echo $i
                lcg-cp srm://hephyse.oeaw.ac.at${dir}000$((j-1))/$i SkimReport_tmp.txt
                while IFS='' read -r line || [[ -n "$line" ]]; do
                    if [[ $(contains "$line" "Sum Unity Weights"; echo $?) -eq 0 ]];then
                      #echo $line                                                                                                                                                                                                                                                                                  
                        weight_tmp=`echo $line | awk -F '[^0-9*]+' '{OFS=" "; for(i=1; i<=2; ++i) if ($i != "") print($i)}'`
                        weight="$(($weight+weight_tmp))"
                    fi
                done < "SkimReport_tmp.txt"
                rm SkimReport_tmp.txt
                echo "Number of events after file $i:"
                echo $weight
            fi
        done
    done

    echo "Total number of weighted events in $dir: $weight"

fi





