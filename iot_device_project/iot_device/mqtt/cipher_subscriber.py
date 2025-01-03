import threading
import paho.mqtt.client as mqtt
import ssl

from files import file_util
from CipherSuites import is_cipher_suite
from mqtt.measurements_publisher import MeasurementsPublisher

class CipherSubscriber:
    """
        The cipher subscriber runs in a loop and handles the lifecycle of the
        measurements publisher thread. Every time a new cipher option is
        received, it will restart MeasurementsPublisher, providing it with
        the new cipher option.
    """
    def __init__(self, device_name, password):
        self.mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        # We wait to receive the current active cipher before
        # sending measurements
        self.active_cipher = None
        self.measurements_publisher_thread = None
        self.measurement_publisher = None
        self.device_name = device_name
        self.password = password

    def start_subscribe_loop(self):
        self.mqttc.on_connect = self.__on_connect
        self.mqttc.on_message = self.__on_message
        self.mqttc.on_subscribe = self.__on_subscribe
        self.mqttc.on_unsubscribe = self.__on_unsubscribe

        # if no ssl files defined, connect to the mqtt broker's http port
        port = 1883

        if file_util.should_use_ssl():
            # Certificates defined. Use ssl
            certs = file_util.read_certificate_conf_file()

            try:

                self.mqttc.tls_set(ca_certs=certs.get("ca_certs"),
                                   certfile=certs.get("certfile"),
                                   keyfile=certs.get("keyfile"),
                                   keyfile_password=self.password,
                                   ciphers=self.active_cipher,
                                   tls_version=mqtt.ssl.PROTOCOL_TLSv1_2)
                # ssl files defined, connect to the mqtt broker's https port
                port = 8883
            except ssl.SSLError:
                print("Unable to connect. "
                      "Please make sure you provided the correct password.")
                quit()

        self.mqttc.user_data_set([])
        self.mqttc.connect("raspberrypi.local", port)
        self.mqttc.loop_forever()
        print(f"Received the following message: {self.mqttc.user_data_get()}")

    def add_value(self, value):
        if self.measurement_publisher == None:
           return
        self.measurement_publisher.add_value(value)

    # methods to start and stop measurement subscriber loop on a different thread
    def __start_measurement_thread(self):
        self.measurements_publisher_thread = threading.Thread(target=self.__start_measurements)
        self.measurements_publisher_thread.start()

    def __stop_measurements(self):
        if self.measurement_publisher is not None:
            self.measurement_publisher.stop_loop()

    def __start_measurements(self):
        self.measurement_publisher = MeasurementsPublisher(self.active_cipher,
                                                           self.device_name,
                                                           self.password)
        self.measurement_publisher.start_loop()

    def stop(self):
        self.__stop_measurements()
        self.mqttc.loop_stop()

    # methods to handle mqtt events
    def __on_message(self, client, userdata, message):
        """
            After publishing to the device_connected topic we wait to receive
            the active cipher suite on.
            The first time we receive the cipher suite we start sending measurements.
            When we receive a new cipher, we need to stop all communication
            and change to the new cipher.
        """
        # userdata is the structure we choose to provide, here it's a list()
        userdata.append(message.payload)
        print(f"topic: set_cipher_suite, message received - {message.payload}")
        cipher = message.payload.decode("utf-8")
        # if the current cipher suite is not supported, stop sending measurements
        if not is_cipher_suite(cipher):
            print(f"Received not supported cipher - {message.payload}")
            self.active_cipher = None
            self.__stop_measurements()
            return

        # if the cipher contained in the message is different from the active
        # one, stop measurements and change to the new one
        if cipher != self.active_cipher:
            print("New cipher received")
            self.__stop_measurements()
            self.active_cipher = cipher
            self.__start_measurement_thread()

    def __on_subscribe(self, self1, userdata, mid, reason_code_list, properties):
        # Since we subscribed only for a single channel, reason_code_list contains
        # a single entry
        if reason_code_list[0].is_failure:
            print(f"Broker rejected you subscription: {reason_code_list[0]}")
        else:
            print(f"Broker granted the following QoS: {reason_code_list[0].value}")

    def __on_unsubscribe(self, self1, client, userdata, mid, reason_code_list, properties):
        # Be careful, the reason_code_list is only present in MQTTv5.
        # In MQTTv3 it will always be empty
        if len(reason_code_list) == 0 or not reason_code_list[0].is_failure:
            print("unsubscribe succeeded (if SUBACK is received in MQTTv3 it success)")
        else:
            print(f"Broker replied with failure: {reason_code_list[0]}")
        client.disconnect()

    def __on_connect(self,  client, userdata, flags, reason_code, properties):
        if reason_code.is_failure:
            print(f"Failed to connect: {reason_code}. loop_forever() will retry connection")
        else:
            # we should always subscribe from on_connect callback to be sure
            # our subscribed is persisted across reconnections.
            client.subscribe("set_cipher_suite", qos = 1)
