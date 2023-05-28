'use strict';

window.addEventListener('load', function () {

  console.log("Hello World!");

});


const showOAuth = async () => {
  window.location.href = '/login';
};

const logout = async () => {
  window.location.href = '/logout';
};