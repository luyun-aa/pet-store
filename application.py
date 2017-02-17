import json
from flask import Flask, request, abort
from flask.views import MethodView

application = Flask(__name__)
store = {}
foods = {
    'cat': {
        'whiskas': {
            'price': '42.9'
        },
        'royal': {
            'price': '135.0',
        },
        'sharlovy': {
            'price': '38.0'
        }
    },
    'dog': {
        'orijen': {
            'price': '290.0',
        },
        'metz': {
            'price': '81.9',
        }
    }
}


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


class BuyPet(MethodView):

    def post(self):
        pet_id = request.form['id']
        if pet_id not in store:
            abort(400, description='Pet %d does not exist' % pet_id)
        pet = store[pet_id]
        pet['status'] = 'SOLD'
        msg = 'Pet sold: %s' % pet
        print msg
        return json.dumps({
            'message': msg
        })


class Foods(MethodView):

    def get(self):
        return json.dumps(foods)


class BuyFoods(MethodView):

    def post(self):
        food_type = request.form['type']
        if food_type not in foods:
            abort(400, 'invalid food type:' + food_type)
        avail_foods = foods[food_type]
        name = request.form['name']
        if name not in avail_foods:
            abort(400, 'invalid food name:' + name)
        food = avail_foods[name]
        quantity = int(request.form.get('quantity', 1))
        pay = float(food['price']) * quantity
        msg = 'Selling %d bags of %s(%s) worth %.2f$' % (quantity, name, food_type, pay)
        print msg
        return json.dumps({
            'message': msg
        })

application.add_url_rule('/', view_func=Index.as_view('index'))
application.add_url_rule('/pets', view_func=Pets.as_view('pets'))
application.add_url_rule('/pets/<pet_id>', view_func=Pet.as_view('pet'))
application.add_url_rule('/pets/buy', view_func=BuyPet.as_view('buy_pet'))
application.add_url_rule('/foods/', view_func=Foods.as_view('foods'))
application.add_url_rule('/foods/buy', view_func=BuyFoods.as_view('buy_foods'))

if __name__ == "__main__":
    application.run(debug=True)
