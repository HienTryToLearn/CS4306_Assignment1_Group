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

#main purpose : implement the Gale-Shapley algorithm to find a stable matching between hospitals and residents based on their preferences
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
PSEUDO-CODE :
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

#gale-shapley algorithm implementation
while len(free_residents) > 0:

    #grab first resident from the list
    resident = free_residents.pop(0)

    #grab the resident's preferences
    preferences = resident_specs[resident]

    #grab the index of the hospital this resident is proposing to
    proposal_idx = resident_proposals_count[resident]

    #If the resident run ouit of options on their prefererence list, skip the loop, remain unassigned. (prevent while loop from crashing)
    if proposal_idx >= len(preferences):
        continue

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

#main purpose : stability checker to verify that the matching we found is stable, meaning there are no resident-hospital pairs that would prefer each other over their current matches
#empty bucket to hold residents that are completely unassigned
fully_unassigned_residents = [] 

#pre filter for type 1 instability
#loop through every resident
for resident, preferences in resident_specs.items():

    #check if the resident is matched to any hospital
    is_matched = False

    #scan through the hospital's list of accepted residents
    for matched_list in hospital_matches.values():
        if resident in matched_list:
            is_matched = True
            break   # break when found 

    #if scan finished and found absolutely no record
    if not is_matched:
        fully_unassigned_residents.append(resident)

#create tracking
is_stable = True

#Type 1 : an unmatched resident gets skipped over by a hospital
# Walk into every hospital one by one
for hosp_name, matched_residents in hospital_matches.items():
    
    # Look at your clipboard of completely unemployed residents
    for unassigned_res in fully_unassigned_residents:
        
        # Check if this unassigned resident even applied to this hospital
        if unassigned_res in hospital_ranks[hosp_name]:
            
            # Look up how much the hospital liked this unemployed resident
            unassigned_rank = hospital_ranks[hosp_name][unassigned_res]
            
            # Look at the residents this hospital hired
            for hired_res in matched_residents:
                hired_rank = hospital_ranks[hosp_name][hired_res]
                
                # Did the hospital hire someone they liked LESS 
                #    than the unemployed resident? (Smaller index = better rank)
                if unassigned_rank < hired_rank:
                    print(f"🚨 Instability Type 1 Found: {hosp_name} prefers unassigned resident {unassigned_res} over {hired_res}!")
                    is_stable = False

#Type 2 : a resident and hospital prefer each other over their current matches
# Test every possible hospital and resident combination
for hosp_name in hospital_specs.keys():
    for resident in resident_specs.keys():
        
        # Skip if this resident is already matched to this hospital
        if resident in hospital_matches[hosp_name]:
            continue
            
        # Check if they both ranked each other
        if resident in hospital_ranks[hosp_name] and hosp_name in resident_ranks[resident]:
            
            # Find where this resident is currently matched
            current_hosp = None
            for h_name, matches in hospital_matches.items():
                if resident in matches:
                    current_hosp = h_name
                    break
            
            # Check the Resident's Preference: Do they prefer this target hospital
            #   over their current match? (Or are they completely unmatched?)
            res_prefers_target = False
            if current_hosp is None:
                # An unmatched resident always prefers being employed
                res_prefers_target = True
            else:
                res_rank_of_target_hosp = resident_specs[resident].index(hosp_name)
                res_rank_of_current_hosp = resident_specs[resident].index(current_hosp)
                if res_rank_of_target_hosp < res_rank_of_current_hosp:
                    res_prefers_target = True
            
            # Check the Hospital's preference
            if res_prefers_target:
                for hired_res in hospital_matches[hosp_name]:
                    hired_res_rank = hospital_ranks[hosp_name][hired_res]
                    target_res_rank = hospital_ranks[hosp_name][resident]
                    
                    # Both parties want to ditch their matches!
                    if target_res_rank < hired_res_rank:
                        print(f"🚨 Instability Type 2 Found: {hosp_name} and {resident} prefer each other!")
                        print(f"   -> {hosp_name} prefers {resident} over current hire {hired_res}")
                        if current_hosp:
                            print(f"   -> {resident} prefers {hosp_name} over current match {current_hosp}")
                        is_stable = False
            
# Final stability printout
if is_stable:
    print("SUCCESS: The matching is stable. No instabilities found!")
else:
    print("FAILURE: Instabilities were detected in the final matching.")