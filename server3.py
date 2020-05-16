
#!/usr/bin/env python3
"""
Very simple HTTP server in python for logging requests
Usage::
    ./server.py [<port>]
"""
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import simplejson
from urllib.request import FancyURLopener
from datetime import datetime


class S(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        self._set_response()
        self.wfile.write("GET request for {}".format(self.path).encode('utf-8'))

        home_coord = "-7.7545807,110.37433493" # Home
        work_coord2 = str(self.path) # Work

        lat = ""
        lon = ""
        for i in range(0,len(work_coord2)):
            if i >= 6 and i<=16:
                lat += work_coord2[i]
            elif i >= 22 and i<= 32:
                lon += work_coord2[i]
        #print(lat)
        #print(lon)

        #work_coord = lat,lon
        #print(work_coord)

        API1 = "AIzaSyCRXi115Ca-2IO6R03VpfYZq6ufvZ9rTcs"
        url_work2home = "https://maps.googleapis.com/maps/api/distancematrix/json?origins=" + lat + "," + lon + "&destinations=" + home_coord + "&mode=driving&traffic_model=best_guess&departure_time=now&language=en-EN&sensor=false&key=" + API1

        class MyOpener(FancyURLopener):
            version = 'My new User-Agent'
        myopener = MyOpener()
        result_work2home = simplejson.load(myopener.open(url_work2home))
        driving_time_seconds_work2home = result_work2home['rows'][0]['elements'][0]['duration_in_traffic']['text']
        print(datetime.now().strftime('%Y-%m-%d %H:%M') + ";" + str(driving_time_seconds_work2home) + ";" + "\n")

        target = open("Results.csv", 'a')
        target.write( datetime.now().strftime('%Y-%m-%d %H:%M') + ";" + str(driving_time_seconds_work2home) + ";"+ "\n")
        target.close()


    def do_POST(self):
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
                str(self.path), str(self.headers), post_data.decode('utf-8'))

        self._set_response()
        self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))


def run(server_class=HTTPServer, handler_class=S, port=8080):
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info('Starting httpd...\n')

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping httpd...\n')

if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
