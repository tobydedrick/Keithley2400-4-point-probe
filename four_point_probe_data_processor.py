# when the program is looking at the current data in I_data and assessing which values correspond to those in I_list, I_thresh is the amount of current above or below an I_data value that the program can accept
# eg:   consider a case where I_list is [0.0 A, 0.50E-4 A, 1.00E-4 A, ... ]. 
#       Any current data in I_data with values between -1E-5 A and +1E-5 A will be assigned to the 0.0 A series
#       Any current data in I_data with values between +0.4E-4 A and +0.6E-4 A will be assigned to the 0.50E-4 A series
I_thresh = 1E-5 #A 


# this script processes the data produced by the sourcemeter_four_point_probe_sheet_resistance_measurement script

print('\nImporting Libraries...')
import csv
import numpy as np

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

# requesting the location and name of the data file from the user
try:
    while True:
            loc = input(r"Enter the path (using double \\ and ending in \\) where the data file is stored and the file's name (excluding the extension" + "\n" + r"eg: C:\\Users\\my_name\\example_file: ")
            
            # checking that the file exists by opening it with csv
            try:
                with open(loc+".csv", 'r', newline='') as results_file:
                    reader = csv.reader(results_file, dialect='excel')
                
                print(
                    CGREEN,
                    "\nFile Located",
                    CEND
                    )
                
                break
                
            except Exception as exc:
                print(
                    CRED,
                    "\nFAILED TO LOCATE FILE",
                    "\nCHECK THAT THE FILE'S PATH AND NAME ARE SPELLED CORRECTLY, AND THAT THE FILE EXTENSION HAS BEEN INCLUDED",
                    CEND
                    )
                print(CRED,
                    "\nError Message:",
                    exc,
                    CEND
                    )
                
                continue
            
except Exception as exc:
    genericError(exc)

# reading from the csv file
print("\nReading data for the CSV file...")
try:
    with open(loc+".csv", 'r', newline='') as results_file:
        reader = csv.reader(results_file, dialect='excel')

        # I_list will store the current values sourced from the power supply during the test
        I_list = []

        # I_data will store the current values actually supplied by the power supply - i.e., the current through the outer probes
        I_data = []

        # V_data will store the potential difference measured by the second sourcemeter - i.e., the potnetial difference between the inner probes
        V_data = []


        row_counter = 1
        for row in reader:
            if row_counter == 2:
                for cell in row:
                    I_list.append(float(cell))
                
            if row_counter > 3:
                I_data.append(float(row[1]))
                V_data.append(float(row[2]))
            
            row_counter+=1
        
        # rows stores the number of rows that contain measured data (there are 3 rows that contain headings and other information)
        rows = (row_counter-3) - 1

        if len(I_data) == len(V_data) == rows:
            print(CGREEN + "Data read from file" + CEND)

        elif len(I_data) != len(V_data):

            print(
                    CRED,
                    "\nWARNING",
                    "\nUnequal number of data in current and potential difference lists. Check your csv for potential issues.",
                    CEND
                    )

        elif len(I_data) != rows:
            print(
                    CRED,
                    "\nWARNING",
                    "\nNumber of data in current list doesn't match the internal counter. Check your csv for potential issues.",
                    CEND
                    )
        
        elif len(V_data) != rows:
            print(
                    CRED,
                    "\nWARNING",
                    "\nNumber of data in potential difference list doesn't match the internal counter. Check your csv for potential issues.",
                    CEND
                    )
            

except Exception as exc:
    genericError(exc)


print("\nProcessing Data...")
# assigning data in I_data into different series according to which current in I_list they correspond to 
try:
    # sorted_data will store the current and potential difference values under different keys depending on which current value in I_list they correspond to 
    sorted_data = dict()

    for current_value in I_list:
        sorted_data[current_value] = {
            'I' : [],
            'V' : []
        }

    keys_index = 0 # used to iterate over all the keys in sorted_data - i.e., the current values in I_list
    I_data_index = 0

    for I in I_data:

        if list(sorted_data.keys())[keys_index] - I_thresh <= I <= list(sorted_data.keys())[keys_index] + I_thresh: # the values in I_list (i.e., the keys of sorted_data) and I_thresh are used to define a window into which values in I_data can fall
            sorted_data[list(sorted_data.keys())[keys_index]]['I'].append(I)
            sorted_data[list(sorted_data.keys())[keys_index]]['V'].append(V_data[I_data_index])
            I_data_index+=1

        else: # the else part of the if statement runs when all values within the window (defined by I_thresh and the values in I_list) have been exhausted; keys_index+=1 means that the next highest value in I_list is used to define the window
            keys_index+=1
            I_data_index+=1

            if list(sorted_data.keys())[keys_index] - I_thresh <= I <= list(sorted_data.keys())[keys_index] + I_thresh: # this if statement checks whether the present value of I falls within the window defined by the next highest value in I_list
                sorted_data[list(sorted_data.keys())[keys_index]]['I'].append(I)
                sorted_data[list(sorted_data.keys())[keys_index]]['V'].append(V_data[I_data_index])

            continue
    
    # n will be used to count the number of current values from I_data that were able to be sorted into series according to the current values in I_list
    n = 0
    for key in sorted_data:
        print(key)
        n = n + len(sorted_data[key]['I'])
        print(n)
    
    outliers = rows - n    

    # processed_data will store the averages of the I and V data from sorted_data
    processed_data = {
        'I' : [],
        'V' : []
        }

    for key in sorted_data:
        processed_data['I'].append(np.mean(sorted_data[key]['I']))
        processed_data['V'].append(np.mean(sorted_data[key]['V']))
    
    
    print(CGREEN + "Data has been processed." + "\n" + str(outliers) + " outlier(s) found." + CEND)

except Exception as exc:
    genericError(exc)

print("\nWriting data to CSV...")
try:
    new_file = loc+'_processed.csv'

    with open(new_file, 'w', newline='') as processed_results_file:
        writer = csv.writer(processed_results_file, dialect='excel')
    
        writer.writerow(['current / A', 'pot. diff. / V'])

        for i in range(0, len(processed_data['I'])):
            writer.writerow([processed_data['I'][i], processed_data['V'][i]])
    
    print(CGREEN + "Data written to CSV file at: " + new_file + CEND)

except Exception as exc:
    genericError(exc)