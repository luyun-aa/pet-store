import json
from flask import Flask, request
from flask.views import MethodView

app = Flask(__name__)
store = {}


class Index(MethodView):

    def get(self):
        return "Hello World from PetStore"


class Pets(MethodView):

    def get(self):
        return json.dumps(store)

    def post(self):
        pet_id = request.form['id']
        attrs = request.form.copy()
        del attrs['id']
        store[pet_id] = attrs
        return json.dumps(attrs)


class Pet(MethodView):

    def get(self, pet_id):
        return json.dumps(store.get(pet_id))

app.add_url_rule('/', view_func=Index.as_view('index'))
app.add_url_rule('/pets', view_func=Pets.as_view('pets'))
app.add_url_rule('/pets/<pet_id>', view_func=Pet.as_view('pet'))

if __name__ == "__main__":
    app.run(debug=True)
