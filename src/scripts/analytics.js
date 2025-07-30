import {
  GA4,
  helpers,
} from "@nationalarchives/frontend/nationalarchives/analytics.mjs";

const ga4Id = document.documentElement.getAttribute("data-ga4id");
if (ga4Id) {
  const analytics = new GA4({ id: ga4Id });

  analytics.addListeners(document.documentElement, "document", [
    {
      eventName: "double_click",
      on: "dblclick",
      data: {
        state: ($el, $scope, event) => helpers.getXPathTo(event.target),
        value: helpers.valueGetters.html,
      },
    },
  ]);

  analytics.addListeners(
    ".etna-details-hierarchy",
    "hierarchy",
    [
      {
        eventName: "select",
        targetElement: ".analytics-hierarchy-link",
        on: "click",
        data: {
          group: helpers.valueGetters.closestHeading,
        },
        rootData: {
          data_component_name: "catalogue_hierarchy",
          data_link: ($el) => $el.dataset.analyticsLevel,
          data_link_type: "link",
          data_position: helpers.valueGetters.index,
        },
      },
    ],
    "select_hierarchy",
  );
}
