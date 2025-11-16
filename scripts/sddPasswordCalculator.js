// Handles password generation logic for SDD Key Generator

const JAGUAR_OPTIONS = {
  'CA': 'X150_ODO_APP',
  'CL': 'VIN_BLOCK_EDITOR',
  'CP': 'VIN_BYPASS',
  'CR': 'CCF_EDITOR',
  'AC': 'X351_ODO_APP',
  'LC': 'SOFTWARE_DOWNLOAD',
  'PC': 'X250_ODO_APP',
  'RC': 'X351_RECOVER_KEYS'
};

const LANDROVER_OPTIONS = {
  'CA': 'TAIWAN_VEHICLE_UPDATE',
  'CL': 'L316_ODO_APP',
  'CP': 'CCF_EDITOR',
  'CR': 'SOFTWARE_DOWNLOAD',
  'AC': 'L322_ERASE_KEYS',
  'LC': 'L322_RECOVER_KEYS',
  'PC': 'L322_ODO_APP',
  'RC': 'OPTION_8'
};

function checkSeedFormat(seed, seedCipherMap, vin) {
  // function that checks the seed format is valid
  //
  // How seeds are created:
  //
  // its a fudge using the last 6 digits of the VIN and the time (24hr clock) when SDD opens the session
  // these values are then mapped (substitution cipher style) against key:value pairs to produce the seed
  //
  // seed[0] = vin[0]  - 100 thousand digit of the vin, this is a letter for Jaguar
  // seed[1] = time[0] - the ten digit of the hour
  // seed[2] = vin[2]  - thousand digit of vin
  // seed[3] = time[1] - the unit digit of the hour
  // seed[4] = vin[3]  - hundred digit of the vin
  // seed[5] = time[2] - ten digit of the minutes
  // seed[6] = vin[4]  - ten digit of the vin
  // seed[7] = time[3] - unit digit of the minutes
  // seed[8] = vin[5]  - unit digit of the vin
  // seed[9] = vin[1]  - 10 thousand digit of the vin

  // check the seed and vin length is correct before doing anything else
  if (seed.length !== 10) {
    return { error: 'Seed error: Seed must be 10 characters long.', seedStatus: false };
  }
  if (vin.length !== 6) {
    return { error: 'Seed error: VIN must be 6 characters long.', seedStatus: false };
  }
  
  const SPLIT_SEED = seed.split('');

  let reversed_vin = "000000".split('');
  let reversed_time = "0000".split('');

  // map the seed back to the vin and time using the reversed cipher map
  reversed_vin[0] = seedCipherMap[SPLIT_SEED[0]];
  reversed_time[0] = seedCipherMap[SPLIT_SEED[1]];
  reversed_vin[2] = seedCipherMap[SPLIT_SEED[2]];
  reversed_time[1] = seedCipherMap[SPLIT_SEED[3]];
  reversed_vin[3] = seedCipherMap[SPLIT_SEED[4]];
  reversed_time[2] = seedCipherMap[SPLIT_SEED[5]];
  reversed_vin[4] = seedCipherMap[SPLIT_SEED[6]];
  reversed_time[3] = seedCipherMap[SPLIT_SEED[7]];
  reversed_vin[5] = seedCipherMap[SPLIT_SEED[8]];
  reversed_vin[1] = seedCipherMap[SPLIT_SEED[9]];

  // put it back to a string and check the seed matches the VIN provided
  const REVERSED_VIN = reversed_vin.join('');
  const REVERSED_TIME = reversed_time.join('');
 
  if (REVERSED_VIN !== vin) {
    return { error: `Error: Seed does not match the provided VIN. Seed is for VIN ending in: ${REVERSED_VIN}`, seedStatus: false };
  }
  if (!isValid24HourTime(REVERSED_TIME)) {
    return { error: `Error: Seed contains invalid time value: ${REVERSED_TIME}`, seedStatus: false };
  }
  return { error: false, seedStatus: true, seedTime: REVERSED_TIME , seedVin: REVERSED_VIN  };
}

