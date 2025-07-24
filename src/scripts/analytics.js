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
        // eslint-disable-next-line no-unused-vars
        state: ($el, $scope, event, index) => helpers.getXPathTo(event.target),
        // eslint-disable-next-line no-unused-vars
        value: ($el, $scope, event, index) => event.target.innerHTML,
      },
    },
  ]);

  analytics.addListeners('.etna-details-hierarchy', 'hierarchy',[
    {
      eventName: "select",
      rootEventName: "select_hierarchy",
      targetElement: ".analytics-hierarchy-link",
      on: "click",
      data: {
        position: helpers.valueGetters.index,
        section: ($el) => helpers.getClosestHeading($el),
      },
      rootData: {
        data_component_name: "catalogue_hierarchy",
        data_link: ($el) => $el.dataset.analyticsLevel,
        data_link_type: "link",
        data_position: helpers.valueGetters.index,
      },
    }
  ]);
}
