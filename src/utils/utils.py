from json import JSONEncoder


class CustomEncoder(JSONEncoder):
    def default(self, obj):
        if hasattr(obj, 'to_json'):
            return obj.to_json()
        return obj.__dict__
