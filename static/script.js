'use strict';

window.addEventListener('load', function () {

  console.log("Hello World!");

});


const greeting = async () => {
  const url = `/greeting?username=${document.getElementById("userName").value}`;
  let response = await fetch(url);
  const userDataResponse = await response.json();
  console.log(userDataResponse);
  document.getElementById("buttonResponse").innerHTML = userDataResponse;
}