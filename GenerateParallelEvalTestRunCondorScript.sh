#!/bin/sh

mkdir -p parallel_run_output_evaltest

python2.7 src/GenerateParallelEvaluationScript.py D3 ./evaltest/QA2007_testset.xml ./parallel_run_output_evaltest/ parallel_run_all_evaltest.cmd

