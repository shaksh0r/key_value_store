class Store:
    def __init__(self):
        self.store = dict()
    
    def get(self,key):
        if self.store.get(key) is not None:
            return self.store.get(key)

        return "Key Not Found"

    def set(self, key,value):
        if self.store.get(key) is None:
            if value is not None:
                self.store[key] = value
                return "Success"
            else:
                return "No value provided"
        
        return "Key is already taken"

    def delete(self,key):
        value = self.store.pop(key, None)

        if value is None:
            return "The key doesn't exist"
        
        return value

