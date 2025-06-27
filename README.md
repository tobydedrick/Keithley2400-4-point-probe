# Keithley2400-4-point-probe
Python scripts for performing 4-point probe IV measurements with 2x Keithley 2400 SourceMeters. Communication is via the serial ports.

The program 'four_point_probe_data_collector.py' is used for data collection; it produces a CSV file containing the measured data, plus information about the experiment. Within the program the user can specify experimental parameters.

The program 'four_point_probe_data_processor.py' processes the data produced by the 'four_point_probe_data_collector.py' program. It sorts the data into groups based on user-specified experimental parameters and calculates average values for both current and potential difference.

See 'Instructions for running 4-point probe on Keithley 2400 SourceMeters.pdf' for complete instructions on setting up the SourceMeters and running the two aforementioned programs.
