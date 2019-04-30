#!/bin/bash

#use javac to compile the code first

#then curl or wget the txt file and store in appropariate file name (common.cfg here).
curl   https://www.cise.ufl.edu/~kiana/common.cfg_.txt > Common.cfg

curl   https://www.cise.ufl.edu/~kiana/PeerInfo.cfg_.txt > PeerInfo.cfg

#curl url_for_whatever > whatever

#run the program (peerProcess) with this common.cfg file
#java test common.cfg
