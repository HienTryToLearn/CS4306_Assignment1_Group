#main purpose : clean and store data from input file into dictionaries for easy access later on in the algorithm
#creating empty storage to hold hospital and resident data
hospital_specs = {}
resident_specs = {}

#open file
with open('input.txt', 'r') as file:

    #reading hospital first, so set flag to true
    am_i_reading_hospitals = True
    
    #read file line by line
    for line in file:           

        #check if line is blank, if so, switch to reading patients
        if line.strip() == "":
            am_i_reading_hospitals = False
            print("Done reading hospitals, now reading patients...")
            continue #skip loop move to next line

        #clean invisible spaces and split by comma
        raw_parts = line.strip().split(',')

        #empty list to hold clean parts 
        clean_parts = []

        #loop through raw parts and clean them
        for item in raw_parts:
            clean_parts.append(item.strip())

        #Save the data into the appropriate storage based on whether we are reading hospitals or residents
        if am_i_reading_hospitals:
            name = clean_parts[0]
            slots = int(clean_parts[1])
            preferences = clean_parts[2:]

            #put into hospital storage
            hospital_specs[name] = [slots, preferences]
        else:
            name = clean_parts[0]
            preferences = clean_parts[1:]

            #put into resident storage
            resident_specs[name] = preferences

#print out stored data to verify they were read correctly
print("\n--- Saved Dictionaries ---")
print("Hospital Specs:", hospital_specs)
print("Resident Specs:", resident_specs)

#main purpose : create a cheat sheet for the algorithm to quickly access the rank of a student for a hospital without having to loop through the preference list each time
#create a new dictionary to hold the ranks of each student for each hospital
hospital_ranks = {}

# Create a ranking for each hospital based on the preferences they have for the students
for hosp_name, info in hospital_specs.items():
        
    #create mini-dictionary to hold the rank of each student for this specific hospital
    current_hosp_dict = {}  

    #loop through the student list and grab the index and the student name
    for index, student_name in enumerate(info[1]):
            
            #save to mini-dictionary
            current_hosp_dict[student_name] = index

    #store data before loop moves to next hospital           
    hospital_ranks[hosp_name] = current_hosp_dict

#print out ranks
print("\n--- Hospital Ranks ---")
print(hospital_ranks)

