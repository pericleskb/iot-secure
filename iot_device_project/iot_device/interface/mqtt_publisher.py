import queue
import threading

from mqtt.measurements_publisher import MeasurementsPublisher
from mqtt.cipher_subscriber import CipherSubscriber
from mqtt.device_connected_publisher import send_device_connected

class MqttPublisher:

    def __init__(self, device_name, password):
        self.device_name = device_name
        self.password = password
        self.value_queue = queue.Queue()
        self.cipher_subscriber = None
        self.stop_received = False

    def __start_cipher_subscriber(self):
        self.cipher_subscriber = CipherSubscriber(self.device_name, self.password)
        self.cipher_subscriber.start_subscribe_loop()

    def start_publishing(self):
        # start cipher subscriber in different thread to not block current execution
        # this subscriber will handle the measurements publisher
        cipher_subscriber_thread = threading.Thread(
            target=self.__start_cipher_subscriber)
        cipher_subscriber_thread.start()

        # publish device connected message, so that the server can respond with
        # the active cipher in cipher_subscriber
        # If the IoT Device Manager is not running during this time, it will publish
        # the active cipher at the time of its connection
        send_device_connected(self.password)

        while not self.stop_received:
            value = self.value_queue.get()  # Blocking until an item is available
            if value is None:
                break
            self.cipher_subscriber.add_value(value)

    def stop_publishing(self):
        self.stop_received = True
        self.value_queue.put(None)
        self.cipher_subscriber.stop()

    def add_value(self, value):
        self.value_queue.put(value)
