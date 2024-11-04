from mqtt.measurements_publisher import MeasurementsPublisher
from mqtt.cipher_subscriber import CipherSubscriber

measurement_publisher = MeasurementsPublisher()
measurement_publisher.start_loop()

cipher_subscriber = CipherSubscriber()
cipher_subscriber.start_subscribe_loop()