ckan.module('montrose_map', function ($, _) {
  "use strict";

  return {
    initialize: function () {
      var self = this;
      ckan.montrose.dashboardmap.init(this.options.id);
    }
  }
});