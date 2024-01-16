import math,os,json
from argparse import ArgumentParser
from datetime import datetime,timedelta

def main(input_file, window_size):
    valid_parms(window_size,input_file)
    #get_data
    data = get_data(input_file)
    #calculate_avarage
    print(calculate_avarage(data,window_size))
    
def calculate_avarage(data,window_size):
    # Get time of first action
    start_time = data[0]['start']
    # Get time of last action
    end_time = data[-1]['start']
    # Translate windows_size to minutes
    time_window = timedelta(minutes = window_size) 
    # Determine the number of lines to print
    delta = math.ceil((end_time - start_time).total_seconds() /60 ) + 1

    output = [] 
    
    # Iterating over each minute that needs to be analyzed.
    for minute in range(delta):

        # Assigning the value of the minute to be analyzed.
        current_time = start_time.replace(second=0, microsecond=0) + timedelta(minutes=minute)
        
        # How many translation occurred
        counter = 0
        
        # Will be used to save the sum of durations
        duration = 0

        for action in data:
            # If the action occurred before the current time, ignore everything that comes after.
            if (current_time >= action['start']):
                # Validate if the action is within the time window.
                if (current_time - time_window )< action['start']:
                    counter += 1
                    duration +=action['duration']
            else:
                break
        
        output.append({"date": str(current_time),"average_delivery_time": duration / counter if counter > 0 else 0})
        
    return output

def valid_parms(window_size, input_file):

    if int(window_size) <= 0:
        raise Exception("Sorry, no numbers below zero")

    if not os.path.exists(input_file):
        raise Exception ("File does not exist")


def get_data(input_file):

    data = [] 
    with open(input_file) as f:
        raw_data = json.load(f)
    for action in raw_data:
        data.append({'start':datetime.strptime(action['timestamp'], '%Y-%m-%d %H:%M:%S.%f'),'duration':action['duration']})
    return data

def parse_args():
    # Create an ArgumentParser object
    parser = ArgumentParser()
    
    # add arguments
    parser.add_argument("-i", "--input_file", dest="input_file",type=str,default=10,help="The input file to change the separator in || default = in.txt") # The input file argument
    parser.add_argument("-w", "--window_size", dest="window_size", type=int, default=10, help="Window time || Default = 10") # window time
    
    return parser.parse_args()

if __name__ == "__main__":
   
    args = parse_args()
    main(**vars(args))