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
        selectList[i].checked = fullCheckAction.checked;

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

    if (document.getElementById('multi_standard')) {
        document.getElementById('multi_standard').disabled = document.querySelectorAll('.error').length > 0;
    }

    document.getElementById('input_multi_number')?.addEventListener('input', () => {
        inputMultiNumber = document.getElementById('input_multi_number');
        inputMultiNumber.value.split('\n').forEach(item => {
            if (isNaN(item)) {
                inputMultiNumber.classList.add('error');
                document.getElementById('service_order_step_2').disabled = true;
            } else {
                inputMultiNumber.classList.remove('error');
                document.getElementById('service_order_step_2').disabled = false;
            }
        })
    })

});

window.document.getElementById("selectDownloadButton")?.addEventListener("click", () => {
    const selectIds = [];
    for(var i in selectList) {
        if(selectList[i].checked && selectList[i].id) {
            if(selectList[i].id.includes("select_")) {
                selectIds.push(selectList[i].id.replace("select_", ""));
            }
        }
    }

    document.getElementById("selectDownloadButton").href = `${window.location.origin}/export-csv/?pk=${selectIds}`;

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
                selectIds.push(selectList[i].id.replace("select_", ""));
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
            document.getElementById("edit_status_name").value = response.name;
            document.getElementById("edit_status_button").name = response.id;
        }
    });
}

document.getElementById("edit_status_form")?.addEventListener('submit', ()=>{
    document.getElementById("edit_status_form").action = `${window.location.origin}/assist_did/service_status_update/${document.getElementById("edit_status_button").name}`;
})

function editService(id) {
    $.ajax({
        url: `${window.location.origin}/assist_did/service_item_read/${id}`,
        method: 'GET',
        success: function(response) {
            document.getElementById("edit_service_item_name").value = response.name;
            document.getElementById("edit_service_item_description").value = response.description;
            document.getElementById("edit_service_item_button").name = response.id;
        }
    });
}

document.getElementById("edit_service_item_form")?.addEventListener('submit', ()=>{
    document.getElementById("edit_service_item_form").action = `${window.location.origin}/assist_did/service_item_update/${document.getElementById("edit_service_item_button").name}`;
})

function editVoiceCarrier(id) {
    $.ajax({
        url: `${window.location.origin}/assist_did/voice_carrier_read/${id}`,
        method: 'GET',
        success: function(response) {
            document.getElementById("edit_voice_carrier_name").value = response.name;
            document.getElementById("edit_voice_carrier_button").name = response.id;
        }
    });
}

document.getElementById("edit_voice_carrier_form")?.addEventListener('submit', ()=>{
    document.getElementById("edit_voice_carrier_form").action = `${window.location.origin}/assist_did/voice_carrier_update/${document.getElementById("edit_voice_carrier_button").name}`;
})

function editSMSCarrier(id) {
    $.ajax({
        url: `${window.location.origin}/assist_did/sms_carrier_read/${id}`,
        method: 'GET',
        success: function(response) {
            document.getElementById("edit_sms_carrier_name").value = response.name;
            document.getElementById("edit_sms_carrier_button").name = response.id;
        }
    });
}

document.getElementById("edit_sms_carrier_form")?.addEventListener('submit', ()=>{
    document.getElementById("edit_sms_carrier_form").action = `${window.location.origin}/assist_did/sms_carrier_update/${document.getElementById("edit_sms_carrier_button").name}`;
})

function editCustomerType(id) {
    $.ajax({
        url: `${window.location.origin}/assist_did/customer_type_read/${id}`,
        method: 'GET',
        success: function(response) {
            document.getElementById("edit_customer_type_name").value = response.name;
            document.getElementById("edit_customer_type_button").name = response.id;
        }
    });
}

document.getElementById("edit_customer_type_form")?.addEventListener('submit', ()=>{
    document.getElementById("edit_customer_type_form").action = `${window.location.origin}/assist_did/customer_type_update/${document.getElementById("edit_customer_type_button").name}`;
})

function editSMSType(id) {
    $.ajax({
        url: `${window.location.origin}/assist_did/sms_type_read/${id}`,
        method: 'GET',
        success: function(response) {
            document.getElementById("edit_sms_type_name").value = response.name;
            document.getElementById("edit_sms_type_button").name = response.id;
        }
    });
}

document.getElementById("edit_sms_type_form")?.addEventListener('submit', ()=>{
    document.getElementById("edit_sms_type_form").action = `${window.location.origin}/assist_did/sms_type_update/${document.getElementById("edit_sms_type_button").name}`;
})

