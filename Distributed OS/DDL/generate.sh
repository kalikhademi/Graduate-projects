#!/bin/bash

for ddl in *.ddl; do
	if parser/parser $ddl; then
		echo generated files for $ddl;
	else
		exit 1
	fi
done
exit 0
