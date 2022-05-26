// Based on w3schools
// https://www.w3schools.com/howto/howto_js_autocomplete.asp

function autocomplete(input, array, error_p) {
  let currentFocus;
  input.addEventListener("blur", function(e){
      let value = this.value;
      if(!array.includes(value) && value){
        error_p.style.visibility = "visible";
        let form = document.querySelector("form");
        form.onsubmit = function() {
          return false;
        }
      }
      else{
        error_p.style.visibility = "hidden";
        let form = document.querySelector("form");
        form.onsubmit = function() {
          return true;
        }
      }
  })

  input.addEventListener("input", function(e) {
      let autocompleteList, listItem
      let value = this.value;
      removeList();
      if (!value) {
        return false;
      }
      currentFocus = -1;
      autocompleteList = document.createElement("DIV");
      autocompleteList.setAttribute("id", this.id + "autocomplete-list");
      autocompleteList.setAttribute("class", "autocomplete-items");
      this.parentNode.appendChild(autocompleteList);
      for (let i = 0; i < array.length; i++) {
        if (array[i].substr(0, value.length).toUpperCase() == value.toUpperCase()) {
          listItem = document.createElement("DIV");
          listItem.innerHTML = "<strong>" + array[i].substr(0, value.length) + "</strong>";
          listItem.innerHTML += array[i].substr(value.length);
          listItem.innerHTML += "<input type='hidden' value='" + array[i] + "'>";

          listItem.addEventListener("click", function(e) {
              input.value = this.getElementsByTagName("input")[0].value;
              error_p.style.visibility = "hidden";
              removeList();
              let form = document.querySelector("form");
              form.onsubmit = function() {
                return true;
              }
          });
          autocompleteList.appendChild(listItem);
        }
      }
  });

  function removeList(element) {
    let autocomplete_items = document.getElementsByClassName("autocomplete-items");
    for (let i = 0; i < autocomplete_items.length; i++) {
      if (element != autocomplete_items[i] && element != input) {
        autocomplete_items[i].parentNode.removeChild(autocomplete_items[i]);
      }
    }
  }
  document.addEventListener("click", function (e) {
      removeList(e.target);
  });
}
