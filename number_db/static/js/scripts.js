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
    for(let i in selectList) {
        selectList[i].checked = fullCheckAction.checked ? true : false;
    }
}

function oneCheck(status, id, event) {
    event.preventDefault();
    if (!status) {
    } else {
        var checkElemet = window.document.getElementById("select " + id);
        checkElemet.checked = !checkElemet.checked;
        checkElemet.checked === true ? selectCount++ : selectCount--;
        if (selectCount === selectList.length) {
            fullCheckAction.checked = true;
        } else {
            fullCheckAction.checked = false;
        }
    }
}

function oneCellCheck(id) {
    var checkElemet = window.document.getElementById("select " + id);
    checkElemet.checked = !checkElemet.checked;
    checkElemet.checked === true ? selectCount++ : selectCount--;
    if (selectCount === selectList.length) {
        fullCheckAction.checked = true;
    } else {
        fullCheckAction.checked = false;
    }
}

window.addEventListener('DOMContentLoaded', event => {

    // Toggle the side navigation
    const sidebarToggle = document.body.querySelector('#sidebarToggle');
    if (sidebarToggle) {
        // Uncomment Below to persist sidebar toggle between refreshes
        // if (localStorage.getItem('sb|sidebar-toggle') === 'true') {
        //     document.body.classList.toggle('sb-sidenav-toggled');
        // }
        sidebarToggle.addEventListener('click', event => {
            event.preventDefault();
            document.body.classList.toggle('sb-sidenav-toggled');
            localStorage.setItem('sb|sidebar-toggle', document.body.classList.contains('sb-sidenav-toggled'));
        });
    }

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