import data from "./data";

$("#select-type").select2();
$("body").on('click', '.select2-results__group', function() {
  $(this).siblings().toggle();
})
 data().then(resp=>resp.json()).then(console.log);