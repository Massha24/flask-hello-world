from flask import Flask, render_template
from appwrite.client import Client
from appwrite.services.databases import Databases

client = Client()
client.set_endpoint('https://cloud.appwrite.io/v1')
client.set_project('flaskblog')
client.set_key('standard_17d6ea4573319f02f18515422638e561ab1115fcd2ccba8f8cd747deb58a022fd47d66415af68aec3503e2c36517f3a73c0bc7e06660179461416a9d2010424ab69c4fc3fe0fc19ab2eb7b3d9607b69a805834487ca165072495b0a7ee93669fc941912678a89215bb8fdd4da74630ca0171a102f19c8abe0cfca5a43d5d2117')

databases = Databases(client)

app = Flask(__name__)


@app.route("/")
def main():
    data = databases.list_documents(
        database_id="flaskblog",
        collection_id="posts"
    )
    print(data)
    return render_template("home.html", posts=data.get("documents"))

@app.route("/<id>")
def post(id):
    data = databases.get_document(
        database_id="flaskblog",
        collection_id="posts",
        document_id=id
    )
    print(data)
    print(id)
    return render_template("post.html", post=data)

