
document.addEventListener('DOMContentLoaded', function() {
    var elems = document.querySelectorAll('select');
    var instances = M.FormSelect.init(elems, {});
  });

let collectionSelect = document.getElementById('collection_select');
    collectionSelect.addEventListener('change', function() {
        let form = document.getElementById('form');
        let collectionId = collectionSelect.value;
        const action = form.getAttribute("action");
        const newAction = action.replace("/0/", `/${collectionId}/`);
        form.setAttribute('action', newAction);
        let button = document.getElementById('submit');
        button.disabled = false;

    });