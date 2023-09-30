import json
from flask import Flask, render_template, request
from waitress import serve
from api.seek import SeekClient

app = Flask(__name__)
seek_client = SeekClient()


@app.route('/')
def index():
    '''
    Home page.
    '''
    return render_template('./index.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    '''
    Upload page.
    '''
    if not request.method == 'POST':
        return render_template('./upload.html', error='Please upload a file.')

    dmp = load_file(request)

    # 1. Create users for all contributors
    people = dmp['contributor']
    for i, person in enumerate(people):
        res = seek_client.create_person(person['name'], person['mbox'])

        people[i]['response'] = {
            'status_code': res.status_code, 'json': res.json()}

    # 2. Create a new project
    project = dmp['project'][0]
    res = seek_client.create_project(
        project['title'], project['description'], [(1, 1)])

    project['response'] = {
        'status_code': res.status_code, 'json': res.json()}

    return render_template('./upload.html', people=people, project=project)


def load_file(request):
    file = request.files['jsonFile']
    return json.load(file)['dmp']


if __name__ == '__main__':
    print('Server running at http://localhost:8080')
    serve(app, host='0.0.0.0', port=8080)
