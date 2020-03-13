import os

# Get a list of each airline, given a prefix of 'budget' or 'charter'.
def get_airline_list(prefix):
    path = os.environ['DATA_DIR']+'/raw/'+prefix+'airline_list.txt'
    airline_list=[]
    with open(path,'r') as airline_reader:
        for airline in airline_reader:
            airline_list.append(airline.rstrip())
    return airline_list

# This returns a clean version of the spreadsheet row.
def clean_line(line):

    # This truncates the 'month' values from the 'Activity Period' so the entry is simply the year.
    cleaned_line = line[:4]+line[6:]
    year = line[:4]
    # Both 2005 and 2019 are incomplete years in the datasets, so they are left out of the cleaned dataset.

    if '2005' in year or '2019' in year:
        return ''

    return line[:4]+line[6:]

# Filter a specific file for lines with airlines in the airline_list in them.
def clean_file(file_name,airline_list,prefix):

    source_path = os.environ['DATA_DIR']+'/raw/'+file_name
    destination_path = os.environ['DATA_DIR']+'/processed/'+"clean_"+prefix+"_"+file_name

    clean_file=open(destination_path,'w')
    with open(source_path,'r') as reader:
        header = reader.readline()
        clean_file.write(header)
        for line in reader:
            for airline in airline_list:
                if airline in line:
                    clean_file.write(clean_line(line))

    clean_file.close()
    reader.close()

# Get the list of budget and charter airlines.
budget_airline_list=get_airline_list("budget_")
charter_airline_list=get_airline_list("charter_")

# Filter the Landings and Passenger Databases for budget and charter airlines respectively.
clean_file('Air_Traffic_Landings_Statistics.csv',budget_airline_list,"budget")
clean_file("Air_Traffic_Passenger_Statistics.csv",budget_airline_list,"budget")
clean_file("Air_Traffic_Landings_Statistics.csv",charter_airline_list,"charter")
clean_file("Air_Traffic_Passenger_Statistics.csv",charter_airline_list,"charter")
