#!/bin/bash

# Execute first_train.py
echo "Executing first_train.py..."
python first_train.py

# Execute improved_training.py
# echo "Executing improved_training.py..."
# python improved_training.py

# Execute extract.py
echo "Executing extract.py..."
python extract.py

# Execute ner_test.py
echo "Executing ner_test.py..."
python ner_test.py

echo "Script execution completed."