################################################################
# How seeds are created
#
# its a fudge using the last 6 digits of the VIN and the time (24hr clock) when SDD opens the session
# these values are then mapped (substitution cipher style) against a dictionary to produce the seed
#
# seed[0] = vin[0]  - 100 thousand digit of the vin, this is a letter for Jaguar
# seed[1] = time[1] - the ten digit of the hour
# seed[2] = vin[2]  - thousand digit of vin
# seed[3] = time[2] - the unit digit of the hour
# seed[4] = vin[3]  - hundred digit of the vin
# seed[5] = time[3] - ten digit of the minutes
# seed[6] = vin[4]  - ten digit of the vin
# seed[7] = time[4] - unit digit of the minutes
# seed[8] = vin[5]  - unit digit of the vin
# seed[9] = vin[1]  - 10 thousand digit of the vin
#
################################################################
# How passwords are created
#
# These values are also mapped (substitution cipher) from the seed against
# a dictionary to produce the main part of the password
#
# password[0] = seed[5] = time[3] - ten digit of the minutes
# password[1] = seed[3] = time[2] - the unit digit of the hour
# password[2] = seed[0] = vin[0]  - 100 thousand digit of the vin, this is a letter for Jaguar
# password[3] = seed[6] = vin[4]  - ten digit of the vin
# password[4] = seed[9] = vin[1]  - 10 thousand digit of the vin
# password[5] = seed[1] = time[1] - the ten digit of the hour
# password[6] = seed[7] = time[4] - unit digit of the minutes
# password[7] = seed[8] = vin[5]  - unit digit of the vin
# password[8] = seed[2] = vin[2]  - thousand digit of vin
# password[9] = seed[4] = vin[3]  - hundred digit of the vin
#

import sys
import getopt
import random
from datetime import datetime

# Generate a seed if needed - not really useful in practice, mostly used to test this code
def generate_random_seed(short_vin,seed_dictionary):
    # create a random time, with python random.range(x,y) means equal or greater than x, to less than y
    random_time = str(random.randrange(0, 24)).zfill(2) + ':' + str(random.randrange(0, 61)).zfill(2)
    random_seed_list = [0] * 10
    # take the values from the VIN and time and put them in the right places in the seed
    random_seed_list[0] = short_vin[:1]
    random_seed_list[1] = random_time[:1]
    random_seed_list[2] = short_vin[2:3]
    random_seed_list[3] = random_time[1:2]
    random_seed_list[4] = short_vin[3:4]
    random_seed_list[5] = random_time[3:4]
    random_seed_list[6] = short_vin[4:5]
    random_seed_list[7] = random_time[4:5]
    random_seed_list[8] = short_vin[5:6]
    random_seed_list[9] = short_vin[1:2]

    # Swap the values for the ones in the seed substitution cipher dictionary
    for seed_list_value in range(len(random_seed_list)):
        random_seed_list[seed_list_value] = str(seed_dictionary.get(random_seed_list[seed_list_value]))

    # Join all the values together to make the seed    
    random_seed = "".join(random_seed_list)
    return random_seed

# base substitution cipher used by JLR
cipher_key =        '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
seed_cipher =       'G7HM8CPLFAQW2R9Y1DE3SVU4O5KTJB6XNIZ0'
password_cipher =   'CPLFAQW2R9Y1DB3SVU4E5K8JO6XNGZTH7IM0'

# Set seed and password cipher dictionaries 
# seed is just the cipher as is
seed_dictionary = dict(zip(list(cipher_key), list(seed_cipher)))
# password cipher uses the seed cipher as the key
password_dictionary = dict(zip(list(seed_cipher), list(password_cipher)))

# Option codes for Jaguar
jaguar_options = {
    'X150_ODO_APP':'CA',
    'VIN_BLOCK_EDITOR':'CL',
    'VIN_BYPASS':'CP',
    'CCF_EDITOR':'CR',
    'X351_ODO_APP':'AC',
    'SOFTWARE_DOWNLOAD':'LC',
    'X250_ODO_APP':'PC',
    'X351_RECOVER_KEYS':'RC'
    }

# Option codes for Landrover
landrover_options = {
    'TAIWAN_VEHICLE_UPDATE':'CA',
    'L316_ODO_APP':'CL',
    'CCF_EDITOR':'CP',
    'SOFTWARE_DOWNLOAD':'CR',
    'L322_ERASE_KEYS':'AC',
    'L322_RECOVER_KEYS':'LC',
    'L322_ODO_APP':'PC',
    'OPTION_8':'RC'
}

