from flask import Flask, render_template

from dashboard_api import dashboard_api

app = Flask(
    __name__,
    template_folder="../templates",
    static_folder="../static"
)

# Regista a API REST
app.register_blueprint(dashboard_api)


###########################################################
# Dashboard
###########################################################

@app.route("/")
def dashboard():

    return render_template("index.html")


###########################################################
# Main
###########################################################

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True,
        use_reloader=False,
        threaded=True
    )
