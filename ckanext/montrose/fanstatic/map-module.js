ckan.module('montrose_map', function ($, _) {
  "use strict";

  return {
    initialize: function () {
      
      ckan.montrose.dashboardmap.init(this.options.id, this.options.countryname, this.options.mapurl);
    }
  }
});