/*!
    * Start Bootstrap - SB Admin v7.0.5 (https://startbootstrap.com/template/sb-admin)
    * Copyright 2013-2022 Start Bootstrap
    * Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-sb-admin/blob/master/LICENSE)
    */
    // 
// Scripts
// 

var fullCheckAction = window.document.getElementById("fullCheckAction");
var selectList = window.document.querySelectorAll(".form-check-input.item");
var selectCount = 0;
var id;

function fullCheck() {
    for(let i in selectList) 
        selectList[i].checked = fullCheckAction.checked ? true : false;

    if (fullCheckAction.checked === true) {
        selectCount = selectList.length;
    } else {
        selectCount = 0;
    }
}

window.addEventListener('DOMContentLoaded', event => {

    // Toggle the side navigation
    const sidebarToggle = document.body.querySelector('#sidebarToggle');
    if (sidebarToggle) {
        sidebarToggle.addEventListener('click', event => {
            event.preventDefault();
            document.body.classList.toggle('sb-sidenav-toggled');
            localStorage.setItem('sb|sidebar-toggle', document.body.classList.contains('sb-sidenav-toggled'));
        });
    }

});

window.document.getElementById("selectDownloadButton")?.addEventListener("click", () => {
    const selectIds = []
    for(var i in selectList) {
        if(selectList[i].checked && selectList[i].id) {
            if(selectList[i].id.includes("select_")) {
                selectIds.push(selectList[i].id.replace("select_", ""))
            }
        }
    }

    document.getElementById("selectDownloadButton").href = `${window.location.origin}/export-csv/?pk=${selectIds}`

    for(let i in selectList) 
        selectList[i].checked = false;
    selectCount = 0;
    fullCheckAction.checked = false
});

window.document.getElementById("errorReportButton")?.addEventListener("click", () => {
    document.getElementById("errorReportButton").href = `${window.location.origin}/export-error-report-csv`;
    setTimeout(() => {
        location.reload();
    }, 150);
});

window.document.getElementById("selectCustomerDownloadButton")?.addEventListener("click", () => {
    const selectIds = []
    for(var i in selectList) {
        if(selectList[i].checked && selectList[i].id) {
            if(selectList[i].id.includes("select_")) {
                selectIds.push(selectList[i].id.replace("select_", ""))
            }
        }
    }

    document.getElementById("selectCustomerDownloadButton").href = `${window.location.origin}/customer/export-csv/?pk=${selectIds}`

    for(let i in selectList) 
        selectList[i].checked = false;
    selectCount = 0;
    fullCheckAction.checked = false
});

var tableElements = document.getElementsByClassName('table-row');

for (let i = 0; i < tableElements.length; i++) {
  const element = tableElements[i];
  element?.addEventListener('click', (event) => {
    var checkElemet = window.document.getElementById(element.id.replace('tr_', 'select_'));
    checkElemet.checked = !checkElemet.checked;
    checkElemet.checked === true ? selectCount++ : selectCount--;
    if (selectCount === selectList.length) {
        fullCheckAction.checked = true;
    } else {
        fullCheckAction.checked = false;
    }
  });
}

var itemsElements = document.getElementsByClassName('item');

for (let i = 0; i < itemsElements.length; i++) {
  const element = itemsElements[i];
  element.addEventListener('click', (event) => {
    var checkElemet = window.document.getElementById(element.id);
    checkElemet.checked === true ? selectCount++ : selectCount--;
    if (selectCount === selectList.length) {
        fullCheckAction.checked = true;
    } else {
        fullCheckAction.checked = false;
    }
    event.stopPropagation();
})
}

function editStatus(id) {
    $.ajax({
        url: `${window.location.origin}/assist_did/service_status_read/${id}`,
        method: 'GET',
        success: function(response) {
            document.getElementById("edit_status_name").value = response.name
            document.getElementById("edit_status_button").name = response.id
        }
    });
}

document.getElementById("edit_status_form")?.addEventListener('submit', ()=>[
    document.getElementById("edit_status_form").action = `${window.location.origin}/assist_did/service_status_update/${document.getElementById("edit_status_button").name}`
])

function editService(id) {
    $.ajax({
        url: `${window.location.origin}/assist_did/service_item_read/${id}`,
        method: 'GET',
        success: function(response) {
            document.getElementById("edit_service_item_name").value = response.name
            document.getElementById("edit_service_item_description").value = response.description
            document.getElementById("edit_service_item_button").name = response.id
        }
    });
}

document.getElementById("edit_service_item_form")?.addEventListener('submit', ()=>[
    document.getElementById("edit_service_item_form").action = `${window.location.origin}/assist_did/service_item_update/${document.getElementById("edit_service_item_button").name}`
])

function editVoiceCarrier(id) {
    $.ajax({
        url: `${window.location.origin}/assist_did/voice_carrier_read/${id}`,
        method: 'GET',
        success: function(response) {
            document.getElementById("edit_voice_carrier_name").value = response.name
            document.getElementById("edit_voice_carrier_button").name = response.id
        }
    });
}

document.getElementById("edit_voice_carrier_form")?.addEventListener('submit', ()=>[
    document.getElementById("edit_voice_carrier_form").action = `${window.location.origin}/assist_did/voice_carrier_update/${document.getElementById("edit_voice_carrier_button").name}`
])

function editSMSCarrier(id) {
    $.ajax({
        url: `${window.location.origin}/assist_did/sms_carrier_read/${id}`,
        method: 'GET',
        success: function(response) {
            document.getElementById("edit_sms_carrier_name").value = response.name
            document.getElementById("edit_sms_carrier_button").name = response.id
        }
    });
}

document.getElementById("edit_sms_carrier_form")?.addEventListener('submit', ()=>[
    document.getElementById("edit_sms_carrier_form").action = `${window.location.origin}/assist_did/sms_carrier_update/${document.getElementById("edit_sms_carrier_button").name}`
])

function editCustomerType(id) {
    $.ajax({
        url: `${window.location.origin}/assist_did/customer_type_read/${id}`,
        method: 'GET',
        success: function(response) {
            document.getElementById("edit_customer_type_name").value = response.name
            document.getElementById("edit_customer_type_button").name = response.id
        }
    });
}

document.getElementById("edit_customer_type_form")?.addEventListener('submit', ()=>[
    document.getElementById("edit_customer_type_form").action = `${window.location.origin}/assist_did/customer_type_update/${document.getElementById("edit_customer_type_button").name}`
])

function editSMSType(id) {
    $.ajax({
        url: `${window.location.origin}/assist_did/sms_type_read/${id}`,
        method: 'GET',
        success: function(response) {
            document.getElementById("edit_sms_type_name").value = response.name
            document.getElementById("edit_sms_type_button").name = response.id
        }
    });
}

document.getElementById("edit_sms_type_form")?.addEventListener('submit', ()=>[
    document.getElementById("edit_sms_type_form").action = `${window.location.origin}/assist_did/sms_type_update/${document.getElementById("edit_sms_type_button").name}`
])

function editTermLocation(id) {
    $.ajax({
        url: `${window.location.origin}/assist_did/term_location_read/${id}`,
        method: 'GET',
        success: function(response) {
            document.getElementById("edit_term_location_name").value = response.name
            document.getElementById("edit_term_location_button").name = response.id
        }
    });
}

document.getElementById("edit_term_location_form")?.addEventListener('submit', ()=>[
    document.getElementById("edit_term_location_form").action = `${window.location.origin}/assist_did/term_location_update/${document.getElementById("edit_term_location_button").name}`
])