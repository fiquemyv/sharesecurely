document.addEventListener('DOMContentLoaded', function () {
    const countryInput = document.getElementById('country');
    const countryCodeInput = document.getElementById('country-code');
    const countryList = document.getElementById('country-list');

    if (!countryInput || !countryCodeInput || !countryList) return;

    countryInput.addEventListener('input', function () {
        const value = this.value.trim();
        const options = countryList.options;
        for (let i = 0; i < options.length; i++) {
            if (options[i].value === value) {
                countryCodeInput.value = options[i].getAttribute('data-code');
                return;
            }
        }
    });
});
