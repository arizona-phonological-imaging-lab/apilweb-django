import json
from tracer.forms import TraceForm
from django.shortcuts import render, render_to_response

def trace(request):
    print(request)
    print(type(request))
    # trace set meta data
    form = TraceForm()
    if request.method == 'POST' and form.validate():
        form = request.form

        data = dict()
        #we'll write json
        try:
            data['trace-data'] = json.loads(form['data'])
            print("{0} traces found.".format(len(data['trace-data'])))
        except:
            print("No traces found!")

        num_files = len(data.get('trace-data',[]))

        data['tracer-id'] = form['name']
        data['subject-id'] = form['subject']
        data['project-id'] = form['project_id']
        data['roi'] = form['roi']

        flash("Got {0}'s {1} trace data for {2} files!".format(data['subject-id'], data['project-id'], num_files))
        return Response(json.dumps(data),
                           mimetype="text/plain",
                           headers={"Content-Disposition":
                                        "attachment;filename={0}".format('traces.json')})
    #must be a GET...
    return render_to_response('draw.html', {"title": "Trace",
     "form": form})
