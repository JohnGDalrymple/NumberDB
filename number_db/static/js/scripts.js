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
  element.addEventListener('click', (event) => {
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