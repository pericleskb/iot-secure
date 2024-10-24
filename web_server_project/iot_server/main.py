from measurementsSubscriber import MeasurementsSubscriber
from files.createDefaultFiles import create_certificates_conf_file

create_certificates_conf_file()
MeasurementsSubscriber().start_subscribe_loop()