# set some defaults
full_vin=seed=vehicle_type=brand_type=''
generate_seed = False
access_option = 'CCF_EDITOR'

# Get full command-line arguments
full_cmd_arguments = sys.argv

# Keep all but the first
argument_list = full_cmd_arguments[1:]

# set the command line options
short_options = "hno:v:s:t:o:gno"
long_options = ["help", "vin=", "seed=","option=","gen","type="]

help_text = ("\noptions:\n"
             "   -v / --vin <VIN>............  VIN of the target vehicle\n"
             "   -s / --seed <seed>..........  SDD seed of the target vehicle\n"
             "   -g / --gen .................  Generate a seed for the provided VIN - will override --seed\n"
             "                                 This option probably isn't very useful in real life, it's mostly used for testing this code\n"
             "   -t / --type <JAG ¦ LR>......  Manually set vehicle type instead of trying work it out from the VIN (overrides VIN if VIN is provided)\n"
             "   -o / --option <option>......  SDD access option.\n"
             "                                 Valid Jaguar options are:\n"
             "                                      X351_ODO_APP\n"
             "                                      SOFTWARE_DOWNLOAD\n"
             "                                      X250_ODO_APP\n"
             "                                      CCF_EDITOR\n"
             "                                      X150_ODO_APP\n"
             "                                      VIN_BLOCK_EDITOR\n"
             "                                      VIN_BYPASS\n"
             "                                      X351_RECOVER_KEYS\n\n"
             "                                 Valid Landrover options are:\n"
             "                                      TAIWAN_VEHICLE_UPDATE\n"
             "                                      L316_ODO_APP\n"
             "                                      SOFTWARE_DOWNLOAD\n"
             "                                      CCF_EDITOR\n"
             "                                      L322_ERASE_KEYS\n"
             "                                      L322_RECOVER_KEYS\n"
             "                                      L322_ODO_APP\n"
             "                                      OPTION_8\n\n"             
             "                                 Defaults to CCF_EDITOR if none provided\n\n"
             "Mandatory to provide at least one of these combinations:\n"
             "   --seed and --vin\n"
             "   --seed and --type\n"
             "   --vin and --gen\n"
             "\nIt's advised to always provide --vin with --seed to ensure the seed matches the target vehicle to prevent incorrect passwords being generated\n")

#####################################################################################
# Test for command line options
try:
    arguments, values = getopt.getopt(argument_list, short_options, long_options)
except getopt.error as err:
    # Output error, and return with an error code
    print(str(err))
    sys.exit(2)

# Evaluate given arguments
for current_argument, current_value in arguments:
    if current_argument in ("-h", "--help"):
        print(help_text)
        sys.exit(2)
    elif current_argument in ("-v", "--vin"):
        full_vin = current_value.upper()
        # You don't actually need the full VIN in order to create or check the seed, it just uses the last 6 digits,
        # so shove them into a handy variable. 
        short_vin = full_vin[11:17]
    elif current_argument in ("-s", "--seed"):
        seed = current_value.upper()
    elif current_argument in ("-o", "--option"):
        access_option = current_value.upper()    
    elif current_argument in ("-g", "--gen"):
        generate_seed = True 
    elif current_argument in ("-t", "--type"):
        brand_type = current_value.upper() 
    
#####################################################################################
# Check if provided arguments make sense

# Check if minimum options have been provided
if (full_vin != '' and seed != '') or (full_vin != '' and generate_seed == True) or (seed != '' and brand_type != ''):
    exit_status = False
else:
    print("Incorrect combination of options provided")
    exit_status = True

# Check type is supported vehicle
if brand_type == 'JAG':
    vehicle_type = 'Jaguar'
    option_codes = jaguar_options
elif brand_type == 'LR':
    vehicle_type = 'Landrover'
    option_codes = landrover_options
elif brand_type != '' and full_vin != '':
        print('Unsupported vehicle type, ignoring user provided value and using VIN')
elif brand_type != '' and full_vin == '':
        print('Unsupported vehicle type and no VIN provided. Expected JAG or LR, got',brand_type)
        exit_status = True

# Check the VIN looks roughly ok
if full_vin != '' and (len(full_vin) != 17 or seed_dictionary.get(short_vin[:1]) == None):
    print('VIN is not valid format, must be 17 chars and of supported type')
    exit_status = True
# Use the first 3 characters of the VIN to guess the brand (i.e. its a Jag or Landy)           
if vehicle_type == '' and full_vin != '' and full_vin[:3] == 'SAJ':
    vehicle_type = 'Jaguar'
    option_codes = jaguar_options
