import { Cookies } from "@nationalarchives/frontend/nationalarchives/all.mjs";

class toggleDetailsListDescriptions {
  constructor(checkbox, detailsList, cookies) {
    this.cookies = cookies;

    this.checkbox = checkbox;
    this.formGroup = this.checkbox.closest(".tna-form__group");

    this.detailsList = detailsList;
    this.detailsListItems = this.detailsList.querySelectorAll(
      ".record-details__description",
    );

    if (this.detailsListItems.length === 0) {
      return;
    }

    if (this.formGroup) {
      this.showFormGroup();
    }

    this.setUpCheckbox();
  }

  showFormGroup() {
    this.formGroup.removeAttribute("hidden");
    this.formGroup
      .querySelector(".tna-form__legend")
      ?.classList.add("tna-visually-hidden");
  }

  setUpCheckbox() {
    this.checkbox?.addEventListener("change", (event) =>
      this.handleCheckboxChange(event.target.checked),
    );

    if (
      this.cookies.isPolicyAccepted("settings") &&
      this.cookies.exists("hide_record_detail_descriptions")
    ) {
      this.checkbox.checked = this.cookies.hasValue(
        "hide_record_detail_descriptions",
        "true",
      );
    }
    console.log(this.checkbox);
    console.log(this.checkbox.checked);

    this.handleCheckboxChange(this.checkbox.checked);
  }

  handleCheckboxChange(hide) {
    console.log(hide);
    for (const item of this.detailsListItems) {
      if (hide) {
        item.setAttribute("hidden", "");
      } else {
        item.removeAttribute("hidden");
      }
    }

    if (this.cookies.isPolicyAccepted("settings")) {
      this.cookies.set("hide_record_detail_descriptions", hide);
    }
  }
}

const checkbox = document.getElementById("field-descriptions-hide");
const detailsList = document.getElementById("record-details");
console.log(checkbox, detailsList);
new toggleDetailsListDescriptions(checkbox, detailsList, new Cookies());
