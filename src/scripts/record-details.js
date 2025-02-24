class toggleDetailsListDescriptions {
  constructor(checkbox, detailsList) {
    this.cookies = window.TNAFrontendCookies;

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
      this.cookies.exists("recordDetailDescriptions")
    ) {
      this.checkbox.checked = this.cookies.hasValue(
        "recordDetailDescriptions",
        "true",
      );
    }

    this.handleCheckboxChange(this.checkbox.checked);
  }

  handleCheckboxChange(show) {
    for (const item of this.detailsListItems) {
      if (show) {
        item.removeAttribute("hidden");
      } else {
        item.setAttribute("hidden", "");
      }
    }

    if (this.cookies.isPolicyAccepted("settings")) {
      this.cookies.set("recordDetailDescriptions", show);
    }
  }
}

const checkbox = document.getElementById("field-descriptions-show");
const detailsList = document.getElementById("record-details");
new toggleDetailsListDescriptions(checkbox, detailsList);
