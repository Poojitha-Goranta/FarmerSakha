function analyzeSoil() {
    fetch("/analyze")
        .then(response => response.json())
        .then(data => {

            let output = `
                <h3>Soil Health Summary</h3>
                <ul>${data.soil_summary.map(s => `<li>${s}</li>`).join("")}</ul>

                <h3>Recommended Crops</h3>
                <ul>${data.crops.map(c => `<li>${c}</li>`).join("")}</ul>

                <h3>Advice for Better Yield</h3>
                <ul>${data.advice.map(a => `<li>${a}</li>`).join("")}</ul>

                <h3>Cost-Effective Remedies</h3>
                <ul>${data.remedies.map(r => `<li>${r}</li>`).join("")}</ul>
            `;

            document.getElementById("output").innerHTML = output;
        });
}