function editTermLocation(id) {
    $.ajax({
        url: `${window.location.origin}/assist_did/term_location_read/${id}`,
        method: 'GET',
        success: function(response) {
            document.getElementById("edit_term_location_name").value = response.name;
            document.getElementById("edit_term_location_button").name = response.id;
        }
    });
}

document.getElementById("edit_term_location_form")?.addEventListener('submit', ()=>{
    document.getElementById("edit_term_location_form").action = `${window.location.origin}/assist_did/term_location_update/${document.getElementById("edit_term_location_button").name}`;
})

function multi_did_add_check() {
    if (document.getElementById('multi_add')) {
        var currentStatus = true;
        const didElements = document.querySelectorAll('[name="did"]');
        const customerElements = document.querySelectorAll('[name="customer"]');

        didElements.forEach(item => {
            if (!item.value) {
                currentStatus = false;
            }
        })

        customerElements.forEach(item => {
            if (!item.value) {
                currentStatus = false;
            }
        })

        document.getElementById('multi_add').disabled = !(document.querySelectorAll('.error').length == 0 && currentStatus);
    }
}

function service_order_value_check() {
    if (document.getElementById('service_order_create_2')) {
        var currentStatus = true;
        const numberElements = document.querySelectorAll('[name="number"]');
        currentStatus = !!document.getElementById('customer').value && !!document.getElementById('term_location').value && currentStatus;

        numberElements.forEach((item, i)=> {
            if (!item.value && i != 0) {
                currentStatus = false;
            }
        })

        document.getElementById('service_order_create_2').disabled = !(document.querySelectorAll('.error').length == 0 && currentStatus);
        console.log(document.getElementById('service_order_create_2').disabled)
    }
}

function change_num(input_type ,id) {
    select_input = document.getElementById(input_type + id)
    if (!select_input.value) {
        select_input.classList.remove('error');
    } else if (/^\d+$/.test(select_input.value)) {
        select_input.classList.remove('error');
    } else {
        select_input.classList.add('error');
    }

    if (document.getElementById('multi_standard')) {
        document.getElementById('multi_standard').disabled = document.querySelectorAll('.error').length > 0;
    }

    multi_did_add_check();
    service_order_value_check();
}

function change_select(select_type, id) {
    select_inbox = document.getElementById(select_type + id)
    if (select_inbox.value === '') {
        select_inbox.classList.add('error');
    } else {
        select_inbox.classList.remove('error');
    }

    if (document.getElementById('multi_standard')) {
        document.getElementById('multi_standard').disabled = document.querySelectorAll('.error').length > 0;
    }

    multi_did_add_check();
    service_order_value_check();
}

function change_email(id) {
    email_input = document.getElementById('email_' + id);
    var regex = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    email_input.value.split(',').map(item => {
        if (regex.test(String(item.trim()).toLowerCase()) || email_input.value === '') {
            email_input.classList.remove('error');
        } else {
            email_input.classList.add('error');
        }
    })

    if (document.getElementById('multi_standard')) {
        document.getElementById('multi_standard').disabled = document.querySelectorAll('.error').length > 0
    }

    multi_did_add_check();
    service_order_value_check();
}

$(function () {
    $('[data-toggle="tooltip"]').tooltip()
})

function change_date(date_input_type, id) {
    date_input = document.getElementById(date_input_type + id)
    const regex = /^(0[1-9]|1[0-2])\/(0[1-9]|[12][0-9]|3[01])\/(\d{4})$/;
    const match = date_input.value.match(regex);

    if (match) {
        const year = parseInt(match[3], 10);
        const month = parseInt(match[1], 10) - 1;
        const day = parseInt(match[2], 10);

        const date = new Date(year, month, day);
        if (date.getFullYear() === parseInt(year, 10) && date.getMonth() === month && date.getDate() === day) {
            date_input.classList.remove('error');
        }
    } else if (date_input.value === '') {
        date_input.classList.remove('error');
    } else {
        date_input.classList.add('error');
    }

    if (document.getElementById('multi_standard')) {
        document.getElementById('multi_standard').disabled = document.querySelectorAll('.error').length > 0
    }
}

