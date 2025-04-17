const $searchForm = document.getElementById("search-form");
const $sortFormGroup = document.getElementById("sort-form-group");
const $sort = document.getElementById("sort");
$sortFormGroup.parentElement
  .querySelector(".tna-button-group")
  ?.setAttribute("hidden", "");
$sort.addEventListener("change", () => {
  $searchForm.submit();
});
