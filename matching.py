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

#bucket 1
free_residents = list(resident_specs.keys())

#bucket 2
hospital_matches = {}

#loop to look at every hospital name
for hosp_name in hospital_specs.keys():
   
    #save empty list under this hospital's name
    hospital_matches[hosp_name] = []

#same for residents, save empty list under their name to keep track of their matches
resident_proposals_count = {}

for resident in resident_specs.keys():
    resident_proposals_count[resident] = 0

"""
PSEUDO-CODE (Required by Part c):
Initialize all residents to be free.
Initialize all hospital match lists to be empty.
While there are free residents who still have hospitals on their preference list:
    Choose such a resident (r)
    Let h be the highest-ranked hospital on r's list to which r has not yet proposed
    If h has an empty slot (current matches < capacity):
        Assign r to h temporarily
    Else (h is at capacity):
        Find the worst-ranked resident (w) currently assigned to h
        If h prefers r to w:
            Evict w (make w free again)
            Assign r to h temporarily
        Else:
            r remains free (will propose to next choice in future iteration)
"""

while len(free_residents) > 0:

    #grab first resident from the list
    resident = free_residents.pop(0)

    #grab the resident's preferences
    preferences = resident_specs[resident]

    #grab the index of the hospital this resident is proposing to
    proposal_idx = resident_proposals_count[resident]

    #grab the name of the hospital this resident is proposing to
    target_hospital = preferences[proposal_idx]

    #increment the proposal count 
    resident_proposals_count[resident] += 1

    #grab the capacity of the hospital
    capacity = hospital_specs[target_hospital][0]

    #if hospital has room, add resident to the hospital's matches
    if len(hospital_matches[target_hospital]) < capacity:
        hospital_matches[target_hospital].append(resident)

    #if hospital is at capacity, we need to check if the hospital prefers this resident over any of its current matches
    else:

        #assume the worst resident is the first one in the list of matches for this hospital
        worst_resident = hospital_matches[target_hospital][0]
        worst_rank = hospital_ranks[target_hospital][worst_resident]

        #check the rest of currently matched residents
        for current_resident in hospital_matches[target_hospital]:
            current_rank = hospital_ranks[target_hospital][current_resident]

            #if current resident rank is higher (worse) than the worst rank, they are even less preferred
            if current_rank > worst_rank:
                worst_resident = current_resident
                worst_rank = current_rank

        #now we have the worst resident, we need to check if the hospital prefers the new resident over the worst one
        new_resident_rank = hospital_ranks[target_hospital][resident]
        
        if new_resident_rank < worst_rank:
            #hospital prefers the new resident, so we replace the worst resident with the new one
            hospital_matches[target_hospital].remove(worst_resident)
            hospital_matches[target_hospital].append(resident)

            #the worst resident is now free, so we add them back to the list of free residents
            free_residents.append(worst_resident)
        else:
            #hospital prefers the worst resident, so the new resident remains free and will propose to the next hospital on their list in the next iteration of the loop
            free_residents.append(resident)

#print out final matches
print("\n--- Final Matches ---")
for hosp_name, matched_residents in hospital_matches.items():
    # If the hospital matched with students, join them with commas
    if matched_residents:
        residents_str = ", ".join(matched_residents)
        print(f"{hosp_name}, {residents_str}")
    else:
        # If a hospital didn't get any matches, just print its name
        print(f"{hosp_name}")