################################################################
# How seeds are created
#
# its a fudge using the last 6 digits of the VIN and the time (24hr clock) when SDD opens the session
# these values are then mapped (substitution cipher style) against a dictionary to produce the seed
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

################################################################
# How passwords are created
#
# These values are also mapped (substitution cipher) from the seed against
# a dictionary to produce the main part of the password
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

import sys
import getopt
import random
from datetime import datetime

# Generate a seed if needed
def seedgen(vin,dt):
    # create a random time
    time = str(random.randrange(0, 24)).zfill(2) + ':' + str(random.randrange(0, 61)).zfill(2)
    sdc = [0] * 10
    # take the values from the VIN and time and put them in the right places in the seed
    sdc[0] = vin[:1]
    sdc[1] = time[:1]
    sdc[2] = vin[2:3]
    sdc[3] = time[1:2]
    sdc[4] = vin[3:4]
    sdc[5] = time[3:4]
    sdc[6] = vin[4:5]
    sdc[7] = time[4:5]
    sdc[8] = vin[5:6]
    sdc[9] = vin[1:2]

    # Swap the values for the ones in the seed substitution cipher dictionary
    for idx in range(len(sdc)):
        sdc[idx] = str(dt.get(sdc[idx]))

    # Join all the values together to make the seed    
    seed_c = "".join(sdc)
    return (seed_c)

# base substitution cipher used by JLR
cipher_key = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
s_cipher =   'G7HM8CPLFAQW2R9Y1DE3SVU4O5KTJB6XNIZ0'
p_cipher =   'CPLFAQW2R9Y1DB3SVU4E5K8JO6XNGZTH7IM0'
# These two ciphers are *almost* the same. It could be they are the same and
# the mismatched values are VIN's that are never used IRL so it doesn't matter

# Set seed and password cipher dictionaries 
# seed is just the cipher as is
dt = dict(zip(list(cipher_key), list(s_cipher)))
# password cipher uses the seed cipher as the key
pt = dict(zip(list(s_cipher), list(p_cipher)))

# Option codes for Jaguar
jopt = {
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
lopt = {
    'TAIWAN_VEHICLE_UPDATE':'CA',
    'L316_ODO_APP':'CL',
    'CCF_EDITOR':'CP',
    'SOFTWARE_DOWNLOAD':'CR',
    'L322_ERASE_KEYS':'AC',
    'L322_RECOVER_KEYS':'LC',
    'L322_ODO_APP':'PC',
    'OPTION_8':'RC'
}

# Create a reverse lookup for the seed to make it easy to check later
rdt = {}
for v in dt:
    rdt[dt.get(v)]= v

# set some defaults
fvin=seed=vtype=vt=''
gen = False
opt = 'CCF_EDITOR'

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
             "   -t / --type <JAG ¦ LR>......  Manually set vehicle type, by default it will try work it out from the VIN\n"
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
             "A VIN and either a seed (--seed) or --gen must be provided\n")

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
        fvin = current_value.upper()
        vin = fvin[11:17]
    elif current_argument in ("-s", "--seed"):
        seed = current_value.upper()
    elif current_argument in ("-o", "--option"):
        opt = current_value.upper()    
    elif current_argument in ("-g", "--gen"):
        gen = True 
    elif current_argument in ("-t", "--type"):
        vt = current_value.upper() 
    
ext = False

#####################################################################################
# Check if provided arguments make sense

# Check if both a VIN and seed have been provided
if fvin == '' or (seed == '' and gen == False):
    print("Both VIN and seed are needed, use --gen to make a seed if you don't have one")
    ext = True

# Check type is supported vehicle
if vt == 'JAG':
    vtype = 'Jaguar'
    optcodes = jopt
elif vt == 'LR':
    vtype = 'Landrover'
    optcodes = lopt
elif vt != '':
    print('Unsupported vehicle type, ignoring user provided value')

# Check the VIN looks roughly ok
if fvin != '' and (len(fvin) != 17 or dt.get(vin[:1]) == None):
    print('VIN is not valid format, must be 17 chars and of supported type')
    ext = True       
if vtype == '' and fvin != '' and fvin[:3] == 'SAJ':
    vtype = 'Jaguar'
    optcodes = jopt
elif vtype == '' and fvin != '' and fvin[:3] == 'SAL':
    vtype = 'Landrover'
    optcodes = lopt
else:
    if vtype == '' and fvin != '': 
        print('Unsupported VIN, expected VIN beginning with SAL or SAJ but got', fvin[:3])
        ext = True

# Check if a provided seed looks about right
if seed != '' and len(seed) != 10 and gen == False:
    print('Seed is not valid format, must be 10 chars')
    ext = True 

# Check a valid option has been provided
if vtype != '' and optcodes.get(opt) == None:
    print('Invalid option:', opt, ' provided')
    ext = True 

if ext == True: 
    print(help_text)
    sys.exit(2) 

#####################################################################################
# Seems we got sensible things so do stuff with them

# If asked to generate a seed go and do it
if gen == True:
    seed = seedgen(vin,dt)

# Turn the seed into a list
sd=list(seed)

# Reverse engineer the VIN and time from the user provided seed so we can check it makes sense
if gen == False and seed != '':
    time = rvin = ''
    vn = [0]*6
    tm = [0]*4

    vn[0] = sd[0]
    tm[0] = sd[1]
    vn[2] = sd[2]
    tm[1] = sd[3]
    vn[3] = sd[4]
    tm[2] = sd[5]
    vn[4] = sd[6]
    tm[3] = sd[7]
    vn[5] = sd[8]
    vn[1] = sd[9]

    # reverse the encoding by using the seed reverse lookup   
    for ch in vn:
        rvin += str(rdt.get(ch))

    for ch in tm:
        time += str(rdt.get(ch))

    # compare the provided VIN with the reverse engineered VIN
    if vin != rvin:
        print('Seed does not match VIN, expected:', vin,'but seed is for:', rvin)
        sys.exit(2)

    # Check the extracted time makes any sense
    try:
        testtime = datetime.strptime(time, "%H%M")
    except ValueError:
        print('Invalid time in seed, expected a 24h time got:', time)
        sys.exit(2)

#####################################################################################
# If we've got this far then we should be able to create a password for this car
# The core part of the password is a 10 byte string derived from the seed

# Put the values from the seed in the right places in the password
pwd = [0] * 10
pwd[0] = sd[5]
pwd[1] = sd[3]
pwd[2] = sd[0]
pwd[3] = sd[6]
pwd[4] = sd[9]
pwd[5] = sd[1]
pwd[6] = sd[7]
pwd[7] = sd[8]
pwd[8] = sd[2]
pwd[9] = sd[4]

# Swap the values for the ones in the password substitution cipher dictionary
for ix in range(len(pwd)):
    pwd[ix] = str(pt.get(pwd[ix]))

# put the password into a string
password = "".join(pwd)

# to finish off the password we just need to append the engineering option to the end
# first 2 bytes are Jaguar options, last 2 bytes are Landrover options. Pad with "CC" where needed.
if vtype == 'Jaguar':
    ops = optcodes.get(opt) + 'CC'
elif vtype == 'Landrover':
    ops = 'CC' + optcodes.get(opt)
password += ops

# We're all done, print it all out and go home
print('VIN:', fvin, ' Brand:', vtype,' Seed:', seed, ' Password', '('+ opt + '):', password)