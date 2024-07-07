import spacy
from spacy.scorer import Scorer
from spacy.training import Example
import json
import math
import csv
from spacy import displacy
import time


class SpacyNer:
    app = None
    nlp = None
    training_annotations = None
    test_annotations = None
    chart_wilayah = {}
    chart_kejahatan = {}

    def __init__(self):
        self.nlp = spacy.load('./App/SpacyNer/models/model-last/')

    def init_app(self, app):
        self.app = app
        self.getSampleData()
        self.checkProgram()

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
        examples = []
        for text, annotations in self.test_annotations:
            doc_pred = self.nlp(text)
            example = Example.from_dict(doc_pred, annotations)
            examples.append(example)

        scorer = Scorer(self.nlp)
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
            pred_entities = self.get_entities(doc)

            for entity in pred_entities:
                ent = []
                ent.append(entity[1])
                ent.append(entity[2])
                ent.append(entity[3])
                if ent in true_entities:
                    correct_entities += 1

        entity_accuracy = correct_entities / total_entities if total_entities > 0 else 0
        return entity_accuracy

    def predict_csv(self, source_file, target):
        self.resetChart()
        result = []
        with open(source_file, mode='r', encoding="utf8") as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                text = row['full_text']
                doc = self.nlp(text)
                entity = self.get_entities(doc)
                result.append({
                    'text': text,
                    'entities': entity
                })
                self.kategorikanWilayah(entity)
        with open(target, "w") as outfile:
            json.dump(result, outfile)

        return self.chart_wilayah

    def predict(self, source_file, target):
        self.resetChart()
        result = []
        with open(source_file, mode='r', encoding="utf8") as file:
            annotations = json.loads('\n'.join(file.readlines()))
            for annotation in annotations:
                doc = self.nlp(annotation['text'])
                entity = self.get_entities(doc)
                result.append({
                    'text': annotation['text'],
                    'entities': entity
                })
                self.kategorikanWilayah(entity)
                self.kategorikanKejahatan(entity)
        with open(target, "w") as outfile:
            json.dump(result, outfile)

        return {
            'wilayah': self.chart_wilayah,
            'kejahatan': self.chart_kejahatan,
        }

    def resetChart(self):
        self.chart_kejahatan = {
            'narkoba': 0,
            'pembunuhan': 0,
            'pemerkosaan': 0,
            'pencurian': 0,
            'penipuan': 0,
            'lainnya': 0
        }
        self.chart_wilayah = {
            'kabmalang': 0,
            'lowokwaru': 0,
            'klojen': 0,
            'blimbing': 0,
            'kedungkandang': 0,
            'sukun': 0,
        }

    def kategorikanWilayah(self, entity):
        wilayah = None
        for ent in entity:
            if ent[3] == 'LOCATION':
                lokasi = ent[0].lower()
                if "lowokwaru" in lokasi:
                    wilayah = "lowokwaru"
                    break
                elif "klojen" in lokasi:
                    wilayah = "klojen"
                    break
                elif "blimbing" in lokasi:
                    wilayah = "blimbing"
                    break
                elif "kedungkandang" in lokasi:
                    wilayah = "kedungkandang"
                    break
                elif "kedung kandang" in lokasi:
                    wilayah = "kedungkandang"
                    break
                elif "sukun" in lokasi:
                    wilayah = "sukun"
                    break

        if wilayah == None:
            self.chart_wilayah['kabmalang'] += 1
        else:
            self.chart_wilayah[wilayah] += 1

    def kategorikanKejahatan(self, entity):
        kejahatan = None
        for ent in entity:
            if ent[3] == 'CRIME':
                tindakan = ent[0].lower()
                if "curi" in tindakan:
                    kejahatan = "pencurian"
                    break
                if "maling" in tindakan:
                    kejahatan = "pencurian"
                    break
                if "hilang" in tindakan:
                    kejahatan = "pencurian"
                    break
                elif "obat" in tindakan:
                    kejahatan = "narkoba"
                    break
                elif "bandar" in tindakan:
                    kejahatan = "narkoba"
                    break
                elif "kurir" in tindakan:
                    kejahatan = "narkoba"
                    break
                elif "sabu" in tindakan:
                    kejahatan = "narkoba"
                    break
                elif "perkosa" in tindakan:
                    kejahatan = "pemerkosaan"
                    break
                elif "pemerkosaan" in tindakan:
                    kejahatan = "pemerkosaan"
                    break
                elif "cabul" in tindakan:
                    kejahatan = "pemerkosaan"
                    break
                elif "cabul" in tindakan:
                    kejahatan = "pemerkosaan"
                    break
                elif "bejat" in tindakan:
                    kejahatan = "pemerkosaan"
                    break
                elif "bunuh" in tindakan:
                    kejahatan = "pembunuhan"
                    break
                elif "tewas" in tindakan:
                    kejahatan = "pembunuhan"
                    break
                elif "penipu" in tindakan:
                    kejahatan = "penipuan"
                    break
                elif "tipu" in tindakan:
                    kejahatan = "penipuan"
                    break

        if kejahatan is not None:
            self.chart_kejahatan[kejahatan] += 1
        else:
            self.chart_kejahatan['lainnya'] += 1