function multi_submit() {
    standardData = document.querySelectorAll('tr')
    var data = []
    for (let i = 1; i < standardData.length; i++) {
        id = standardData[i].id;
        data.push({
            id: id,
            did: document.getElementById('did_' + id).value,
            customer: document.getElementById('customer_' + id).value,
            reseller: document.getElementById('reseller_' + id).value,
            in_method: document.getElementById('in_method_' + id).value,
            voice_carrier: document.getElementById('voice_carrier_' + id).value,
            status: document.getElementById('status_' + id).value,
            sms_enabled: document.getElementById('sms_enabled_' + id).value,
            sms_carrier: document.getElementById('sms_carrier_' + id).value,
            sms_type: document.getElementById('sms_type_' + id).value,
            sms_campaign: document.getElementById('sms_campaign_' + id).value,
            term_location: document.getElementById('term_location_' + id).value,
            user_first_name: document.getElementById('user_first_name_' + id).value,
            user_last_name: document.getElementById('user_last_name_' + id).value,
            extension: document.getElementById('extension_' + id).value,
            email: document.getElementById('email_' + id).value,
            onboard_date: document.getElementById('onboard_date_' + id).value,
            note: document.getElementById('note_' + id).value,
            e911_enabled_billed: document.getElementById('e911_enabled_billed_' + id).value,
            e911_cid: document.getElementById('e911_cid_' + id).value,
            e911_address: document.getElementById('e911_address_' + id).value,
            service_1: document.getElementById('service_1_' + id).value,
            service_2: document.getElementById('service_2_' + id).value,
            service_3: document.getElementById('service_3_' + id).value,
            service_4: document.getElementById('service_4_' + id).value,
        })
    }

    let searchQuery = window.location.href.split('?')[1];

    $.ajax({
        url: `${window.location.origin}/did_standardization/multi_standardization`,
        method: 'POST',
        contentType: 'application/json', 
        headers: {
            'X-CSRFToken': document.cookie.split('=')[1],
        },
        data: JSON.stringify({data: data, searchQuery: searchQuery}),
        success: function (response) {
            document.open();
            document.write(response);
            document.close();
        },
        error: function(xhr, status, error) {
            location.reload();
        }
    });
}

function check_add_item() {
    let tbody = document.getElementById("multi_did_item"); // Reference to the tbody
    let rowCount = tbody.querySelectorAll('tr').length; // Current number of rows
    let newRowIndex = rowCount + 1; // Index for the new row

    let trElement = document.getElementById("multi_did_create_1");
    let trElementClone = trElement.cloneNode(true); // Deep clone the row
    trElementClone.id = "multi_did_create_" + newRowIndex; // Update the id of the cloned tr element

    // Get all first child elements of td tags within the cloned tr and update their IDs
    let firstChildElements = trElementClone.querySelectorAll("td > :first-child");
    firstChildElements.forEach((element) => {
        let baseId = element.id.substring(0, element.id.lastIndexOf("_") + 1); // Extract base ID without the numeric part
        element.id = baseId + newRowIndex; // Update ID with new index
        if (element.tagName === "INPUT") {
            element.value = ""; // Reset text input value
        } else if (element.tagName === "SELECT") {
            element.selectedIndex = 0; // Reset select to the first option
        }
    });

    tbody.appendChild(trElementClone);
    
    document.getElementById('did_'+newRowIndex).oninput = () => change_num('did_', newRowIndex)
    document.getElementById('customer_'+newRowIndex).oninput = () => change_select('customer_', newRowIndex)
    document.getElementById('extension_'+newRowIndex).oninput = () => change_num('extension_', newRowIndex)
    document.getElementById('email_'+newRowIndex).oninput = () => change_email(newRowIndex)
    document.getElementById('onboard_date_'+newRowIndex).oninput = () => change_date('onboard_date_', newRowIndex)
    document.getElementById('multi_add').disabled = true
}

function multi_add_submit() {
    data = document.querySelectorAll('tr')
    var request_data = []
    for (let i = 1; i < data.length; i++) {
        console.log(data[i].id.split('_')[3]);
        id = data[i].id.split('_')[3];
        request_data.push({
            did: document.getElementById('did_' + id).value,
            customer: document.getElementById('customer_' + id).value,
            reseller: document.getElementById('reseller_' + id).value,
            in_method: document.getElementById('in_method_' + id).value,
            voice_carrier: document.getElementById('voice_carrier_' + id).value,
            status: document.getElementById('status_' + id).value,
            sms_enabled: document.getElementById('sms_enabled_' + id).value,
            sms_carrier: document.getElementById('sms_carrier_' + id).value,
            sms_type: document.getElementById('sms_type_' + id).value,
            sms_campaign: document.getElementById('sms_campaign_' + id).value,
            term_location: document.getElementById('term_location_' + id).value,
            user_first_name: document.getElementById('user_first_name_' + id).value,
            user_last_name: document.getElementById('user_last_name_' + id).value,
            extension: document.getElementById('extension_' + id).value,
            email: document.getElementById('email_' + id).value,
            onboard_date: document.getElementById('onboard_date_' + id).value,
            note: document.getElementById('note_' + id).value,
            e911_enabled_billed: document.getElementById('e911_enabled_billed_' + id).value,
            e911_cid: document.getElementById('e911_cid_' + id).value,
            e911_address: document.getElementById('e911_address_' + id).value,
            service_1: document.getElementById('service_1_' + id).value,
            service_2: document.getElementById('service_2_' + id).value,
            service_3: document.getElementById('service_3_' + id).value,
            service_4: document.getElementById('service_4_' + id).value,
        })
    }

    $.ajax({
        url: `${window.location.origin}/did/multi_add/`,
        method: 'POST',
        contentType: 'application/json', 
        headers: {
            'X-CSRFToken': document.cookie.split('=')[1],
        },
        data: JSON.stringify(request_data),
        success: function (response) {
            location.reload();
        },
        error: function(xhr, status, error) {
            location.reload();
        }
    });
}

