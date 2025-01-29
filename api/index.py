from flask import Flask, render_template, request, redirect
from appwrite.client import Client
from appwrite.services.databases import Databases
from appwrite.id import ID
from flask_wtf import Form
from wtforms import StringField


class Wtf(Form):
    title = StringField("title")
    author = StringField("author")
    authorImage = StringField("authorImage")
    content = StringField("content")
    titleImage = StringField("titleImage")
    description = StringField("description")


client = Client()
client.set_endpoint('https://cloud.appwrite.io/v1')
client.set_project('flaskblog')
client.set_key(
    'standard_17d6ea4573319f02f18515422638e561ab1115fcd2ccba8f8cd747deb58a022fd47d66415af68aec3503e2c36517f3a73c0bc7e06660179461416a9d2010424ab69c4fc3fe0fc19ab2eb7b3d9607b69a805834487ca165072495b0a7ee93669fc941912678a89215bb8fdd4da74630ca0171a102f19c8abe0cfca5a43d5d2117')

databases = Databases(client)

app = Flask(__name__)


@app.route("/")
def main():
    data = databases.list_documents(
        database_id="flaskblog",
        collection_id="posts"
    )

    return render_template("home.html", posts=data.get("documents"))

@app.route("/<id>")
def post(id):
    data = databases.get_document(
        database_id="flaskblog",
        collection_id="posts",
        document_id=id
    )

    return render_template("post.html", post=data)

@app.route("/add-post", methods=['GET', "POST"])
def addPost():
    form = Wtf(request.form)
    if request.method == 'POST' and form.validate():
        databases.create_document(
            database_id="flaskblog",
            collection_id="posts",
            document_id=ID.unique(),
            data={
                "title": form.title.data,
                "content": form.content.data,
                "author": form.author.data,
                "authorImage": form.authorImage.data,
                "titleImage": form.titleImage.data,
                "description": form.description.data
            }
        )
        return redirect("/")
    return render_template('addPost.html', form=form)


app.run(debug=True)
