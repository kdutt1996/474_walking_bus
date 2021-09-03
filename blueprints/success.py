from blueprints import app
from flask import render_template, request

@app.route('/success_grp_create')
def grpAdd():
    msg = request.args.get('msg')
    return render_template('addgroup.html', msg=msg)

@app.route('/success_grp_join')
def grpJoin():
    msg = request.args.get('msg')
    id = request.args.get('id')
    return render_template('joingrp.html', msg=msg, id=id)