function multi_number_check() {
    inputMultiNumber = document.getElementById('input_multi_number');
    inputMultiNumber.value.split('\n').forEach(item => {
        if (isNaN(item)) {
            inputMultiNumber.classList.add('error');
            document.getElementById('service_order_step_2').disabled = false;
        } else {
            inputMultiNumber.classList.remove('error');
            document.getElementById('service_order_step_2').disabled = true;
        }
    })
}

function username_validator() {
    document.getElementById('service_order_create_2').disabled = !document.getElementById('input_username').value
}

function service_order_create() {
    let number_email_date = []

    for (let i = 1; i < document.querySelectorAll('[name="number"]').length; i++) {
        number_email_date.push({
            name: document.querySelectorAll('[name="name"]')[i].value,
            number: document.querySelectorAll('[name="number"]')[i].value,
            reseller: document.querySelectorAll('[name="reseller"]')[i].value,
            email: document.querySelectorAll('[name="email"]')[i].value,
            requested_port_date: document.querySelectorAll('[name="requested_port_date"]')[i].value,
            e911_number: document.querySelectorAll('[name="e911_number"]')[i].value,
            e911_address: document.querySelectorAll('[name="e911_address"]')[i].value,
            service_status: document.querySelectorAll('[name="service_status"]')[i].value,
            voice_carrier: document.querySelectorAll('[name="voice_carrier"]')[i].value,
            sms_carrier: document.querySelectorAll('[name="sms_carrier"]')[i].value,
            sms_type: document.querySelectorAll('[name="sms_type"]')[i].value,
            sms_enabled: document.querySelectorAll('[name="sms_enabled"]')[i].value,
            sms_campaign: document.querySelectorAll('[name="sms_campaign"]')[i].value,
            extension: document.querySelectorAll('[name="extension"]')[i].value,
            onboard_date: document.querySelectorAll('[name="onboard_date"]')[i].value,
            e911_enabled_billed: document.querySelectorAll('[name="e911_enabled_billed"]')[i].value,
            note: document.querySelectorAll('[name="note"]')[i].value,
            service_1: document.querySelectorAll('[name="service_1"]')[i].value,
            service_2: document.querySelectorAll('[name="service_2"]')[i].value,
            service_3: document.querySelectorAll('[name="service_3"]')[i].value,
            service_4: document.querySelectorAll('[name="service_4"]')[i].value,
        })
    }

    const request_data = {
        username: document.getElementById('input_username').value,
        customer: document.getElementById('customer').value,
        term_location: document.getElementById('term_location').value,
        texting: document.getElementById('input_texting').value,
        number_email_date: number_email_date
    }

    $.ajax({
        url: `${window.location.origin}/service_order/create/`,
        method: 'POST',
        contentType: 'application/json', 
        headers: {
            'X-CSRFToken': document.cookie.split('=')[1],
        },
        data: JSON.stringify(request_data),
        success: function (response) {
            document.open();
            document.write(response);
            document.close();
            window.location.href = '/service_order/'
        },
        error: function(xhr, status, error) {
            location.reload();
        }
    });
}

