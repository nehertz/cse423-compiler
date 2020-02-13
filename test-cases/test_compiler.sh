#!/bin/bash
testsuite=`ls easy-suite`
for eachfile in $testsuite
do
   echo "Test File Name: '$eachfile'" >> result.out
   python3 ../main.py -p easy-suite/$eachfile >> result.out
   echo "********************************************************'" >> result.out
done


