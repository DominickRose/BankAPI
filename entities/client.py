#Represents a single client of the bank
class Client:
    def __init__(self, client_id: int, first_name: str, last_name: str):
        self.client_id = client_id
        self.first_name = first_name
        self.last_name = last_name

    def json(self):
        client = {
            'clientId': self.client_id,
            'firstName': self.first_name,
            'lastName': self.last_name,
        }
        return client

    @staticmethod
    def from_json(json):
        client = Client(0, "", "")
        client.client_id = json['clientId']
        client.first_name = json['firstName']
        client.last_name = json['lastName']
        return client