function service_order_update() {
    let number_email_date = []
    let remove_numbers = []

    for (let i = 1; i < document.querySelectorAll('[name="number"]').length; i++) {
        number_email_date.push({
            id: document.querySelectorAll('[name="number"]')[i].id.split('number_')[1],
            name: document.querySelectorAll('[name="name"]')[i].value,
            number: document.querySelectorAll('[name="number"]')[i].value,
            reseller: document.querySelectorAll('[name="reseller"]')[i].value,
            email: document.querySelectorAll('[name="email"]')[i].value,
            requested_port_date: document.querySelectorAll('[name="requested_port_date"]')[i].value,
            e911_number: document.querySelectorAll('[name="e911_number"]')[i].value,
            e911_address: document.querySelectorAll('[name="e911_address"]')[i].value,
            service_status: document.querySelectorAll('[name="service_status"]')[i].value,
            voice_carrier: document.querySelectorAll('[name="voice_carrier"]')[i].value,
            sms_carrier: document.querySelectorAll('[name="sms_carrier"]')[i].value,
            sms_type: document.querySelectorAll('[name="sms_type"]')[i].value,
            sms_enabled: document.querySelectorAll('[name="sms_enabled"]')[i].value,
            sms_campaign: document.querySelectorAll('[name="sms_campaign"]')[i].value,
            extension: document.querySelectorAll('[name="extension"]')[i].value,
            onboard_date: document.querySelectorAll('[name="onboard_date"]')[i].value,
            e911_enabled_billed: document.querySelectorAll('[name="e911_enabled_billed"]')[i].value,
            note: document.querySelectorAll('[name="note"]')[i].value,
            service_1: document.querySelectorAll('[name="service_1"]')[i].value,
            service_2: document.querySelectorAll('[name="service_2"]')[i].value,
            service_3: document.querySelectorAll('[name="service_3"]')[i].value,
            service_4: document.querySelectorAll('[name="service_4"]')[i].value,
        })
    }

    for (let i = 2; i < document.querySelectorAll('tr').length; i++) {
        document.querySelectorAll('tr')[i].id && document.querySelectorAll('tr')[i].hidden == true ? remove_numbers.push(document.querySelectorAll('tr')[i].id) : '';
    }

    const request_data = {
        username: document.getElementById('input_username').value,
        customer: document.getElementById('customer').value,
        term_location: document.getElementById('term_location').value,
        texting: document.getElementById('input_texting').value,
        number_email_date: number_email_date,
        remove_numbers: remove_numbers
    }

    console.log(request_data);

    $.ajax({
        url: `${window.location.origin}/service_order/edit/${window.location.href.split('/')[window.location.href.split('/').length - 1]}`,
        method: 'POST',
        contentType: 'application/json', 
        headers: {
            'X-CSRFToken': document.cookie.split('=')[1],
        },
        data: JSON.stringify(request_data),
        success: function (response) {
            document.open();
            document.write(response);
            document.close();
            window.location.href = '/service_order/'
        },
        error: function(xhr, status, error) {
            location.reload();
        }
    });
}

function remove_number(remove_number_id) {
    remove_number_id.includes('_') ? document.getElementById(remove_number_id).remove() : document.getElementById(remove_number_id).hidden = true
    document.querySelectorAll('tr').length > 1 ? '' : document.getElementById('service_order_create_2').disabled = true;
}

function add_number() {
    let tbody = document.querySelector('tbody')
    let trElements = document.querySelectorAll('tr')
    if(trElements.length > 1) {
        let new_id = 'new_1';
        trElements.forEach(item => {
            item.id.includes('_') ? new_id = `new_${(Number(item.id.split('_')[1]) + 1)}` : '';
        })
        let trElementClone = trElements[1].cloneNode(true);
        trElementClone.hidden = false
        trElementClone.id = new_id; // Update the id of the cloned tr element

        // Get all first child elements of td tags within the cloned tr and update their IDs
        let firstChildElements = trElementClone.querySelectorAll("td > :first-child");
        firstChildElements.forEach((element) => {
            let baseId = element.id.substring(0, element.id.lastIndexOf("_") + 1); // Extract base ID without the numeric part
            element.id = baseId + new_id; // Update ID with new index
            if (element.tagName === "INPUT") {
                element.value = ""; // Reset text input value
            } else if (element.tagName === "SELECT") {
                element.selectedIndex = 0; // Reset select to the first option
            } else if (element.tagName === "BUTTON") {
                element.onclick = () => remove_number(new_id);
            }
        });

        tbody.appendChild(trElementClone);
        document.getElementById('service_order_create_2').disabled = true
        document.getElementById('number_'+new_id).oninput = () => change_num('number_', new_id);
        document.getElementById('email_'+new_id).oninput = () => change_email(new_id);
        document.getElementById('e911_number_'+new_id).oninput = () => change_num('e911_number_', new_id);
        document.getElementById('extension_'+new_id).oninput = () => change_num('extension_', new_id);
    } 
}