import flask
# import psycopg2
# from psycopg2 import connect
# from flask import request

app = flask.Flask(__name__)

@app.route("/create_room")
def create_room():
  ...
  # params = request.args.to_dict()
  # if (not (params.get("username") and params.get("fullname") and params.get("email") and params.get("password") and params.get("photo"))): 
  #   return "missing params"

  # with connect(**config) as conn:
  #   with conn.cursor() as cursor:
  #     for table in tables:
  #       cursor.execute(table)
  #     cursor.execute(f"insert into Users (username, fullname, email, password, photo) values ('{params['username']}', '{params['fullname']}', '{params['email']}', '{params['password']}', '{params['photo']}')")
  #     conn.commit()
  #     return app.redirect("/")
    
@app.route("/remove_room")
def remover_room():
  ...
  # id = request.args.get("id")
  # if (not id): return "missing params"

  # with connect(**config) as conn:
  #   with conn.cursor() as cursor:
  #     cursor.execute(f"delete from Users where id={id}")
  #     return app.redirect("/")

@app.route("/", methods=["GET"])
def dashboad():
  # with connect(**config) as conn:
  #   with conn.cursor() as cursor:
  #     cursor.execute("select * from Users")
  #     select = cursor.fetchall()
  # return flask.render_template("dashboard.html", len=len(select), users=(select))
  return flask.render_template("dashboard.html")

if __name__ == "__main__":
  app.run(debug=True)