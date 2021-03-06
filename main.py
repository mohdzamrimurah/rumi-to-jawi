#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Import the Flask Framework
# from flask import Flask

from flask import Flask, session, redirect, url_for, escape, request
from flask import render_template
#from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.

# latest changes
latest_changes = "8-8-2020"


import codecs

import re

# read rumi jawi data
f = codecs.open("rumi-jawi-unicode.txt", mode="r", encoding='utf-8')
rjDict1 = {}
rjDict2 = {}
rjDict3 = {}

for line in f:
  line = line.strip()
  r, j = line.split(",")
  if r not in rjDict1:
    rjDict1[r] = j
  elif r not in rjDict2:
  	rjDict2[r] = j
  else:
  	rjDict3[r] = j

# read name data base
g = codecs.open("name-db.txt", mode="r", encoding='utf-8')
nDict = {}
for line in g:
  line = line.strip()
  r, j = line.split(",")
  nDict[r] = j


###norvig
alphabet = 'abcdefghijklmnopqrstuvwxyz'
def edits1(word):
  splits     = [(word[:i], word[i:]) for i in range(len(word) + 1)]
  deletes    = [a + b[1:] for a, b in splits if b]
  transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b)>1]
  replaces   = [a + c + b[1:] for a, b in splits for c in alphabet if b]
  inserts    = [a + c + b     for a, b in splits for c in alphabet]
  return set(deletes + transposes + replaces + inserts)
##
def edits2(word):
  return set(e2 for e1 in edits1(word) for e2 in edits1(e1))


# @app.route('/')
# def hello():
#     # """Return a friendly HTTP greeting."""
#     # return 'Hello World! Flask'
# def index():
#     return 'Index Page'

# @app.route('/')
# def index():
#     if 'username' in session:
#         return 'Logged in as %s' % escape(session['username'])
#     return 'You are not logged in'



@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, Nothing at this URL.', 404


# @app.errorhandler(500)
# def page_not_found(e):
#     """Return a custom 500 error."""
#     return 'Sorry, unexpected error: {}'.format(e), 500




@app.route('/transliterate', methods = ['POST'])
def transliterate():
    rumi = request.form['rumi']
    # print not working on browser
    #print "hello world"
    #print("The email address is in signup function '" + email + "'")

    # rumi.lower().strip() # have no effect!! 8/8/2020
    r = rumi.lower().strip()

    if r in rjDict1:
    	if r in rjDict2 and r in rjDict3:
    		return render_template('transliterate.html', rumi = r,
          jawi = rjDict1[r], jawi2 = rjDict2[r], jawi3 = rjDict3[r],
          latest_changes=latest_changes)
    	elif r in rjDict2:
    		return render_template('transliterate.html', rumi = r, jawi = rjDict1[r],
          jawi2 = rjDict2[r], latest_changes=latest_changes)
    	else:
    		return render_template('transliterate.html', rumi = r,
          jawi = rjDict1[r],latest_changes=latest_changes)
    else:
    	guest1 = edits1(r)
    	guest2 = []
    	for c in guest1:
    		if c in rjDict1:
    			guest2.append(c)
    	return render_template('not_found_transliterasi.html', rumi = r,
        guesses = guest2,latest_changes=latest_changes)
    # return pass
# set the secret key.  keep this really secret:

@app.route('/')
@app.route('/rumijawi')
def rumijawi():
	return render_template('rumijawi.html',latest_changes=latest_changes)

@app.route('/rumijawi_paragraph')
def rumijawi_paragraph():
	return render_template('rumijawi_paragraph.html',latest_changes=latest_changes)

@app.route('/transliterate_paragraph', methods = ['POST'])
def transliterate_paragraph():
    rumi = request.form['rumi']
    rumi = re.split('(\W+)',rumi)

    # print not working on browser
    #print "hello world"
    #print("The email address is in signup function '" + email + "'")

    punc =      ['.',',','?',':',';','-','(',')','!','`','"','“']
    punc_arab = ['.',',','؟',':','؛','-',')','(','!','’','"','"']


    paragraph_rumi = []
    paragraph_jawi = []
    rj = {}
    number_of_untransliterate = 0
    for r in rumi:
    	if r.lower().strip() == '':
    		continue
    	if r.lower().strip() == ' ':
    		continue
    	if r.lower() in rjDict1:
    		paragraph_rumi.append(r)
    		paragraph_jawi.append(rjDict1[r.lower()])
    		rj[r] = rjDict1[r.lower()]
    	elif r.strip() in punc:
    		paragraph_rumi.append(r.strip())
    		paragraph_jawi.append(punc_arab[punc.index(r.strip())])
    	else:
    		paragraph_rumi.append(r)
    		paragraph_jawi.append('؟'.decode('utf-8'))
    		number_of_untransliterate = number_of_untransliterate + 1

    return render_template('transliterate_paragraph.html',
      paragraph_rumi = paragraph_rumi,paragraph_jawi = paragraph_jawi,
      number_of_untransliterate = number_of_untransliterate,
      number_of_words = len(paragraph_jawi), latest_changes=latest_changes)
    # return pass

@app.route('/overview')
def overview():
	return render_template('overview.html', latest_changes=latest_changes)

@app.route('/teknikal')
def teknikal():
	return render_template('teknikal.html', latest_changes=latest_changes)


@app.route('/hubungi')
def hubungi():
    return render_template('hubungi.html',latest_changes=latest_changes)

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

@app.route('/nama')
def nama():
  return render_template('nama.html', latest_changes=latest_changes)

@app.route('/transliterate_name', methods = ['POST'])
def transliterate_name():

  rumi = request.form['rumi']
  rumi = re.split('(\W+)',rumi)

  name_rumi = []
  name_jawi = []
  guest2 = []

  for r in rumi:
    if r.lower().strip() == '':
    	continue
    if r.lower().strip() == ' ':
    	continue
    if r.lower() in nDict:
      name_rumi.append(r.lower())
      name_jawi.append(nDict[r.lower()])
    else:
      name_rumi.append(r.lower())
      name_jawi.append("?")
      guest1 = edits1(r.lower())

      for c in guest1:
    		if c in nDict:
    			guest2.append(c)


  return render_template('transliterate_name.html', name_rumi = name_rumi,
    name_jawi = name_jawi, guest2 = guest2)
