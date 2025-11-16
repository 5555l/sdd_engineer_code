document.addEventListener('DOMContentLoaded', function () {
  document.getElementById('keyForm').addEventListener('submit', function (e) {
    e.preventDefault();
    const SEED = document.getElementById('seed').value.toUpperCase().trim();
    const VIN = document.getElementById('vin').value.toUpperCase().trim();
    let brand = document.getElementById('brand').value;
    let accessOption = document.getElementById('optionSelect').value;
    let engineeringCode = createSddEngineerCode(SEED, VIN, brand, accessOption);
    if (engineeringCode.error) {
      document.getElementById('result').innerHTML = `<span class="error-message">${engineeringCode.error}</span>`;
      return;
    } else if (engineeringCode.brand != brand) {
      // selected brand does not match the detected VIN, update the brand selection and recalculate
      updateSelectedOption('brand', engineeringCode.brand);
      brand = engineeringCode.brand;
      updateOptions();
      updateSelectedOption('optionSelect', accessOption);
    }
    document.getElementById('result').innerHTML = `Password for VIN ending in ${engineeringCode.seedVin}: <span class="password-value">${engineeringCode.password}</span>`;
  });
  
  // Erase password on change of options select
  document.getElementById('optionSelect').addEventListener('change', function () {
    document.getElementById('result').innerHTML = '';
  });
  
  // Erase password on change of brand select
  document.getElementById('brand').addEventListener('change', function () {
    document.getElementById('result').innerHTML = '';
    updateOptions();
  });
});

function updateSelectedOption(elementId, newElementValue) {
  document.getElementById(elementId).value = newElementValue;
}

function updateOptions() {
  let brand = document.getElementById('brand').value;
  const OPTIONS_SELECT = document.getElementById('optionSelect');
  OPTIONS_SELECT.innerHTML = '';
  const OPTIONS = brand === 'JAG' ? JAGUAR_OPTIONS : LANDROVER_OPTIONS;
  for (const [KEY, VALUE] of Object.entries(OPTIONS)) {
    const OPTION = document.createElement('option');
    OPTION.value = KEY;
    OPTION.text = `${VALUE} (${KEY})`;
    OPTIONS_SELECT.appendChild(OPTION);
  }
  // always default to CCF_EDITOR option after updating
  if (brand == 'JAG') {
    updateSelectedOption('optionSelect', 'CR');
  } else if (brand == 'LR') {
    updateSelectedOption('optionSelect', 'CP');
  }
}

// Initialize options on page load
updateOptions();