#!/usr/bin/env python
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler

import yaml
import json

import urlparse
import subprocess
import traceback

options = {}

class RequestHandler(BaseHTTPRequestHandler):
    # Run the payload for a project / ref
    def run_payload(self, project_key, project, ref, show_output = False):
        output = ['', '']

        try:
            if project.has_key(ref):
                cmd = 'trap \'echo "# $BASH_COMMAND"\' DEBUG && ' + (' && '.join(project[ref]))
                self.log_message('Got payload for %s (%s), running: %s', project_key, ref, cmd)
                output = subprocess.Popen(['/bin/bash', '-c', cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        except Exception as e:
            self.log_message('Error while running payload: %s', traceback.format_exc())
            self.send_error(400)
            return
        
        self.send_response(200)
        self.end_headers()
        
        if show_output:
            self.wfile.write("Output:\n")
            self.wfile.write(output[0])
            self.wfile.write("\nErrors:\n")
            self.wfile.write(output[1])

    # Handle GET (for manual deploys with secret key)
    def do_GET(self):
        url = urlparse.urlparse(self.path)
        project_key = url.path[1:]

        if not options['projects'].has_key(project_key):
            self.log_message('Invalid project')
            self.send_error(400)
            return
        
        project = options['projects'][project_key]
        query = urlparse.parse_qs(url.query)

        if not query.has_key('ref') or not query.has_key('secret'):
            self.log_message('Missing params')
            self.send_error(400)
            return

        ref = query['ref'][0]
        secret = query['secret'][0]
        
        if not project.has_key(ref) or options['secret'] != secret:
            self.log_message('Bad ref or secret')
            self.send_error(400)
            return
        
        self.run_payload(project_key, project, ref, True)

    # Handle POST (for GitHub push notifications)
    def do_POST(self):
        project_key = self.path[1:]

        if not options['projects'].has_key(project_key):
            self.log_message('Invalid project')
            self.send_error(400)
            return
        
        project = options['projects'][project_key]
            
        length = int(self.headers.getheader('content-length'))
        form = urlparse.parse_qs(self.rfile.read(length), keep_blank_values=1)

        payload = form['payload']
        
        if not payload:
            self.log_message('Missing payload')
            self.send_error(400)
            return

        payload = json.loads(payload[0])
        
        ref = payload['ref']
        if ref != 'refs/heads/master':
            self.log_message('Only master can be deployed via POST')
            send.response(200)
            return

        self.run_payload(project_key, project, ref)

if __name__ == '__main__':
    options = yaml.load(open('config.yml', 'r'))
    server = HTTPServer((options['host'], int(options['port'])), RequestHandler)
    server.serve_forever()
