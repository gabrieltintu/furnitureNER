import spacy
import os

nlp = spacy.load("./trained_improved")

input_directory = "html_to_txt"
output_directory = "ner_output"

def apply_ner_model(text):
    doc = nlp(text)

    entities = [(ent.text, ent.label_) for ent in doc.ents]

    return entities

def read_text_files(directory, output_directory):
    for idx, filename in enumerate(os.listdir(directory), start=1):
        if filename.endswith(".txt") and filename != "not_working_urls.txt":
            input_file_path = os.path.join(directory, filename)
            output_file_path = os.path.join(output_directory, f"output_{idx}.txt")
            
            with open(input_file_path, "r", encoding="utf-8") as file:
                text = file.read()
            
            entities = apply_ner_model(text)
            
            # write the NER results to the output file
            with open(output_file_path, "w", encoding="utf-8") as file:
                for entity, entity_type in entities:
                    file.write(f"{entity} - {entity_type}\n")
            print(f"NER results for {input_file_path} saved to {output_file_path}")
  
read_text_files(input_directory, output_directory)
print("Testing NER done.")

