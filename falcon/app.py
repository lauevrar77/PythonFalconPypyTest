import falcon
import random


class NumbersResource:
    def on_get(self, req, resp):
        """Handle GET requests."""
        numbers = []

        # This code is intentionnaly ugly in order to test falcon + pypy
        # compared to flask restful + pypy
        for _ in range(10):
            for _ in range(100):
                for _ in range(500):
                    numbers.append(random.randint(0, 1000000))

        resp.media = numbers


api = falcon.API()
api.add_route("/numbers", NumbersResource())
