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

    if (document.getElementById('multi_standard')) {
        document.getElementById('multi_standard').disabled = document.querySelectorAll('.error').length > 0 ? true : false;
    }

    
    document.getElementById('service_order_detail_less')?.addEventListener('click', () => {
        $('#service_order_detail_show').fadeToggle(300)
        if (document.getElementById('show_hide_text').innerText === 'Show more detail') {
            document.getElementById('show_hide_text').innerText = 'Show less'
        } else {
            document.getElementById('show_hide_text').innerText = 'Show more detail'
        }
    })

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

function change_num(input_type ,id) {
    select_input = document.getElementById(input_type + id)
    if (/^\d+$/.test(select_input.value)) {
        select_input.classList.remove('error');
    } else {
        select_input.classList.add('error');
    }

    if (document.getElementById('multi_standard')) {
        document.getElementById('multi_standard').disabled = document.querySelectorAll('.error').length > 0 ? true : false;
    }
}

function change_select(select_type, id) {
    select_inbox = document.getElementById(select_type + id)
    if (select_inbox.value === '') {
        select_inbox.classList.add('error');
    } else {
        select_inbox.classList.remove('error');
    }

    if (document.getElementById('multi_standard')) {
        document.getElementById('multi_standard').disabled = document.querySelectorAll('.error').length > 0 ? true : false;
    }
}

function change_email(id) {
    email_input = document.getElementById('email_' + id)
    var regex = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    email_input.value.split(',').map(item => {
        if (regex.test(String(item.trim()).toLowerCase()) || email_input.value === '') {
            email_input.classList.remove('error');
        } else {
            email_input.classList.add('error');
        }
    })

    if (document.getElementById('multi_standard')) {
        document.getElementById('multi_standard').disabled = document.querySelectorAll('.error').length > 0 ? true : false;
    }
}

$(function () {
    $('[data-toggle="tooltip"]').tooltip()
})

function change_date(id) {
    date_input = document.getElementById('onboard_date_' + id)
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
        document.getElementById('multi_standard').disabled = document.querySelectorAll('.error').length > 0 ? true : false;
    }
}

function multi_submit() {
    data = document.querySelectorAll('tr')
    var request_data = []
    for (let i = 1; i < data.length; i++) {
        id = data[i].id;
        request_data.push({
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
            updated_by: document.getElementById('updated_by_' + id).value,
        })
    }

    $.ajax({
        url: `${window.location.origin}/did_standardization/multi_standardization`,
        method: 'POST',
        contentType: 'application/json', 
        headers: {
            'X-CSRFToken': document.cookie.split('=')[1],
        },
        data: JSON.stringify(request_data),
    });
    setTimeout(() => {
        location.reload();
    }, 300);
}
