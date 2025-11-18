from dotenv import load_dotenv
import os
from livekit import api
from flask import Flask
from flask_cors import CORS
load_dotenv()



app = Flask(__name__)


CORS(app)

@app.route('/getToken')
def getToken():
  token = api.AccessToken(os.getenv('LIVEKIT_API_KEY'), os.getenv('LIVEKIT_API_SECRET')) \
    .with_identity("identity") \
    .with_name("Eslam Walid") \
    .with_grants(api.VideoGrants(
        room_join=True,
        room="my-room",
    ))
  print(token.to_jwt())
  return token.to_jwt()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)