elif vehicle_type == '' and full_vin != '' and full_vin[:3] == 'SAL':
    vehicle_type = 'Landrover'
    option_codes = landrover_options
else:
    if vehicle_type == '' and full_vin != '': 
        print('Unsupported VIN, expected VIN beginning with SAL or SAJ but got', full_vin[:3])
        exit_status = True

# Check if a provided seed looks about right
if seed != '' and len(seed) != 10 and generate_seed == False:
    print('Seed is not valid format, must be 10 chars')
    exit_status = True 

# Check a valid option has been provided
if vehicle_type != '' and option_codes.get(access_option) == None:
    print('Invalid option:', access_option, ' provided')
    exit_status = True 

if exit_status == True: 
    print(help_text)
    sys.exit(2) 

#####################################################################################
# Seems we got sensible things, lets do stuff with them

# If asked to generate a seed go and do it
if generate_seed == True:
    seed = generate_random_seed(short_vin,seed_dictionary)

# Turn the seed into a list
seed_list=list(seed)

# Reverse engineer the VIN and time from the user provided seed so we can check it makes sense
if generate_seed == False and seed != '':
    
    # Create a reverse lookup for the seed cipher to make it easy to check
    seed_reverse_lookup = {}
    for seed_key in seed_dictionary:
        seed_reverse_lookup[seed_dictionary.get(seed_key)]= seed_key

    reversed_time = reversed_vin = ''
    reversed_vin_list  = [0]*6
    reversed_time_list = [0]*4

    reversed_vin_list[0]  = seed_list[0]
    reversed_time_list[0] = seed_list[1]
    reversed_vin_list[2]  = seed_list[2]
    reversed_time_list[1] = seed_list[3]
    reversed_vin_list[3]  = seed_list[4]
    reversed_time_list[2] = seed_list[5]
    reversed_vin_list[4]  = seed_list[6]
    reversed_time_list[3] = seed_list[7]
    reversed_vin_list[5]  = seed_list[8]
    reversed_vin_list[1]  = seed_list[9]

    # reverse the encoding by using the seed reverse lookup   
    for reversed_vin_value in reversed_vin_list:
        reversed_vin += str(seed_reverse_lookup.get(reversed_vin_value))

    for reversed_time_value in reversed_time_list:
        reversed_time += str(seed_reverse_lookup.get(reversed_time_value))

    # compare the provided VIN with the reverse engineered VIN
    if full_vin != '' and short_vin != reversed_vin:
        print('Seed does not match VIN, VIN ends in:', short_vin,'but seed is for VIN ending:', reversed_vin)
        sys.exit(2)

    # Check the extracted time makes any sense
    try:
        test_time_format = datetime.strptime(reversed_time, "%H%M")
    except ValueError:
        print('Invalid time in seed, expected a 24h time got:', reversed_time)
        sys.exit(2)

#####################################################################################
# If we've got this far then we should be able to create a password for this car
# The core part of the password is a 10 byte string derived from the seed

# Put the values from the seed in the right places in the password using a list
password_list = [0] * 10
password_list[0] = seed_list[5]
password_list[1] = seed_list[3]
password_list[2] = seed_list[0]
password_list[3] = seed_list[6]
password_list[4] = seed_list[9]
password_list[5] = seed_list[1]
password_list[6] = seed_list[7]
password_list[7] = seed_list[8]
password_list[8] = seed_list[2]
password_list[9] = seed_list[4]

# Swap the values for the ones in the password substitution cipher dictionary
for password_key in range(len(password_list)):
    password_list[password_key] = str(password_dictionary.get(password_list[password_key]))

# put the password into a string
password = "".join(password_list)

# to finish off the password we just need to append the engineering option to the end
# first 2 bytes are Jaguar options, last 2 bytes are Landrover options. Pad with "CC" where needed.
if vehicle_type == 'Jaguar':
    options = option_codes.get(access_option) + 'CC'
elif vehicle_type == 'Landrover':
    options = 'CC' + option_codes.get(access_option)
password += options

# how we display the VIN output depends on what input we got, so decide that here
if full_vin != '':
    vin_output_text = full_vin
    vin_output_label = "VIN:"
else:
    vin_output_text = reversed_vin
    vin_output_label = "VIN ending in:"

# We're all done, print it all out and go home
print(vin_output_label, vin_output_text, ' Brand:', vehicle_type,' Seed:', seed, ' Password', '('+ access_option + '):', password)