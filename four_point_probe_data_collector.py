# serial commands are the same commands listed under SCPI in the SourceMeter 2400 user manual 
# https://download.tek.com/manual/2400S-900-01_K-Sep2011_User.pdf

print('\nImporting Libraries...')
import serial
import time
import csv
import numpy as np
from decimal import Decimal


print('Libraries Imported')



###FUNCTIONS ZONE 

#a function to keep the terminal open while I read the error message
def holdTerminal():
     while True:
        entry = input("Press x to exit: ")
        if entry == 'x':
            break
        else:
            continue

def isBlank (myString):
    return not (myString and myString.strip())

def genericError(exc):
    print(
            CRED,
            "\nPROCESS FAILED",
            CEND
            )
    print(CRED,
        "\nError Message:",
        exc,
        CEND
        )


#defining some string to use to print coloured text to the terminal
#see link for details (https://stackoverflow.com/questions/287871/how-do-i-print-colored-text-to-the-terminal?page=2&tab=modifieddesc#tab-top)
#to get colours to display on 32-bit versions of windows, you have to edit the registry
#see link for details (https://superuser.com/questions/413073/windows-console-with-ansi-colors-handling/1050078)
CRED = '\033[91m'
CEND = '\033[0m'
CGREEN = '\033[92m'


#connecting to serial devices
print('\nOpening ports...')

try:
    # configure the serial connections with the pump
    SourceMeter24 = serial.Serial(
    port='COM4',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_TWO,
    bytesize=serial.EIGHTBITS
    )
    print("SourceMeter24 connected")

except serial.SerialException as exc:
    print(
        CRED,
        "\nUNABLE TO OPEN PORT COM 4",
        "\nCheck serial connection between PC and SourceMeter",
        CEND
        )
    print(CRED,
        "\nError Message:",
        exc,
        CEND
        )

try:
    # configure the serial connections with the pump
    SourceMeter25 = serial.Serial(
    port='COM5',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
    )
    print("SourceMeter25 connected")

except serial.SerialException as exc:
    print(
        CRED,
        "\nUNABLE TO OPEN PORT COM 5",
        "\nCheck serial connection between PC and SourceMeter",
        CEND
        )
    print(CRED,
        "\nError Message:",
        exc,
        CEND
        )
    


#checking communication to sourcemeters
print("\nPerforming pump communication self-test...")
try:
    SourceMeter24.write(b'*IDN?\n')
    response = SourceMeter24.readline().decode('utf-8').strip()

    print('here1')

    if isBlank(response) == True:
        print("\nSourceMeter 24 response string empty")    
    if response == 'KEITHLEY INSTRUMENTS INC.,MODEL 2400,1260629,C30   Mar 17 2006 09:29:29/A02  /K/J':
        print("SourceMeter 24 coms self test successful")
    else:
        raise Exception(f"\nPump returned unexpected response string: {response}")
except Exception as exc:
    print(
        CRED,
        "\nSOURCEMETER 24 COMS SELF TEST FAILED",
        "\nENSURE THE SOURCEMETER ADDRESS MATCHES THE COM PORT NUMBER",
        CEND
        )
    print(CRED,
        "\nError Message:",
        exc,
        CEND
        )

try:
    SourceMeter25.write(b'*IDN?\n')
    response = SourceMeter25.readline().decode('utf-8').strip()

    if isBlank(response) == True:
        print("\nSourceMeter 25 response string empty")    
    if response == 'KEITHLEY INSTRUMENTS INC.,MODEL 2400,1260619,C30   Mar 17 2006 09:29:29/A02  /K/J':
        print("SourceMeter 25 coms self test successful")
    else:
        raise Exception(f"\nPump returned unexpected response string: {response}")
except Exception as exc:
    print(
        CRED,
        "\nSOURCEMETER 25 COMS SELF TEST FAILED",
        "\nENSURE THE SOURCEMETER ADDRESS MATCHES THE COM PORT NUMBER",
        CEND
        )
    print(CRED,
        "\nError Message:",
        exc,
        CEND
        )
    
#configuring source-measure stati
print("\nConfiguring current source...")

#sourcemeter 24 is the current source

