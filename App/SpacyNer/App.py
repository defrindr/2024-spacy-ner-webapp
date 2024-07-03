import spacy
from spacy.scorer import Scorer
from spacy.training import Example
import json
import math


class SpacyNer:
    app = None
    nlp = None
    training_annotations = None
    test_annotations = None

    def __init__(self):
        self.nlp = spacy.load('./App/SpacyNer/models/model-last/')

    def init_app(self, app):
        self.app = app
        self.getSampleData()

    def getSampleData(self):
        # Load training data
        list_data = []
        with open("./App/SpacyNer/resources/annotations.json", 'r') as f:
            list_data = json.load(f)

        # Ambil hanya annotation
        annotations = list_data['annotations']

        # dapatkan total jumlah annotation
        len_annotations = len(annotations)
        print(f"Jumlah annotations adalah {len_annotations}")

        # split annotation menjadi 8:2
        len_training_annotations = math.floor(len_annotations * .8)
        self.training_annotations = annotations[:len_training_annotations]
        self.test_annotations = annotations[len_training_annotations:]
        print(f"Jumlah training annotations adalah {len_training_annotations}")
        print(f"""Jumlah test annotations adalah {
              len_annotations-len_training_annotations}""")

    def checkProgram(self):
        for text, annotations in test_annotations:
            doc_pred = nlp(text)
            example = Example.from_dict(doc_pred, annotations)
            examples.append(example)

        scorer = Scorer(nlp)
        scores = scorer.score(examples)

        print(f"Precision = {scores['ents_p']}")
        print(f"Recall = {scores['ents_r']}")
        print(f"F1-Score = {scores['ents_f']}")
        print(f"""Accuracy = {
            self.evaluate_ner(self.nlp, self.test_annotations)
        }""")

    def get_entities(self, doc):
        return [(ent.text, ent.start_char, ent.end_char, ent.label_) for ent in doc.ents]

    def evaluate_ner(self, model, test_data):
        correct_entities = 0
        total_entities = 0

        for text, annotations in test_data:
            true_entities = annotations['entities']
            total_entities += len(true_entities)

            doc = model(text)
            pred_entities = get_entities(doc)

            for entity in pred_entities:
                ent = []
                ent.append(entity[1])
                ent.append(entity[2])
                ent.append(entity[3])
                if ent in true_entities:
                    correct_entities += 1

        entity_accuracy = correct_entities / total_entities if total_entities > 0 else 0
        return entity_accuracy
