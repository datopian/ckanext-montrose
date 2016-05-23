$(document).ready(function () {

  var chart_colors = ['#B80000', '#995522', '#556677', '#118888', '#115588', '#4C3D3D', '#2B2B2B', '#660000', '#221100'];

  var chart_gas = c3.generate({
    bindto: '#chart_gas',
    padding: {
      top: 20,
      left: 30,
      right: 30
    },
    data: {
      columns: [
        ['data1', 30, 200, 100, 400, 150, 250],
        ['data2', 50, 20, 10, 40, 15, 25],
        ['data3', 120, 40, 50, 300, 200, 50]
      ]
    },
    legend: {
      show: false
    },
    color: {
      pattern: chart_colors
    }
  });

  var chart_mining = c3.generate({
    bindto: '#chart_mining',
    padding: {
      top: 20
    },
    data: {
      json: [{
          "name": "Rafined Gold",
          "value": 100
        }, {
          "name": "Rafined Silver",
          "value": 200
        }, {
          "name": "Antimonial Lead",
          "value": 500
        }, {
          "name": "Nickel Speiss",
          "value": 4000
        }],
      keys: {
        x: 'name',
        value: ["value"]
      },
      type: 'bar'
    },
    axis: {
      rotated: true, // horizontal bar chart
      x: {
        type: 'category' // this needed to load string x value
      }
    },
    grid: {
      x: {
        show: true
      },
      y: {
        show: true
      }
    },
    legend: {
      show: false
    },
    color: {
      pattern: chart_colors
    }
  });

  var chart_gdp = c3.generate({
    bindto: '#chart_gdp',
    padding: {
      top: 20,
      left: 20
    },
    data: {
      x: 'x',
      columns: [
        ['x', '2012', '2013', '2014', '2015'],
        ['data1', 12.03, 13.84, 13.64, 8.24]
      ],
      type: 'bar',
      labels: true
    },
    grid: {
      y: {
        show: true
      }
    },
    legend: {
      show: false
    },
    color: {
      pattern: chart_colors
    }
  });

  var chart_shore = c3.generate({
    bindto: '#chart_shore',
    padding: {
      top: 20,
      left: 20
    },
    data: {
      columns: [
        ['Azerbeijan', 30, 200, 100, 400, 150],
        ['France', 50, 20, 10, 40, 15, 25],
        ['Malaysia', 50, 20, 10, 40, 15, 25],
        ['South Korea', 50, 20, 10, 40, 15, 25],
        ['China', 50, 20, 150, 40, 15, 25],
        ['Myanmar', 50, 20, 40, 40, 15, 25],
        ['Vietnam', 50, 20, 40, 40, 15, 25],
        ['Singapore', 50, 20, 40, 40, 15, 25]
      ],
      type: 'pie'
    },
    legend: {
      position: 'right'
    },
    color: {
      pattern: chart_colors
    }
  });

  var chart_population = c3.generate({
    bindto: '#chart_population',
    padding: {
      top: 20,
      left: 30,
      right: 10
    },
    data: {
      x: 'x',
      columns: [
        ['x', '2011', '2012', '2013', '2014', '2015'],
        ['data1', 30, 200, 100, 400, 150, 250]
      ],
      type: 'spline'
    },
    grid: {
      y: {
        show: true
      }
    },
    legend: {
      show: false
    },
    color: {
      pattern: chart_colors
    }
  });

});