try:
    #SourceMeter24.write(b'\r\n')
    SourceMeter24.write(b'*RST\r\n') #resets default configuration

    SourceMeter24.write(b':SOUR:CLE:AUTO OFF\r\n') # prevents sourcemeter from disabling output after measuring 

    SourceMeter24.write(b':SOUR:FUNC CURR\r\n') # puts sourcemeter in current source mode

    SourceMeter24.write(b':SOUR:CURR:MODE FIXED\r\n') # fixes sourcemeter in current source configuration

    SourceMeter24.write(b':SENS:FUNC "CURR"\r\n') # puts sourcemeter in current measure mode

    SourceMeter24.write(b':SOUR:CURR:RANG MAX\r\n') # setting current source range to max (1A)

    #SourceMeter24.write(b':SOUR:CURR:RANG MIN\r\n') # setting current source range to min (1uA)

    #SourceMeter24.write(b':SOUR:CURR:RANG UP\r\n') # increasing  current source range - eg: (1uA -> 10uA)

    SourceMeter24.write(b':SOUR:CURR:RANG DOWN\r\n') # decreasing  current source range - eg: (100mA -> 10mA)

    SourceMeter24.write(b':SOUR:CURR:LEV 0\r\n')

    SourceMeter24.write(b':SENS:VOLT:PROT 21\r\n') # setting the compliance voltage

    SourceMeter24.write(b':FORM:ELEM CURR\r\n') # setting FORMat for data output (CURRent only)

except Exception as exc:
    genericError(exc)

print("Current source configured")

print("\nConfiguring voltmeter...")

#sourcemeter 25 is the voltmeter

try:
    #SourceMeter25.write(b'\r\n')
    SourceMeter25.write(b'*RST\r\n') #resets default configuration

    SourceMeter25.write(b':SOUR:CLE:AUTO OFF\r\n') # prevents sourcemeter from disabling output after measuring 

    SourceMeter25.write(b':SOUR:FUNC CURR\r\n') # puts sourcemeter in current source mode (will be set to zero)

    SourceMeter25.write(b':SOUR:CURR:MODE FIXED\r\n') # fixes sourcemeter in current source configuration
    
    SourceMeter25.write(b':SOUR:CURR:RANG MIN\r\n') # settting current source range to MIN

    SourceMeter25.write(b':SENS:FUNC "VOLT"\r\n') # puts sourcemeter in voltage measure mode

    SourceMeter25.write(b':SOUR:CURR:LEV 0\r\n')

    SourceMeter25.write(b':FORM:ELEM VOLT\r\n') # setting FORMat for data output (CURRent only)

except Exception as exc:
    genericError(exc)





#enabling outputs
print("\nEnabling outputs...")
try:
    SourceMeter24.write(b':OUTP ON\r\n')

    SourceMeter24.write(b'OUTP?\r\n')
    response = SourceMeter24.readline().decode('utf-8').strip()

    if response == '1':
        print("SourceMeter 24 output enabled")
    elif response == '0':
        print("Failed to enable SourceMeter 24")
    else:
        raise Exception(f"\SourceMeter returned unexpected response string: {response}")

except Exception as exc:
    genericError(exc)

try:
    SourceMeter25.write(b':OUTP ON\r\n')

    SourceMeter25.write(b'OUTP?\r\n')
    response = SourceMeter25.readline().decode('utf-8').strip()

    if response == '1':
        print("SourceMeter 25 output enabled")
    elif response == '0':
        print("Failed to enable SourceMeter 25")
    else:
        raise Exception(f"\SourceMeter returned unexpected response string: {response}")

except Exception as exc:
    genericError(exc)


# disabling output at end of config step

try:
    SourceMeter24.write(b':OUTP OFF\r\n')
    SourceMeter25.write(b':OUTP OFF\r\n')
except Exception as exc:
    print(
        CRED,
        "\nFAILED TO DISABLE OUTPUT",
        "\n*** PLEASE DISABLE OUTPUT LOCALLY ***",
        CEND
        )
    print(CRED,
        "\nError Message:",
        exc,
        CEND
        )

print('Outputs disabled')


### systew initializatin complete
print(
    CGREEN,
    "\n\n*** SYSTEM INITIALIZATION COMPLETE ***\n\n",
    CEND
    )











### measurement zone

# experiment parameters
I_min = 0.0 # A <- lower bound of current
I_max = 1.0E-3 # A <- upper bound of current
I_res = 0.05E-3 # A <- interval between current measurements - i.e., current resolution
dwell_1 = 10.0 #s <- time to hold each current value
dwell_2 = 0.1 #s <- time interval between measurements for a given current



I_list = np.arange(I_min, I_max, I_res) # list of current values to use for measurements

I_list = [1E-7, 2E-7, 3E-7, 4E-7, 5E-7, 6E-7, 7E-7, 8E-7, 9E-7]

I_list_string = ['%.2E' % Decimal(str(I)) for I in I_list] # converts all decimal values in I_list to string in scientific notation - i.e., 0.00E-04

# printing the list of current values to test to the console
I_string = "\nCurrent values to test: | "
for I in I_list_string:
    I_string += I+" A | "
I_string += "\n"
print(I_string)



