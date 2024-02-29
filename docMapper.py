import json

class DocMapper:
    def __init__(self, mapping_file):
        self.mapping_file = mapping_file
        self.mapping = self.load_mapping()

    def load_mapping(self):
        try:
            with open(self.mapping_file, 'r') as f:
                # load dictionary from map
                return json.load(f)
        except FileNotFoundError:
            return {}

    def save_mapping(self):
        with open(self.mapping_file, 'w') as f:
            # dump updated dictionary to map
            json.dump(self.mapping, f)

    def add_mapping(self, doc):
        doc_id = len(self.mapping) + 1
        self.mapping[doc_id] = doc
        self.save_mapping()
        return doc_id

    def get_doc(self, doc_id):
        return self.mapping.get(doc_id)
