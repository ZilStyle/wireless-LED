from flask import Flask, render_template
import time
import socket

#Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Bind the server socket to the client port
server_address = ('197.220.147.52', 10002)
sock.bind(server_address)

#Listen for the incomming connections
sock.listen(5)

try:
    while True:
        #wait for a connection from client
        print('waiting for a connection...')
        connection, client_address = sock.accept()

        #print client details
        print('connection from %s:%d' % client_address)

        try:
            while True:
                app = Flask(__name__)

                @app.route('/profile')
                def profile():
                    return render_template('profile.html')

                #background process happening without any refreshing
                @app.route('/background_process_test')
                def background_process_test():
                    msg = '1'
                    connection.send((msg.encode()))
                    time.sleep(1)
                    return "nothing"

                @app.route('/background_process_test1')
                def background_process_test1():
                    msg = '0'
                    connection.send((msg.encode()))
                    time.sleep(1)
                    return "nothing"

                if __name__ == "__main__":
                    app.run()

        finally:
            connection.close()
except KeyboardInterrupt:
    print('exiting')

finally:
    sock.shutdown(socket.SHUT_RDWR)
    sock.close()
    