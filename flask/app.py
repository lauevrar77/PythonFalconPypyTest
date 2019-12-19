from flask import Flask
import random
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)


class Numbers(Resource):
    def get(self):
        numbers = []
        for _ in range(10):
            for _ in range(100):
                for _ in range(500):
                    numbers.append(random.randint(0, 1000000))

        return numbers


api.add_resource(Numbers, "/numbers")

if __name__ == "__main__":
    app.run(debug=True)
