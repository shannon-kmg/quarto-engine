#!/bin/sh
echo "" > outputs.txt
for i in $(seq 100); do python3 game.py >> outputs.txt; done
echo "Q: $(grep -c "Q won!" outputs.txt)"
echo "G: $(grep -c "G won!" outputs.txt)"
