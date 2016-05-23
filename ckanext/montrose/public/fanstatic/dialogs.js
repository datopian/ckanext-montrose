var map = new L.Map('hero_map', {scrollWheelZoom: false});

var osmUrl = 'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
var osmAttrib = 'Map data © <a href="http://openstreetmap.org">OpenStreetMap</a> contributors';
var osm = new L.TileLayer(osmUrl, {
  minZoom: 2,
  maxZoom: 8,
  attribution: osmAttrib
});

map.addLayer(osm);

var layers = [];
var geojson = {
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "properties": {
        name: 'Polygon 1'
      },
      "geometry": {
        "type": "Polygon",
        "coordinates": [
          [
            [
              39.2431640625,
              1.867345112921926
            ],
            [
              38.84765625,
              2.5040852618529215
            ],
            [
              39.287109375,
              2.986927393334876
            ],
            [
              39.3310546875,
              3.381823735328289
            ],
            [
              39.90234375,
              3.381823735328289
            ],
            [
              40.5615234375,
              2.745530718801952
            ],
            [
              40.93505859375,
              2.1088986592431382
            ],
            [
              41.02294921875,
              0.4833927027896987
            ],
            [
              40.341796875,
              0.3076157096439005
            ],
            [
              39.57275390625,
              0.856901647439813
            ],
            [
              39.2431640625,
              1.867345112921926
            ]
          ]
        ]
      }
    },
    {
      "type": "Feature",
      "properties": {
        name: 'Polygon 2'
      },
      "geometry": {
        "type": "Polygon",
        "coordinates": [
          [
            [
              35.15625,
              2.5040852618529215
            ],
            [
              35.859375,
              1.6477220517969353
            ],
            [
              36.27685546875,
              1.5159363834516861
            ],
            [
              36.27685546875,
              2.1308562777325313
            ],
            [
              35.8154296875,
              2.9430409100551445
            ],
            [
              35.595703125,
              4.19302960536076
            ],
            [
              34.6728515625,
              4.19302960536076
            ],
            [
              34.4091796875,
              3.491489430459778
            ],
            [
              35.15625,
              2.5040852618529215
            ]
          ]
        ]
      }
    },
    {
      "type": "Feature",
      "properties": {
        name: 'Point 1'
      },
      "geometry": {
        "type": "Point",
        "coordinates": [
          96.131591,
          16.823710
        ]
      }
    },
    {
      "type": "Feature",
      "properties": {
        name: 'Point 2'
      },
      "geometry": {
        "type": "Point",
        "coordinates": [
          40.6494140625,
          -2.3065056838291094
        ]
      }
    },
    {
      "type": "Feature",
      "properties": {
        name: 'Point 3'
      },
      "geometry": {
        "type": "Point",
        "coordinates": [
          96,
          6
        ]
      }
    }
  ]
};

var geoL = L.geoJson(geojson, {
  style: function (feature) {
    return feature.properties.style;
  },
  onEachFeature: function (feature, layer) {
    layer.bindPopup('<strong>' + feature.properties.name + '</strong>' + '<p>Information popup sample</p>');
    layer.name = feature.properties.name;
    layers.push(layer);
  }
}).addTo(map);

map.fitBounds(geoL.getBounds());

var select_dataset = $('.hero-select #dataset');

select_dataset.append('<option>Select Data Set</option>');

for (elem in layers) {
  select_dataset.append('<option>' + layers[elem].name + '</option>');
}