import json
import random
import logging

def convert_data(FilePath):
    try:
        dataset = []
        lines=[]
        with open(FilePath, 'r', encoding="utf-8") as f:
            lines = f.readlines()

        for line in lines:
            data = json.loads(line)
            text = data['content']
            entities = []
            for annotation in data['annotation']:
               
                point = annotation['points'][0]
                labels = annotation['label']
                
                if not isinstance(labels, list):
                    labels = [labels]

                for label in labels:
                    entities.append((point['start'], point['end'] + 1 ,label))
            dataset.append((text, {"entities" : entities}))

        return dataset
    except Exception as e:
        logging.exception("Unable to process " + FilePath + "\n" + "error = " + str(e))
        return None

import spacy
import re

def trim_spaces(data: list) -> list:

    invalid_span_tokens = re.compile(r'\s')

    cleaned_data = []
    for text, annotations in data:
        entities = annotations['entities']
        valid_entities = []
        for start, end, label in entities:
            valid_start = start
            valid_end = end
            while valid_start < len(text) and invalid_span_tokens.match(
                    text[valid_start]):
                valid_start += 1
            while valid_end > 1 and invalid_span_tokens.match(
                    text[valid_end - 1]):
                valid_end -= 1
            valid_entities.append([valid_start, valid_end, label])
        cleaned_data.append([text, {'entities': valid_entities}])

    return cleaned_data


def train_test_model():

    TRAIN_DATA = convert_data("traindata.json")
    nlp = spacy.blank('en') 
    if 'ner' not in nlp.pipe_names:
        ner = nlp.create_pipe('ner')
        nlp.add_pipe(ner, last=True)
       

    TRAIN_DATA = trim_spaces(TRAIN_DATA)
   
    for _, annotations in TRAIN_DATA:
         for ent in annotations.get('entities'):
            ner.add_label(ent[2])
    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != 'ner']
    with nlp.disable_pipes(*other_pipes): 
        optimizer = nlp.begin_training()
        for itn in range(10):
            print("Statring iteration " + str(itn))
            random.shuffle(TRAIN_DATA)
            losses = {}
            
            for text, annotations in TRAIN_DATA:
                print(losses)
                nlp.update([text],  [annotations],  drop=0.2,  sgd=optimizer, losses=losses)
            print(losses)
    
    examples = convert_data("testdata.json")
    c=0        
    for text,annot in examples:

        f=open("validated_resumes/resume"+str(c)+".txt","w" , encoding="utf-8")
        doc_to_test=nlp(text)
        d={}
        for ent in doc_to_test.ents:
            d[ent.label_]=[]
        for ent in doc_to_test.ents:
            d[ent.label_].append(ent.text)

        for i in set(d.keys()):
            f.write(i +":")
            for j in set(d[i]):
                f.write(j.replace('\n','')+"\n")
        c+=1
train_test_model()


