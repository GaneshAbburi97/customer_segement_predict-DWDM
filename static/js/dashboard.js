/**
 * Library Data Warehouse & Data Mining System
 * Interactive Client Scripts & Chart.js Controllers
 */

document.addEventListener('DOMContentLoaded', function () {
    // -------------------------------------------------------------
    // 1. ETL Runner Trigger
    // -------------------------------------------------------------
    const btnRunETL = document.getElementById('btn-run-etl');
    if (btnRunETL) {
        btnRunETL.addEventListener('click', function () {
            const statusBox = document.getElementById('etl-status-box');
            const btnOriginal = btnRunETL.innerHTML;
            btnRunETL.disabled = true;
            btnRunETL.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Executing ETL Pipeline...';

            fetch('/etl/run', {
                method: 'POST',
                headers: { 'X-Requested-With': 'XMLHttpRequest' }
            })
            .then(res => res.json())
            .then(data => {
                btnRunETL.disabled = false;
                btnRunETL.innerHTML = btnOriginal;
                if (data.status === 'SUCCESS') {
                    alert(`ETL Process Completed Successfully!\n\nSource Records: ${data.source_count}\nCleaned Records: ${data.cleaned_count}\nWarehouse Fact Records: ${data.fact_count}\nDuration: ${data.duration_sec}s`);
                    window.location.reload();
                } else {
                    alert(`ETL Status: ${data.status}\nMessage: ${data.message}`);
                }
            })
            .catch(err => {
                btnRunETL.disabled = false;
                btnRunETL.innerHTML = btnOriginal;
                alert('Error running ETL pipeline: ' + err);
            });
        });
    }

    // -------------------------------------------------------------
    // 2. Classification Live Predictor Form
    // -------------------------------------------------------------
    const formPredict = document.getElementById('form-predict-reader');
    if (formPredict) {
        formPredict.addEventListener('submit', function (e) {
            e.preventDefault();
            const formData = new FormData(formPredict);
            const resultBox = document.getElementById('prediction-result-box');

            fetch('/classification/predict', {
                method: 'POST',
                body: formData
            })
            .then(res => res.json())
            .then(data => {
                if (data.status === 'SUCCESS') {
                    const res = data.result;
                    let badgeClass = 'bg-primary';
                    if (res.predicted_category === 'High Borrower') badgeClass = 'bg-success';
                    else if (res.predicted_category === 'Low Borrower') badgeClass = 'bg-secondary';

                    let probHtml = '';
                    if (res.probabilities) {
                        probHtml = Object.entries(res.probabilities).map(([cls, p]) => 
                            `<span class="badge bg-light text-dark border me-1">${cls}: ${p}%</span>`
                        ).join('');
                    }

                    resultBox.innerHTML = `
                        <div class="alert alert-info d-flex align-items-center justify-content-between p-3">
                            <div>
                                <h6 class="mb-1">Predicted Reader Category:</h6>
                                <span class="badge ${badgeClass} fs-6">${res.predicted_category}</span>
                            </div>
                            <div>${probHtml}</div>
                        </div>
                    `;
                } else {
                    resultBox.innerHTML = `<div class="alert alert-danger">${data.message}</div>`;
                }
            })
            .catch(err => {
                resultBox.innerHTML = `<div class="alert alert-danger">Error: ${err}</div>`;
            });
        });
    }
});
