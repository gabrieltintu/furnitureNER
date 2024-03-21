# Load a spacy model and chekc if it has ner
from __future__ import unicode_literals, print_function
import random
from pathlib import Path
import spacy
from tqdm import tqdm
from pathlib import Path
from spacy.tokens import Doc
from spacy.training import Example
import random
from pathlib import Path
from training_data.data import TRAIN_DATA


nlp = spacy.load('./trained')

output_dir=Path("./")

n_iter=300

if 'ner' not in nlp.pipe_names:
    ner = nlp.add_pipe('ner', last=True)
else:
    ner = nlp.get_pipe('ner')
    
    
for _, annotations in TRAIN_DATA:
    for ent in annotations.get('entities'):
        ner.add_label(ent[2])

other_pipes = [pipe for pipe in nlp.pipe_names if pipe != 'ner']
with nlp.disable_pipes(*other_pipes):
    optimizer = nlp.begin_training()
    for itn in range(n_iter):
        print("Iteration number: ", itn)
        random.shuffle(TRAIN_DATA)
        losses = {}
        for text, annotations in tqdm(TRAIN_DATA):
            doc = nlp.make_doc(text)
            example = Example.from_dict(doc, annotations)

            nlp.update(
                [example],  
                drop=0.5,  
                sgd=optimizer,
                losses=losses)
        print(losses)

nlp.to_disk('./trained_improved/')