function checkInput(seed, vin, brand) {
  // check the seed and vin lengths match expected values, returns:
  // false: if there are no errors
  // string: error message if there is an error

  // check the seed and VIN lengths are correct
  if (seed.length == 10 && vin.length == 17) {
    // if a 17 digit VIN is provided, detect the brand from the VIN
    const DETECTED_BRAND = detectBrand(vin);
    // not sure what all possible VIN prefixes are, so if we can't detect just return the selected brand
    if (!DETECTED_BRAND) {
      return { error: false, brand: brand };
    } else {
      return { error: false, brand: DETECTED_BRAND };
    }
  } else if (seed.length == 10 && vin.length == 6) {
    // if a 6 digit VIN is provided, just return no errors if seed length is correct
    return { error: false, brand: brand };
  } else if (!seed || !vin) {
    return { error: 'Error: Please enter both seed and VIN.', brand: false };
  } else if (vin.length !== 17 && vin.length !== 6) {
    return { error: 'Error: VIN must be the full the 17 characters or last 6 characters.', brand: false };
  } else if (seed.length !== 10) {
    return { error: 'Error: Seed must be 10 characters long.', brand: false };
  }
  return { error: 'Error: Unknown error condition occurred and I panicked', brand: false };
}

function createSddEngineerCode(seed, vin, brand, accessOption) {
  // function to generate the engineer code

  seed = seed.toUpperCase().trim();
  vin = vin.toUpperCase().trim();

  // base cipher values needed for the mapping process
  const BASE_CIPHER_KEY         = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
  const SEED_CIPHER_VALUES      = 'G7HM8CPLFAQW2R9Y1DE3SVU4O5KTJB6XNIZ0'
  const PASSWORD_CIPHER_VALUES  = 'CPLFAQW2R9Y1DB3SVU4E5K8JO6XNGZTH7IM0'

  // check the input makes sense, returns false if no errors, otherwise returns error string
  const CHECK_INPUT_VALUES = checkInput(seed, vin, brand);
  // if there are errors, return the error message and stop
  if (CHECK_INPUT_VALUES.error) {
    return { error: CHECK_INPUT_VALUES.error, password: false, brand:brand };
  }
  // set the brand to whatever was detected from the VIN if applicable
  brand = CHECK_INPUT_VALUES.brand;

  // build the cipher maps needed
  const SEED_CIPHER_MAP = mapStringsToKeyValues(SEED_CIPHER_VALUES, BASE_CIPHER_KEY);
  if (SEED_CIPHER_MAP.error) {
    return { error: SEED_CIPHER_MAP.error, password: false, brand:brand };
  }

  const PASSWORD_CIPHER_MAP = mapStringsToKeyValues(SEED_CIPHER_VALUES, PASSWORD_CIPHER_VALUES);
  if (PASSWORD_CIPHER_MAP.error) {
    return { error: PASSWORD_CIPHER_MAP.error, password: false, brand:brand };
  }

  // lets make sure the seed makes sense
  const CHECK_SEED_FORMAT = checkSeedFormat(seed, SEED_CIPHER_MAP.cipherMap, vin.slice(-6));
  if (CHECK_SEED_FORMAT.error) {
    return { error: CHECK_SEED_FORMAT.error, password: false, brand:brand };
  }

  // finally generate the password
  const PASSWORD_RESULT = generatePassword(seed, PASSWORD_CIPHER_MAP.cipherMap, brand, accessOption);
  if (PASSWORD_RESULT.error) {
    return { error: PASSWORD_RESULT.error, password: false, brand:brand };
  } else {  
    return { error: false, password: PASSWORD_RESULT.password, brand:brand, seedTime: CHECK_SEED_FORMAT.seedTime, seedVin: CHECK_SEED_FORMAT.seedVin };
  }
}

