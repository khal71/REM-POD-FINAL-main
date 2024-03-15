from sense_hat import SenseHat
import socket
import time

sense = SenseHat()
server_port = 5000  # Make sure it matches the port in the client script

def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('0.0.0.0', server_port))

    while True:
        data, addr = server_socket.recvfrom(5000)
        distance_cm = float(data.decode())
        print('Received distance from client: {} cm'.format(distance_cm))
        

        distance_str = "{:.1f}".format(distance_cm)
        sense.show_message("D: "+ distance_str, text_colour=[0, 0, 255], scroll_speed=0.1)

        # Display temperature and magnetic field
        temperature = sense.get_temperature()
        temperature_str = "{:.1f}".format(temperature)
        print('Received temperature from Sensehat: {} celcius'.format(temperature_str))
        sense.show_message("T: "+ temperature_str, text_colour=[255, 0, 0], scroll_speed=0.1)
        
        north = sense.get_compass()
        north_str = "{:.1f}".format(north)
        sense.show_message("M: "+ north_str, text_colour=[0, 255, 0], scroll_speed=0.1)

if __name__ == "__main__":
    server()
