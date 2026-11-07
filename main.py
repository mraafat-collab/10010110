<!DOCTYPE html>
<html lang="ar" dir="ltr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HR Management System</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Inter', sans-serif; background: #f3f4f6; }
        .primary-bg { background-color: #6B4226; }
        .primary-text { color: #6B4226; }
        .secondary-bg { background-color: #F5EDE0; }
        .card-shadow { box-shadow: 0 2px 8px rgba(0,0,0,0.08); }
        .timeline-line { position: relative; }
        .timeline-line::before {
            content: '';
            position: absolute;
            top: 20px;
            left: 0;
            right: 0;
            height: 2px;
            background: #6B4226;
            z-index: 0;
        }
        .timeline-step { position: relative; z-index: 1; }
        @media print {
            .no-print { display: none !important; }
            body { background: white; }
        }
        .status-pending { background: #fbbf24; color: #78350f; }
        .status-approved { background: #34d399; color: #064e3b; }
        .status-rejected { background: #f87171; color: #7f1d1d; }
    </style>
</head>
<body class="min-h-screen">

    <!-- Navigation -->
    <nav class="primary-bg text-white p-4 no-print">
        <div class="max-w-7xl mx-auto flex justify-between items-center">
            <h1 class="text-xl font-bold">HR Management System</h1>
            <div class="flex gap-4">
                <button onclick="showPage('hire')" class="px-4 py-2 rounded hover:bg-white/20 transition">New Hire Form</button>
                <button onclick="showPage('resignation')" class="px-4 py-2 rounded hover:bg-white/20 transition">Resignation Form</button>
                <button onclick="showPage('records')" class="px-4 py-2 rounded hover:bg-white/20 transition">View Records</button>
            </div>
        </div>
    </nav>

    <div class="max-w-6xl mx-auto p-6">

        <!-- NEW HIRE FORM PAGE -->
        <div id="hire-page" class="page">
            <div id="hire-form-content" class="bg-white rounded-lg card-shadow p-8">
                <!-- Header -->
                <div class="flex justify-between items-start mb-8">
                    <div>
                        <p class="text-xs text-gray-500 uppercase tracking-wider">COMPANY</p>
                        <h2 class="text-3xl font-bold primary-text mt-1">New Hire Approval Form</h2>
                        <div class="mt-3 flex items-center gap-2">
                            <span id="hire-status-badge" class="px-3 py-1 rounded-full text-xs font-semibold status-pending">● PENDING</span>
                        </div>
                        <p class="mt-3 text-gray-600">Dear Mr. <span id="hire-manager-display">Manager</span>, Greetings</p>
                    </div>
                    <div class="secondary-bg rounded-lg p-4 w-64 card-shadow">
                        <div class="w-24 h-24 bg-gray-300 rounded-full mx-auto mb-3 overflow-hidden">
                            <img id="hire-photo-preview" src="" class="w-full h-full object-cover hidden">
                            <div id="hire-photo-placeholder" class="w-full h-full flex items-center justify-center text-gray-500">📷</div>
                        </div>
                        <p class="text-xs text-gray-500 uppercase">CANDIDATE</p>
                        <p id="hire-name-display" class="font-bold text-lg">mohamed</p>
                        <p id="hire-title-display" class="text-sm text-gray-600">Factory</p>
                        <p id="hire-branch-display" class="text-sm text-gray-600">Factory</p>
                    </div>
                </div>

                <!-- Metrics Row -->
                <div class="grid grid-cols-4 gap-4 mb-8">
                    <div class="secondary-bg rounded-lg p-4 card-shadow">
                        <p class="text-xs text-gray-500 uppercase">Total Net (EGP)</p>
                        <p id="hire-total-display" class="text-2xl font-bold primary-text">0</p>
                    </div>
                    <div class="secondary-bg rounded-lg p-4 card-shadow">
                        <p class="text-xs text-gray-500 uppercase">Hiring Date</p>
                        <p id="hire-date-display" class="text-lg font-bold">-</p>
                    </div>
                    <div class="secondary-bg rounded-lg p-4 card-shadow">
                        <p class="text-xs text-gray-500 uppercase">Job Title</p>
                        <p id="hire-job-display" class="text-lg font-bold">-</p>
                    </div>
                    <div class="secondary-bg rounded-lg p-4 card-shadow">
                        <p class="text-xs text-gray-500 uppercase">Manager</p>
                        <p id="hire-mgr-display" class="text-lg font-bold">-</p>
                    </div>
                </div>

                <!-- Data Table -->
                <div class="border rounded-lg overflow-hidden mb-8">
                    <table class="w-full">
                        <thead>
                            <tr class="primary-bg text-white">
                                <th class="p-3 text-left">Field</th>
                                <th class="p-3 text-left">Value</th>
                            </tr>
                        </thead>
                        <tbody id="hire-table-body">
                            <!-- Filled by JS -->
                        </tbody>
                    </table>
                </div>

                <!-- Checklist -->
                <div class="border rounded-lg p-6 mb-8">
                    <h3 class="font-bold text-lg primary-text mb-4">ONBOARDING CHECKLIST • <span id="checklist-count">0</span>/6</h3>
                    <div class="w-full bg-gray-200 rounded-full h-2 mb-4">
                        <div id="checklist-progress" class="primary-bg h-2 rounded-full transition-all" style="width: 0%"></div>
                    </div>
                    <div class="grid grid-cols-2 gap-3" id="checklist-items">
                        <label class="flex items-center gap-2"><input type="checkbox" class="checklist-cb" data-item="Contract signed"> Contract signed</label>
                        <label class="flex items-center gap-2"><input type="checkbox" class="checklist-cb" data-item="ID & documents collected"> ID & documents collected</label>
                        <label class="flex items-center gap-2"><input type="checkbox" class="checklist-cb" data-item="Medical/insurance done"> Medical / insurance done</label>
                        <label class="flex items-center gap-2"><input type="checkbox" class="checklist-cb" data-item="Uniform/equipment issued"> Uniform / equipment issued</label>
                        <label class="flex items-center gap-2"><input type="checkbox" class="checklist-cb" data-item="System access created"> System access created</label>
                        <label class="flex items-center gap-2"><input type="checkbox" class="checklist-cb" data-item="Orientation completed"> Orientation completed</label>
                    </div>
                </div>

                <!-- Footer Signatures -->
                <div class="grid grid-cols-3 gap-8 pt-8 border-t">
                    <div class="text-center">
                        <div class="border-b border-gray-400 h-16 mb-2"></div>
                        <p class="text-sm text-gray-600">Candidate</p>
                    </div>
                    <div class="text-center">
                        <div class="border-b border-gray-400 h-16 mb-2"></div>
                        <p class="text-sm text-gray-600">Direct Manager</p>
                    </div>
                    <div class="text-center">
                        <div class="border-b border-gray-400 h-16 mb-2"></div>
                        <p class="text-sm text-gray-600">HR</p>
                    </div>
                </div>
            </div>

            <!-- Action Buttons -->
            <div class="mt-6 flex gap-4 no-print">
                <button onclick="saveHire()" class="primary-bg text-white px-6 py-3 rounded-lg font-semibold hover:opacity-90">💾 Save Record</button>
                <button onclick="printForm('hire-form-content')" class="bg-gray-700 text-white px-6 py-3 rounded-lg font-semibold hover:opacity-90">🖨️ Print</button>
                <button onclick="downloadPNG('hire-form-content')" class="bg-blue-600 text-white px-6 py-3 rounded-lg font-semibold hover:opacity-90">📥 Save as PNG</button>
            </div>

            <!-- Edit Form (collapsible) -->
            <div class="mt-8 bg-white rounded-lg card-shadow p-6 no-print">
                <h3 class="font-bold text-lg mb-4">📝 Edit Hire Data</h3>
                <div class="grid grid-cols-2 gap-4">
                    <input id="f-name" placeholder="Employee Name" class="border p-2 rounded">
                    <input id="f-branch" placeholder="Branch" class="border p-2 rounded">
                    <input id="f-title" placeholder="Job Title" class="border p-2 rounded">
                    <input id="f-date" type="date" class="border p-2 rounded">
                    <input id="f-grading" placeholder="Grading System" class="border p-2 rounded">
                    <input id="f-basic" type="number" placeholder="Net Basic Salary" class="border p-2 rounded">
                    <input id="f-allowance" type="number" placeholder="Net Allowance" class="border p-2 rounded">
                    <input id="f-kpi" type="number" placeholder="Net KPI Amount" class="border p-2 rounded">
                    <input id="f-total" type="number" placeholder="Total Net" class="border p-2 rounded">
                    <input id="f-education" placeholder="Educational Qualifications" class="border p-2 rounded">
                    <input id="f-age" type="number" placeholder="Age" class="border p-2 rounded">
                    <input id="f-address" placeholder="Address" class="border p-2 rounded">
                    <input id="f-experience" placeholder="Professional Experience" class="border p-2 rounded">
                    <input id="f-manager" placeholder="Direct Manager" class="border p-2 rounded">
                    <select id="f-status" class="border p-2 rounded">
                        <option>Pending</option>
                        <option>Approved</option>
                        <option>Rejected</option>
                    </select>
                    <input id="f-comment" placeholder="Manager Comment" class="border p-2 rounded">
                    <div class="col-span-2">
                        <input type="file" id="f-photo" accept="image/*" class="border p-2 rounded w-full" onchange="previewPhoto(this, 'hire')">
                    </div>
                </div>
                <button onclick="updatePreview()" class="mt-4 primary-bg text-white px-6 py-2 rounded">Update Preview</button>
            </div>
        </div>

        <!-- RESIGNATION FORM PAGE -->
        <div id="resignation-page" class="page hidden">
            <div id="resignation-form-content" class="bg-white rounded-lg card-shadow p-8">
                <!-- Header -->
                <div class="flex justify-between items-start mb-8">
                    <div>
                        <p class="text-gray-600">Dear Mr. <span id="res-manager-display">Mohamed</span>,</p>
                        <h2 class="text-3xl font-bold primary-text mt-2">RESIGNATION APPROVAL REQUEST</h2>
                    </div>
                    <div class="secondary-bg rounded-lg p-4 w-64 card-shadow">
                        <div class="w-24 h-24 bg-gray-300 rounded-full mx-auto mb-3 overflow-hidden">
                            <img id="res-photo-preview" src="" class="w-full h-full object-cover hidden">
                            <div id="res-photo-placeholder" class="w-full h-full flex items-center justify-center text-gray-500">📷</div>
                        </div>
                        <p class="text-xs text-gray-500 uppercase">EMPLOYEE PROFILE</p>
                        <p id="res-name-display" class="font-bold text-lg">Abu Bakr Muhammad Mahmoud</p>
                        <p id="res-title-display" class="text-sm text-gray-600">Sales Casual</p>
                        <p class="text-sm text-gray-600">Resigning <span id="res-date-display">20/10/2026</span></p>
                    </div>
                </div>

                <!-- Timeline -->
                <div class="mb-8">
                    <h3 class="font-bold text-lg mb-6">Resignation Journey</h3>
                    <div class="timeline-line flex justify-between px-8">
                        <div class="timeline-step text-center flex-1">
                            <div class="w-10 h-10 primary-bg rounded-full mx-auto flex items-center justify-center text-white mb-2">👤</div>
                            <p class="text-xs text-gray-500">Joined</p>
                            <p id="res-joined-display" class="font-semibold text-sm">03/10/2026</p>
                        </div>
                        <div class="timeline-step text-center flex-1">
                            <div class="w-10 h-10 primary-bg rounded-full mx-auto flex items-center justify-center text-white mb-2">🏆</div>
                            <p class="text-xs text-gray-500">Total Experience</p>
                            <p id="res-exp-display" class="font-semibold text-sm">17 Days</p>
                        </div>
                        <div class="timeline-step text-center flex-1">
                            <div class="w-10 h-10 primary-bg rounded-full mx-auto flex items-center justify-center text-white mb-2">📄</div>
                            <p class="text-xs text-gray-500">Letter Submitted</p>
                            <p id="res-letter-display" class="font-semibold text-sm">20/10/2026</p>
                        </div>
                        <div class="timeline-step text-center flex-1">
                            <div class="w-10 h-10 primary-bg rounded-full mx-auto flex items-center justify-center text-white mb-2">🕐</div>
                            <p class="text-xs text-gray-500">Notice Period</p>
                            <p id="res-notice-display" class="font-semibold text-sm">One Month</p>
                        </div>
                        <div class="timeline-step text-center flex-1">
                            <div class="w-10 h-10 primary-bg rounded-full mx-auto flex items-center justify-center text-white mb-2">✓</div>
                            <p class="text-xs text-gray-500">Finalized</p>
                            <p id="res-final-display" class="font-semibold text-sm">20/10/2026</p>
                        </div>
                    </div>
                </div>

                <!-- Metrics Row -->
                <div class="grid grid-cols-4 gap-4 mb-8">
                    <div class="secondary-bg rounded-lg p-4 card-shadow">
                        <p class="text-xs text-gray-500 uppercase">Total Net Pay (EGP)</p>
                        <p id="res-total-display" class="text-2xl font-bold primary-text">7000</p>
                    </div>
                    <div class="secondary-bg rounded-lg p-4 card-shadow">
                        <p class="text-xs text-gray-500 uppercase">Last Working Day</p>
                        <p id="res-last-display" class="text-lg font-bold">20/10/2026</p>
                    </div>
                    <div class="secondary-bg rounded-lg p-4 card-shadow">
                        <p class="text-xs text-gray-500 uppercase">Reason for Leaving</p>
                        <p id="res-reason-display" class="text-lg font-bold">Education</p>
                    </div>
                    <div class="secondary-bg rounded-lg p-4 card-shadow">
                        <p class="text-xs text-gray-500 uppercase">Direct Manager</p>
                        <p id="res-mgr-display" class="text-lg font-bold">Sherif S. El-Sayed</p>
                    </div>
                </div>

                <!-- Data Table -->
                <div class="border rounded-lg overflow-hidden mb-8">
                    <table class="w-full">
                        <thead>
                            <tr class="primary-bg text-white">
                                <th class="p-3 text-left">Field</th>
                                <th class="p-3 text-left">Value</th>
                            </tr>
                        </thead>
                        <tbody id="res-table-body"></tbody>
                    </table>
                </div>

                <!-- Action Items -->
                <div class="border rounded-lg p-6">
                    <h3 class="font-bold text-lg primary-text mb-4">MANAGER ACTION ITEMS - Resignation Next Steps</h3>
                    <div class="grid grid-cols-2 gap-4">
                        <div class="flex items-start gap-3">
                            <span class="text-2xl">🧮</span>
                            <p class="text-sm">Calculate final dues and payout. Ensure <strong>'Total Net to pay <span id="ai-total">7000</span> EGP'</strong> is correct.</p>
                        </div>
                        <div class="flex items-start gap-3">
                            <span class="text-2xl">🤝</span>
                            <p class="text-sm">Facilitate handover process with Team Leader and new point of contact.</p>
                        </div>
                        <div class="flex items-start gap-3">
                            <span class="text-2xl">🕐</span>
                            <p class="text-sm">Review notice period waiver request (<strong id="ai-notice">One Month</strong> Status).</p>
                        </div>
                        <div class="flex items-start gap-3">
                            <span class="text-2xl">📦</span>
                            <p class="text-sm">Schedule property return (laptop, badge, keys).</p>
                        </div>
                        <div class="flex items-start gap-3 col-span-2">
                            <span class="text-2xl">✉️</span>
                            <p class="text-sm">Issue final acceptance letter and experience certificate.</p>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Action Buttons -->
            <div class="mt-6 flex gap-4 no-print">
                <button onclick="saveResignation()" class="primary-bg text-white px-6 py-3 rounded-lg font-semibold hover:opacity-90">💾 Save Record</button>
                <button onclick="printForm('resignation-form-content')" class="bg-gray-700 text-white px-6 py-3 rounded-lg font-semibold hover:opacity-90">🖨️ Print</button>
                <button onclick="downloadPNG('resignation-form-content')" class="bg-blue-600 text-white px-6 py-3 rounded-lg font-semibold hover:opacity-90">📥 Save as PNG</button>
            </div>

            <!-- Edit Form -->
            <div class="mt-8 bg-white rounded-lg card-shadow p-6 no-print">
                <h3 class="font-bold text-lg mb-4">📝 Edit Resignation Data</h3>
                <div class="grid grid-cols-2 gap-4">
                    <input id="r-name" placeholder="Employee Name" class="border p-2 rounded">
                    <input id="r-branch" placeholder="Branch" class="border p-2 rounded">
                    <input id="r-title" placeholder="Job Title" class="border p-2 rounded">
                    <input id="r-hire-date" placeholder="Hiring Date (DD/MM/YYYY)" class="border p-2 rounded">
                    <input id="r-res-date" placeholder="Resignation Date" class="border p-2 rounded">
                    <input id="r-last-day" placeholder="Last Working Day" class="border p-2 rounded">
                    <input id="r-grading" placeholder="Grading System" class="border p-2 rounded">
                    <input id="r-total" type="number" placeholder="Total Net" class="border p-2 rounded">
                    <input id="r-reason" placeholder="Reason for Leaving" class="border p-2 rounded">
                    <input id="r-notice" placeholder="Notice Period Status" class="border p-2 rounded">
                    <input id="r-handover" placeholder="Handover Status" class="border p-2 rounded">
                    <input id="r-experience" placeholder="Total Experience" class="border p-2 rounded">
                    <input id="r-manager" placeholder="Direct Manager" class="border p-2 rounded">
                    <input id="r-absence" type="number" placeholder="Absence Days" class="border p-2 rounded">
                    <input id="r-loan" type="number" placeholder="Loan Balance" class="border p-2 rounded">
                    <select id="r-status" class="border p-2 rounded">
                        <option>Pending</option>
                        <option>Approved</option>
                        <option>Rejected</option>
                    </select>
                    <div class="col-span-2">
                        <input type="file" id="r-photo" accept="image/*" class="border p-2 rounded w-full" onchange="previewPhoto(this, 'res')">
                    </div>
                </div>
                <button onclick="updateResignationPreview()" class="mt-4 primary-bg text-white px-6 py-2 rounded">Update Preview</button>
            </div>
        </div>

        <!-- RECORDS PAGE -->
        <div id="records-page" class="page hidden">
            <div class="bg-white rounded-lg card-shadow p-6">
                <h2 class="text-2xl font-bold primary-text mb-6">📁 Saved Records</h2>
                
                <div class="mb-6">
                    <h3 class="font-bold text-lg mb-3">New Hires</h3>
                    <div id="hires-list" class="space-y-2"></div>
                </div>
                
                <div class="border-t pt-6">
                    <h3 class="font-bold text-lg mb-3">Resignations</h3>
                    <div id="resignations-list" class="space-y-2"></div>
                </div>
            </div>
        </div>

    </div>

    <script>
        const API = '';
        let hirePhotoPath = '';
        let resPhotoPath = '';

        // Navigation
        function showPage(page) {
            document.querySelectorAll('.page').forEach(p => p.classList.add('hidden'));
            document.getElementById(page + '-page').classList.remove('hidden');
            if (page === 'records') loadRecords();
        }

        // Photo Preview
        function previewPhoto(input, type) {
            const file = input.files[0];
            if (!file) return;
            const reader = new FileReader();
            reader.onload = (e) => {
                const img = document.getElementById(type + '-photo-preview');
                img.src = e.target.result;
                img.classList.remove('hidden');
                document.getElementById(type + '-photo-placeholder').classList.add('hidden');
            };
            reader.readAsDataURL(file);
            
            // Upload to server
            const formData = new FormData();
            formData.append('file', file);
            fetch(API + '/api/upload-photo', { method: 'POST', body: formData })
                .then(r => r.json())
                .then(data => {
                    if (type === 'hire') hirePhotoPath = data.photo_path;
                    else resPhotoPath = data.photo_path;
                });
        }

        // Update Hire Preview
        function updatePreview() {
            const name = document.getElementById('f-name').value || 'mohamed';
            const branch = document.getElementById('f-branch').value || 'Factory';
            const title = document.getElementById('f-title').value || 'Factory';
            const date = document.getElementById('f-date').value || '-';
            const total = document.getElementById('f-total').value || '0';
            const manager = document.getElementById('f-manager').value || '-';
            const status = document.getElementById('f-status').value;

            document.getElementById('hire-name-display').textContent = name;
            document.getElementById('hire-branch-display').textContent = branch;
            document.getElementById('hire-title-display').textContent = title;
            document.getElementById('hire-date-display').textContent = date;
            document.getElementById('hire-total-display').textContent = total;
            document.getElementById('hire-mgr-display').textContent = manager;
            document.getElementById('hire-manager-display').textContent = manager;
            document.getElementById('hire-job-display').textContent = title;

            const badge = document.getElementById('hire-status-badge');
            badge.textContent = '● ' + status.toUpperCase();
            badge.className = 'px-3 py-1 rounded-full text-xs font-semibold status-' + status.toLowerCase();

            // Table
            const fields = [
                ['Employee Name', name], ['Branch', branch], ['Job Title', title],
                ['Hiring Date', date], ['Grading System', document.getElementById('f-grading').value],
                ['Net Basic Salary EGP', document.getElementById('f-basic').value],
                ['Net Allowance EGP', document.getElementById('f-allowance').value],
                ['Net KPI Amount 100% EGP', document.getElementById('f-kpi').value],
                ['Total Net to pay EGP', total],
                ['Educational Qualifications', document.getElementById('f-education').value],
                ['Age', document.getElementById('f-age').value],
                ['Address', document.getElementById('f-address').value],
                ['Professional Experience', document.getElementById('f-experience').value],
                ['Direct Manager', manager], ['Status', status],
                ['Manager Comment', document.getElementById('f-comment').value]
            ];
            document.getElementById('hire-table-body').innerHTML = fields.map(f => 
                `<tr class="border-b"><td class="p-3 font-medium">${f[0]}</td><td class="p-3">${f[1]}</td></tr>`
            ).join('');
        }

        // Update Resignation Preview
        function updateResignationPreview() {
            const name = document.getElementById('r-name').value || 'Abu Bakr Muhammad Mahmoud';
            const branch = document.getElementById('r-branch').value || 'Park-St Branch';
            const title = document.getElementById('r-title').value || 'Sales Casual';
            const hireDate = document.getElementById('r-hire-date').value || '03/10/2026';
            const resDate = document.getElementById('r-res-date').value || '20/10/2026';
            const lastDay = document.getElementById('r-last-day').value || '20/10/2026';
            const total = document.getElementById('r-total').value || '7000';
            const reason = document.getElementById('r-reason').value || 'Education';
            const notice = document.getElementById('r-notice').value || 'One Month';
            const manager = document.getElementById('r-manager').value || 'Sherif S. El-Sayed';

            document.getElementById('res-name-display').textContent = name;
            document.getElementById('res-title-display').textContent = title;
            document.getElementById('res-date-display').textContent = resDate;
            document.getElementById('res-joined-display').textContent = hireDate;
            document.getElementById('res-letter-display').textContent = resDate;
            document.getElementById('res-final-display').textContent = resDate;
            document.getElementById('res-last-display').textContent = lastDay;
            document.getElementById('res-total-display').textContent = total;
            document.getElementById('res-reason-display').textContent = reason;
            document.getElementById('res-notice-display').textContent = notice;
            document.getElementById('res-mgr-display').textContent = manager;
            document.getElementById('res-manager-display').textContent = manager;
            document.getElementById('ai-total').textContent = total;
            document.getElementById('ai-notice').textContent = notice;

            const fields = [
                ['Employee Name', name], ['Branch', branch], ['Job Title', title],
                ['Hiring Date', hireDate], ['Resignation Date', resDate],
                ['Last Working Day', lastDay], ['Grading System', document.getElementById('r-grading').value],
                ['Total Net to pay EGP', total], ['Reason for Leaving', reason],
                ['Notice Period Status', notice], ['Handover Status', document.getElementById('r-handover').value],
                ['Total Experience', document.getElementById('r-experience').value],
                ['Direct Manager', manager], ['Absence during the year', document.getElementById('r-absence').value + ' Day'],
                ['Loan balance', document.getElementById('r-loan').value + ' EGP']
            ];
            document.getElementById('res-table-body').innerHTML = fields.map(f => 
                `<tr class="border-b"><td class="p-3 font-medium">${f[0]}</td><td class="p-3">${f[1]}</td></tr>`
            ).join('');
        }

        // Checklist
        document.querySelectorAll('.checklist-cb').forEach(cb => {
            cb.addEventListener('change', () => {
                const count = document.querySelectorAll('.checklist-cb:checked').length;
                document.getElementById('checklist-count').textContent = count;
                document.getElementById('checklist-progress').style.width = (count/6*100) + '%';
            });
        });

        // Save Hire
        async function saveHire() {
            const checklist = Array.from(document.querySelectorAll('.checklist-cb:checked')).map(cb => cb.dataset.item);
            const data = {
                employee_name: document.getElementById('f-name').value,
                branch: document.getElementById('f-branch').value,
                job_title: document.getElementById('f-title').value,
                hiring_date: document.getElementById('f-date').value,
                grading_system: document.getElementById('f-grading').value,
                net_basic_salary: parseFloat(document.getElementById('f-basic').value) || 0,
                net_allowance: parseFloat(document.getElementById('f-allowance').value) || 0,
                net_kpi: parseFloat(document.getElementById('f-kpi').value) || 0,
                total_net: parseFloat(document.getElementById('f-total').value) || 0,
                educational_qualifications: document.getElementById('f-education').value,
                age: parseInt(document.getElementById('f-age').value) || 0,
                address: document.getElementById('f-address').value,
                professional_experience: document.getElementById('f-experience').value,
                direct_manager: document.getElementById('f-manager').value,
                status: document.getElementById('f-status').value,
                manager_comment: document.getElementById('f-comment').value,
                photo_path: hirePhotoPath,
                checklist: checklist
            };
            await fetch(API + '/api/hires', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(data)
            });
            alert('✅ Hire record saved!');
        }

        // Save Resignation
        async function saveResignation() {
            const data = {
                employee_name: document.getElementById('r-name').value,
                branch: document.getElementById('r-branch').value,
                job_title: document.getElementById('r-title').value,
                hiring_date: document.getElementById('r-hire-date').value,
                resignation_date: document.getElementById('r-res-date').value,
                last_working_day: document.getElementById('r-last-day').value,
                grading_system: document.getElementById('r-grading').value,
                total_net: parseFloat(document.getElementById('r-total').value) || 0,
                reason_for_leaving: document.getElementById('r-reason').value,
                notice_period_status: document.getElementById('r-notice').value,
                handover_status: document.getElementById('r-handover').value,
                total_experience: document.getElementById('r-experience').value,
                direct_manager: document.getElementById('r-manager').value,
                absence_days: parseInt(document.getElementById('r-absence').value) || 0,
                loan_balance: parseFloat(document.getElementById('r-loan').value) || 0,
                status: document.getElementById('r-status').value,
                photo_path: resPhotoPath
            };
            await fetch(API + '/api/resignations', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(data)
            });
            alert('✅ Resignation record saved!');
        }

        // Load Records
        async function loadRecords() {
            const hires = await fetch(API + '/api/hires').then(r => r.json());
            const resignations = await fetch(API + '/api/resignations').then(r => r.json());
            
            document.getElementById('hires-list').innerHTML = hires.length ? hires.map(h => `
                <div class="flex justify-between items-center p-3 border rounded">
                    <div><strong>${h.employee_name}</strong> - ${h.job_title} <span class="text-sm text-gray-500">(${h.status})</span></div>
                    <button onclick="deleteRecord('hires', '${h.id}')" class="text-red-600 text-sm">🗑️ Delete</button>
                </div>
            `).join('') : '<p class="text-gray-500">No records</p>';
            
            document.getElementById('resignations-list').innerHTML = resignations.length ? resignations.map(r => `
                <div class="flex justify-between items-center p-3 border rounded">
                    <div><strong>${r.employee_name}</strong> - ${r.job_title} <span class="text-sm text-gray-500">(${r.status})</span></div>
                    <button onclick="deleteRecord('resignations', '${r.id}')" class="text-red-600 text-sm">🗑️ Delete</button>
                </div>
            `).join('') : '<p class="text-gray-500">No records</p>';
        }

        async function deleteRecord(type, id) {
            if (!confirm('Delete this record?')) return;
            await fetch(API + '/api/' + type + '/' + id, { method: 'DELETE' });
            loadRecords();
        }

        // Print
        function printForm(elementId) {
            window.print();
        }

        // Download PNG
        async function downloadPNG(elementId) {
            const element = document.getElementById(elementId);
            const canvas = await html2canvas(element, { scale: 2, backgroundColor: '#ffffff' });
            const link = document.createElement('a');
            link.download = elementId + '.png';
            link.href = canvas.toDataURL();
            link.click();
        }

        // Initialize
        updatePreview();
        updateResignationPreview();
    </script>
</body>
</html>