function detectBrand(vin) {
  // detects the brand from the VIN if possible, otherwise returns false
  const VIN_PREFIX = vin.slice(0, 3);
  switch (VIN_PREFIX) {
    case 'SAJ':
      return 'JAG';
    case 'SAL':
      return 'LR';
    default:
      return false;
  }
}

function generatePassword(seed, passwordCipherMap, brand, accessOption) {
  // function to generate the password from the seed, for the correct brand

  // How passwords are created
  //
  // These values are mapped (substitution cipher) from the seed against
  // key:value pairs to produce the main part of the password
  //
  // password[0] = seed[5] = time[2] - ten digit of the minutes
  // password[1] = seed[3] = time[1] - the unit digit of the hour
  // password[2] = seed[0] = vin[0]  - 100 thousand digit of the vin, this is a letter for Jaguar
  // password[3] = seed[6] = vin[4]  - ten digit of the vin
  // password[4] = seed[9] = vin[1]  - 10 thousand digit of the vin
  // password[5] = seed[1] = time[0] - the ten digit of the hour
  // password[6] = seed[7] = time[3] - unit digit of the minutes
  // password[7] = seed[8] = vin[5]  - unit digit of the vin
  // password[8] = seed[2] = vin[2]  - thousand digit of vin
  // password[9] = seed[4] = vin[3]  - hundred digit of the vin

  // check access option is valid for the brand
  if (!isValidAccessOption(accessOption, brand)) {
    return { error: `Invalid access option: ${accessOption} for brand: ${brand}`, password: false };
  }

  let password = "0000000000".split('');

  // map the seed to the password, decode using the cipher map
  password[0] = passwordCipherMap[seed[5]];
  password[1] = passwordCipherMap[seed[3]];
  password[2] = passwordCipherMap[seed[0]];
  password[3] = passwordCipherMap[seed[6]];
  password[4] = passwordCipherMap[seed[9]];
  password[5] = passwordCipherMap[seed[1]];
  password[6] = passwordCipherMap[seed[7]];
  password[7] = passwordCipherMap[seed[8]];
  password[8] = passwordCipherMap[seed[2]];
  password[9] = passwordCipherMap[seed[4]];

  let engineeringCode = password.join('');
  let padding='CC';
  let options='';

  if (brand === 'JAG') {
      options = accessOption + padding;
  } else if (brand === 'LR') {
      options = padding +accessOption;
  }
  engineeringCode += options;
  return {error:false, password: engineeringCode} ;
}

function isValid24HourTime(timeValueToCheck) {
  // Checks if a 4-digit string is a valid 24-hour clock time (HHMM)
  if (!/^\d{4}$/.test(timeValueToCheck)) return false;
  const HOURS = parseInt(timeValueToCheck.slice(0, 2), 10);
  const MINUTES = parseInt(timeValueToCheck.slice(2, 4), 10);
  if (HOURS < 0 || HOURS > 23 || MINUTES < 0 || MINUTES > 59) return false;
  return true;
}

function isValidAccessOption(accessOption, brand) {
  // Checks if accessOption is a key in the correct options object
  const OPTIONS = brand === 'JAG' ? JAGUAR_OPTIONS : LANDROVER_OPTIONS;
  return Object.prototype.hasOwnProperty.call(OPTIONS, accessOption);
}

function mapStringsToKeyValues(keys, values) {
  // maps two strings into a key-value object, returns error or the object
  let characterMap = {};
  // check both strings are the same length to avoid mapping issues
  if (keys.length !== values.length) {
    return { error: `Error: Cipher key and value lengths do not match. Keys: ${keys.length}, Values: ${values.length}`, cipherMap: false };
  }
  const CIPHER_LENGTH = keys.length;
  for (let characterPosition = 0; characterPosition < CIPHER_LENGTH; characterPosition++) {
    characterMap[keys[characterPosition]] = values[characterPosition];
  }
  return { error: false, cipherMap: characterMap };
}