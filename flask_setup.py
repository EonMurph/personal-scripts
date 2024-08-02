import os
import subprocess

cwd = os.getcwd()

if not os.path.exists(f"{cwd}/.flaskenv"):
    with open(".flaskenv", "w") as outFile:
        lines = ["FLASK_APP=app.py\n", "FLASK_DEBUG=TRUE"]
        outFile.writelines(lines)

if not os.path.exists(f"{cwd}/app.py"):
    with open("app.py", "w") as outFile:
        lines = ["from flask import Flask, render_template\n\n", "app = Flask(__name__)\n", 'app.config["SECRET_KEY"] = "this-is-my-secret-key"\n\n']
        outFile.writelines(lines)

if not os.path.exists(f"/templates/"):
    os.mkdir("templates")
    
    with open("templates/base.html", "w") as outFile:
        pass


subprocess.run(["code.cmd", "."])
subprocess.run(["code.cmd", "app.py"])