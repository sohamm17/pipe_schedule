#!/bin/bash

pandoc README.md --pdf-engine=xelatex -o artifact.pdf
echo "Artifact PDF Instruction is generated: artifact.pdf."
