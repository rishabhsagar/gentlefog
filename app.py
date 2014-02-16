import os
import requests
import xml.etree.ElementTree as ET

from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

app = Flask(__name__)
app.config.update(dict(
    DEBUG=False
    ))

@app.route('/')
def hello():
    raw_data = requests.get('http://en.wikipedia.org/w/api.php?action=parse&format=xml&page=Statistics&prop=links|wikitext&contentmodel=wikitext')
    ascii_data = raw_data.text.encode('ascii', 'ignore')
    xdoc = ET.fromstring(ascii_data)
    list_of_links = []

    for link in xdoc.iter('pl'):
        list_of_links.append(link.text)

    print "List of links has ", len(list_of_links)
    root = request.url_root
    return render_template('show_links.html', root=root, title="Statistics", list_of_links=list_of_links)

@app.route('/<topic>')
def show_topic(topic=None):
    if request.method == 'GET':
        payload = {'action':'parse', 'format':'xml', 'page':'sex', 'prop':'links'}
        payload['page']=topic
        wikilink = 'http://en.wikipedia.org/w/api.php'
        
        raw_data = requests.get(wikilink, params=payload).text
        ascii_data = raw_data.encode('ascii', 'ignore')
        xdoc = ET.fromstring(ascii_data)
    
        if ( xdoc.find('error') is not None):
            error = {}
            error['code'] = xdoc.find('error').attrib['code']
            error['summary'] = xdoc.find('error').attrib['info']
            return render_template('show_error.html', error=error)
        else:
            list_of_links = []
            root = request.url_root
            for link in xdoc.iter('pl'):
                list_of_links.append(link.text)
            list_of_links = filter(lambda link: ':' not in link, list_of_links)
            return render_template('show_links.html', root=root, title=topic, list_of_links=list_of_links)
    error = {}
    error['code'] = 'Invalid request type'
    error['summary'] = 'This page expects only GET type requests'
    return render_template('show_error.html', error=error)

if __name__ == '__main__':
    # Bind to PORT if defined, else default to 5000.
    port = int(os.environ.get('PORT', 5000))

    # Run the app.
    app.run(host='0.0.0.0', port=port)
