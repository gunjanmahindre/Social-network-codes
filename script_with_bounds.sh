#!/bin/bash
#normal_matrix_completion.py
#0 , 5, 10, 20, 40, 60, 80
#fraction = 0 #percentage of elements to be removed
#np.savetxt('nw_0.txt', dc, delimiter = '\t')
#run 7 times
#mean_error_ton.py
#Iteration_1
run=1
j=0
y=1
#rm -rf file_C.txt
#rm -rf file_A.txt

for x in $(eval echo "{1..$run}")
do
	for i in 20 40 60 80 90
	do
		echo "---------------------------------------------------------------------------------Iteration running is $x"
		echo "--------------------------------------------------------------------------------Percentage running is $i"
		sed -i "s|fraction = ${j}|fraction = ${i}|g" MC_with_bounds.py
		sed -i "s|Iteration_${y}|Iteration_${x}|g" MC_with_bounds.py
		#run script1
		~/anaconda3/bin/python3.6 MC_with_bounds.py
		j=$i
		y=$x
		if [ $i == 90 ]
		then
			sed -i "s|fraction = ${i}|fraction = 0|g" MC_with_bounds.py
			j=0
		fi
		if [ $x == $run ]
		then
			sed -i "s|Iteration_${x}|Iteration_1|g" MC_with_bounds.py
		fi
	done
done

# Calculate clustering coefficient
FILE=C_result_with_bound.txt
for a in 20 40 60 80 90
do
	c=`cat file_C.txt | grep "$a% " -c`
	total=0
	for b in $(eval echo "{1..$c}")
	do
		value=`cat file_C.txt | grep "$a% " -m$b | tail -n1 | rev | cut -d' ' -f1 | rev`
		total=`echo $total + $value | bc`
	done
	total=`echo $total / $c | bc -l`
	echo "$total" >> $FILE
done

# Calculate clustering coefficient
FILE2=A_result_with_bound.txt
for a in 20 40 60 80 90
do
	c=`cat file_A.txt | grep "$a% " -c`
	total=0
	for b in $(eval echo "{1..$c}")
	do
		value=`cat file_A.txt | grep "$a% " -m$b | tail -n1 | rev | cut -d' ' -f1 | rev`
		total=`echo $total + $value | bc`
	done
	total=`echo $total / $c | bc -l`
	echo "$total" >> $FILE2
done

# Calculate mean error
FILE3=mean_result.txt
for a in 20 40 60 80 90
do
	c=`cat file_mean.txt | grep "$a% " -c`
	total=0
	for b in $(eval echo "{1..$c}")
	do
		value=`cat file_mean.txt | grep "$a% " -m$b | tail -n1 | rev | cut -d' ' -f1 | rev`
		total=`echo $total + $value | bc`
	done
	total=`echo $total / $c | bc -l`
	echo "$total" >> $FILE3
done

# Calculate clustering coefficient
FILE4=hop_result.txt
for a in 20 40 60 80 90
do
	c=`cat file_abs.txt | grep "$a% " -c`
	total=0
	for b in $(eval echo "{1..$c}")
	do
		value=`cat file_abs.txt | grep "$a% " -m$b | tail -n1 | rev | cut -d' ' -f1 | rev`
		total=`echo $total + $value | bc`
	done
	total=`echo $total / $c | bc -l`
	echo "$total" >> $FILE4
done

# Calculate count value
FILE5=count_result.txt
for a in 20 40 60 80 90
do
	c=`cat file_count.txt | grep "$a% " -c`
	total=0
	for b in $(eval echo "{1..$c}")
	do
		value=`cat file_count.txt | grep "$a% " -m$b | tail -n1 | rev | cut -d' ' -f1 | rev`
		total=`echo $total + $value | bc`
	done
	total=`echo $total / $c | bc -l`
	echo "$total" >> $FILE5
done