from flask import Flask, request
from flask_restful import Resource, Api, reqparse
import json

app = Flask(__name__)
api = Api(app)

beers = []

def addBeer(style, brewer, product):
    beers.append({"brewer": brewer, "product": product, "style": style})
    
addBeer("Pilsner", "Pilsner Urquell", "Pilsner Urquell")
addBeer("Pilsner", "Stella Artois", "Stella Artois")
addBeer("Pilsner", "Stiegl", "Pils")
addBeer("Pilsner", "Trummer", "Pils")
addBeer("Pilsner", "Two Roads", "Ol' Factory Pils")

addBeer("Stout", "Victory", "Donnybrook Stout")
addBeer("Stout", "Deschutes", "Obsidian Stout")
addBeer("Stout", "Brooklyn", "Black Chocolate Stout")
addBeer("Stout", "4 Hands", "Chocolate Milk Stout")

addBeer("IPA", "Founders", "All Day IPA")
addBeer("IPA", "Two Roads", "Lil Heaven")
addBeer("IPA", "Bells", "Two Hearted")
addBeer("IPA", "Temperance", "Gatecrasher")

addBeer("Double IPA", "Two Roads", "Road 2 Ruin")
addBeer("Double IPA", "The Alchemist", "Heady Topper")
addBeer("Double IPA", "Russian River", "Pliny the Elder")
addBeer("Double IPA", "Lagunitas", "Hop Stoopid")

# Helper functions for manipulating the list of beers
def styles():
    return list(set([b["style"] for b in beers]))   # set selects only unique values

def pilsners():
    return [b for b in beers if b["style"] == "Pilsner"]
    
def stouts():
    return [b for b in beers if b["style"] == "Stout"]

def ipas():
    return [b for b in beers if b["style"] == "IPA"]
    
def dipas():
    return [b for b in beers if b["style"] == "Double IPA"]


def brewers():
    return [b["brewer"] for b in beers]

# Rest, but adhering to format required for API.ai
class Alexa(Resource):
    def get(self):          

        return beers;
        #payload = request.get_json()
        
        # some debugging controls
        #print 'action: ' + payload['result']['action']        
        #print 'parameters: ' + json.dumps(payload['result']['parameters'])
        #print json.dumps(payload, indent=4, separators=(',', ':'))

        #
        # Beer.List 
        #   User requested a list of beers served
        #
        if payload['result']['action'] == 'Beer.List':
            # Check to see if a particular style was requested
            if 'style' in payload['result']['parameters']:
                style = payload['result']['parameters']['style']
                blist = [b for b in beers if b['style'] == style]
                speech = 'For ' + style + 's I have '
            else:
                style = ''
                speech = 'On tap I have '
                blist = beers
           
            for beer in blist[:-1]:
                if beer['brewer'] == beer['product']:
                    speech += beer['brewer'] + ', '
                else:
                    speech += beer['brewer'] + ' ' + beer['product'] + ', '
            speech += 'and ' + blist[-1]['brewer'] + ' ' + blist[-1]['product'] + '. '   # pretty up the last one
            speech += 'Now, what can I get you?'                            # Webhook m/provide all text
            
            return {
                "speech": speech,
                "displayText": speech,
                # "data": data,
                # "contextOut": [],
                "source": "bartender service"
            }


api.add_resource(Alexa, '/alexa')
        
if __name__ == '__main__':
    app.run(debug=True)