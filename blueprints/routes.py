from blueprints import app
from flask import render_template, redirect, url_for, request, session
from datetime import date, datetime
import MySQLdb.cursors
import string
import mysql.connector

cnx = mysql.connector.connect(user="tnpham@walkingbus1", password="SFU_cmpt474_P", host="walkingbus1.mysql.database.azure.com", port=3306, database='walkingbus1')

#create route
@app.route('/createroute/<int:groupid>', methods=['GET', 'POST'])
def addroute(groupid):
    if request.method == 'POST' and 'sLat' in request.form and 'sLng' in request.form and 'dLat' in request.form and 'dLng' in request.form:
        sLat = request.form['sLat']
        sLng = request.form['sLng']
        dLat = request.form['dLat']
        dLng = request.form['dLng']
        # stime = request.form['stime']
        # etime = request.form['etime']
        current_date = date.today()
        end_date = date(2099,12,31)

        cnx.ping(True)
        cursor = cnx.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO Routes (StartPointLatitude, StartPointLongitude, EndPointlatitude, EndPointLongitude) VALUES (%s, %s, %s, %s);', [sLat, sLng, dLat, dLng])
        cnx.commit()
        cursor.execute('SELECT ID From Routes where StartPointLatitude = %s and StartPointLongitude = %s and EndPointlatitude = %s and EndPointLongitude= %s;', [sLat, sLng, dLat, dLng])
        result = cursor.fetchone()
        (routeID,) = result

        cursor.execute('INSERT INTO GroupRoutes (GroupID, RouteID, EffectiveStartDate, EffectiveEndDate) values (%s, %s, %s, %s);', [groupid, routeID, current_date, end_date])
        cnx.commit()
        cursor.close()
        successMsg = 'You have created route#' + str(routeID) + " successfully!"
        return redirect(url_for('showgrp', id=groupid, msg=successMsg))


    return render_template('route.html', groupid = groupid)