#opening csv file to write data to 
try:
    
    while True:
        path = input(r"Enter the path (using double \\ and ending in \\) where you want to save the data file"  + "\n" + r"eg: C:\\Users\\my_name\\: ")
        name = current_time = time.strftime(f"four_point_probe_data_%d-%m-%y_%H%M%S", time.localtime())

        # uncomment this section to allow custom file names
        """
        while True:
            entry = input(r"Enter a path (using double \\ and ending in \\) to store experiment results (press 'd' to use the default): ")
            if entry == 'd':
                break
            else:
                path = entry
                break
        
        while True:
            entry = input("\nEnter a file name for experiment results (press 'd' to use the default): ")
            if entry == 'd':
                break
            else:
                name = entry
                break
        

        print("\nResults file will be stored at: " + path+name + ".csv")        

        entry = input("\nAccept this path ('y/n'): ")

        if entry == 'y':
            break
        elif entry == 'n':
            continue
        else:
            print('Invalid input')
        """
        break

    with open(path+name+".csv", 'w', newline='') as results_file:
        writer = csv.writer(results_file, dialect='excel')


except Exception as exc:
    print(
        CRED,
        "\nFAILED TO CREATE FILE",
        CEND
        )
    print(CRED,
        "\nError Message:",
        exc,
        CEND
        )
    holdTerminal()

print('\nFile initialization complete')


"""
# reading from sourcemeters to confirm that they are working + have good connectivity to the samples
for i in range(0, 40):
    SourceMeter24.write(b':READ?\r\n')
    SourceMeter25.write(b':READ?\r\n')
    time.sleep(0.5)
"""


experiment_duration = dwell_1 * len(I_list_string)
print(f"\nEstimated experiment duration: {experiment_duration}s")

entry = input("\nPress enter to begin experiemnt: ")

#enabling outputs
print("\nEnabling outputs...")
try:
    SourceMeter24.write(b':OUTP ON\r\n')

    SourceMeter24.write(b'OUTP?\r\n')
    response = SourceMeter24.readline().decode('utf-8').strip()

    if response == '1':
        print("SourceMeter 24 output enabled")
    elif response == '0':
        print("Failed to enable SourceMeter 24")
    else:
        raise Exception(f"\SourceMeter returned unexpected response string: {response}")

except Exception as exc:
    genericError(exc)

try:
    SourceMeter25.write(b':OUTP ON\r\n')

    SourceMeter25.write(b'OUTP?\r\n')
    response = SourceMeter25.readline().decode('utf-8').strip()

    if response == '1':
        print("SourceMeter 25 output enabled")
    elif response == '0':
        print("Failed to enable SourceMeter 25")
    else:
        raise Exception(f"\SourceMeter returned unexpected response string: {response}")

except Exception as exc:
    genericError(exc)







t_0 = time.time() # starts timer for experiment
print('\nRunning experiment...')


#starting taking measurements
try:
    
    with open(path+name+".csv", 'w', newline='') as results_file:
        writer = csv.writer(results_file, dialect='excel')

        writer.writerow(['current values used / A'])

        writer.writerow(I_list)
        
        writer.writerow(['time / s', 'current / A', 'pot. diff. / V'])

        for I in I_list_string:

            print('I = ' + I)
        
            SourceMeter24.write(bytes(f':SOUR:CURR:LEV {I}\r\n', encoding='utf-8')) # updating current 
            t_i = time.time() # time at which the current value was updated

            while time.time() < t_i + dwell_1: # while loop that ends when dwell_1 has elapsed

                t_start = time.time()
                # read current data
                SourceMeter24.write(b':READ?\r\n')
                I_now = SourceMeter24.readline().decode('utf-8').strip()

                # read voltage data
                SourceMeter25.write(b':READ?\r\n')
                V_now = SourceMeter25.readline().decode('utf-8').strip()

                writer.writerow([time.time()-t_0, I_now, V_now])
                t_end = time.time()

                time.sleep(dwell_2) # sleep for dwell_2 minus time it took to execute read and write functions


except Exception as exc:
    print(
        CRED,
        "\nMEASUREMENT FAILED",
        CEND
        )
    print(CRED,
        "\nError Message:",
        exc,
        CEND
        )
    holdTerminal()


# disabling output at end of measurements

try:
    SourceMeter24.write(b':OUTP OFF\r\n')
    SourceMeter25.write(b':OUTP OFF\r\n')
except Exception as exc:
    print(
        CRED,
        "\nFAILED TO DISABLE OUTPUT",
        "\n*** PLEASE DISABLE OUTPUT LOCALLY ***",
        CEND
        )
    print(CRED,
        "\nError Message:",
        exc,
        CEND
        )


SourceMeter24.close()
SourceMeter25.close()

print('\nExperiment complete')