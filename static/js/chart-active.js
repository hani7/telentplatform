// ================================
// Template Name: Affan - PWA Mobile HTML Template
// Template Author: Designing World
// Template Author URL: https://themeforest.net/user/designing-world
// ================================

'use strict';

document.addEventListener("DOMContentLoaded", function () {

    /* ================================
      :: 1.0 Area Chart
    ================================ */

    const areaChartOne = document.getElementById('areaChartOne');

    if (areaChartOne) {
        var areaChartOneOptions = {
            series: [{
                name: 'Affan',
                data: [31, 40, 28, 51, 42, 109, 100]
            }, {
                name: 'Suha',
                data: [11, 32, 45, 32, 34, 52, 41]
            }],
            chart: {
                height: 240,
                type: 'area',
                zoom: {
                    enabled: false
                },
                toolbar: {
                    show: false
                },
            },
            dataLabels: {
                enabled: false
            },
            stroke: {
                curve: 'smooth'
            },
            xaxis: {
                type: 'datetime',
                labels: {
                    show: false
                },
                categories: ["2018-09-19T00:00:00.000Z", "2018-09-19T01:30:00.000Z", "2018-09-19T02:30:00.000Z", "2018-09-19T03:30:00.000Z", "2018-09-19T04:30:00.000Z", "2018-09-19T05:30:00.000Z", "2018-09-19T06:30:00.000Z"]
            },
            yaxis: {
                labels: {
                    offsetX: -10,
                    offsetY: 0,
                    style: {
                        colors: '#8480ae',
                        fontSize: '12px',
                    },
                }
            },
            tooltip: {
                x: {
                    format: 'dd/MM/yy HH:mm'
                },
            },
            tooltip: {
                theme: 'dark',
                marker: {
                    show: true,
                },
                x: {
                    show: false,
                }
            },
            subtitle: {
                text: 'This week sales',
                align: 'left',
                margin: 0,
                offsetX: 0,
                offsetY: 0,
                floating: false,
                style: {
                    fontSize: '14px',
                    color: '#8480ae'
                }
            },
            stroke: {
                show: true,
                curve: 'smooth',
                width: 3
            },
        };

        var chart1 = new ApexCharts(areaChartOne, areaChartOneOptions);
        chart1.render();
    }

    /* ================================
      :: 2.0 Column Chart
    ================================ */

    const columnChartOne = document.getElementById('columnChartOne');

    if (columnChartOne) {
        var options = {
            series: [{
                name: 'Actual',
                data: [{
                        x: '2011',
                        y: 1292,
                        goals: [{
                            name: 'Expected',
                            value: 1400,
                            strokeHeight: 5,
                            strokeColor: '#8480ae'
                        }]
                    },
                    {
                        x: '2012',
                        y: 4432,
                        goals: [{
                            name: 'Expected',
                            value: 5400,
                            strokeHeight: 5,
                            strokeColor: '#8480ae'
                        }]
                    },
                    {
                        x: '2013',
                        y: 5423,
                        goals: [{
                            name: 'Expected',
                            value: 5200,
                            strokeHeight: 5,
                            strokeColor: '#8480ae'
                        }]
                    },
                    {
                        x: '2014',
                        y: 6653,
                        goals: [{
                            name: 'Expected',
                            value: 6500,
                            strokeHeight: 5,
                            strokeColor: '#8480ae'
                        }]
                    },
                    {
                        x: '2015',
                        y: 8133,
                        goals: [{
                            name: 'Expected',
                            value: 6600,
                            strokeHeight: 13,
                            strokeLineCap: 'round',
                            strokeColor: '#8480ae'
                        }]
                    },
                    {
                        x: '2016',
                        y: 7132,
                        goals: [{
                            name: 'Expected',
                            value: 7500,
                            strokeHeight: 5,
                            strokeColor: '#8480ae'
                        }]
                    },
                    {
                        x: '2017',
                        y: 7332,
                        goals: [{
                            name: 'Expected',
                            value: 8700,
                            strokeHeight: 5,
                            strokeColor: '#8480ae'
                        }]
                    },
                    {
                        x: '2018',
                        y: 6553,
                        goals: [{
                            name: 'Expected',
                            value: 7300,
                            strokeHeight: 2,
                            strokeDashArray: 2,
                            strokeColor: '#8480ae'
                        }]
                    }
                ]
            }],
            chart: {
                height: 250,
                type: 'bar',
                toolbar: {
                    show: false
                }
            },
            plotOptions: {
                bar: {
                    columnWidth: '60%'
                }
            },
            colors: ['#00E396'],
            dataLabels: {
                enabled: false
            },
            xaxis: {
                labels: {
                    style: {
                        colors: '#8480ae',
                        fontSize: '12px'
                    }
                },
                axisBorder: {
                    show: true,
                    color: '#8480ae'
                },
                axisTicks: {
                    show: true,
                    color: '#8480ae'
                }
            },
            yaxis: {
                labels: {
                    style: {
                        colors: '#8480ae',
                        fontSize: '12px'
                    }
                },
                axisBorder: {
                    show: true,
                    color: '#8480ae'
                },
                axisTicks: {
                    show: true,
                    color: '#8480ae'
                }
            },

            legend: {
                show: true,
                showForSingleSeries: true,
                customLegendItems: ['Actual', 'Expected'],
                markers: {
                    fillColors: ['#00E396', '#8480ae']
                }
            }
        };

        var chart = new ApexCharts(columnChartOne, options);
        chart.render();
    }

    /* ================================
      :: 3.0 Line Chart
    ================================ */

    const lineChartOne = document.getElementById('lineChartOne');

    if (lineChartOne) {
        var lineChartOneOptions = {
            chart: {
                height: 180,
                type: 'line',
                zoom: {
                    enabled: false
                },
                toolbar: {
                    show: false
                },
            },
            colors: ['#0134d4'],
            dataLabels: {
                enabled: false
            },
            stroke: {
                curve: 'smooth'
            },
            title: {
                text: 'Last 6 month sales',
                align: 'center',
                margin: 0,
                offsetX: 0,
                offsetY: 0,
                floating: true,
                style: {
                    fontSize: '14px',
                    color: '#8480ae',
                    fontWeight: '500',
                    fontFamily: 'Google Sans, sans-serif',
                }
            },
            tooltip: {
                theme: 'dark',
                marker: {
                    show: true,
                },
                x: {
                    show: false,
                }
            },
            grid: {
                borderColor: '#dbeaea',
                strokeDashArray: 4,
                xaxis: {
                    lines: {
                        show: true
                    }
                },
                yaxis: {
                    lines: {
                        show: false,
                    }
                },
                padding: {
                    top: 0,
                    right: 0,
                    bottom: 0,
                    left: 0
                },
            },
            series: [{
                name: "Affan",
                data: [100, 401, 305, 501, 409, 602]
            }],
            xaxis: {
                categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
                crosshairs: {
                    show: true
                },
                labels: {
                    offsetX: 0,
                    offsetY: 0,
                    style: {
                        colors: '#8380ae',
                        fontSize: '12px'
                    },
                },
                tooltip: {
                    enabled: false,
                },
            },
            yaxis: {
                labels: {
                    offsetX: -10,
                    offsetY: 0,
                    style: {
                        colors: '#8380ae',
                        fontSize: '12px'
                    },
                }
            },
        };

        new ApexCharts(lineChartOne, lineChartOneOptions).render();
    }

    /* ================================
      :: 4.0 Line Chart 2
    ================================ */

    const lineChartTwo = document.getElementById('lineChartTwo');

    if (lineChartTwo) {
        var lineChartTwoOptions = {
            chart: {
                height: 160,
                type: 'line',
                zoom: {
                    enabled: false
                },
                toolbar: {
                    show: false
                },
            },
            colors: ['#2ecc4a'],
            dataLabels: {
                enabled: false
            },
            stroke: {
                curve: 'smooth'
            },
            title: {
                text: '',
                align: 'center',
                margin: 0,
                offsetX: 0,
                offsetY: 0,
                floating: true,
                style: {
                    fontSize: '14px',
                    color: '#8480ae',
                }
            },
            tooltip: {
                theme: 'dark',
                marker: {
                    show: true,
                },
                x: {
                    show: false,
                }
            },
            grid: {
                borderColor: '#dbeaea',
                strokeDashArray: 4,
                xaxis: {
                    lines: {
                        show: true
                    }
                },
                yaxis: {
                    lines: {
                        show: false,
                    }
                },
                padding: {
                    top: 0,
                    right: 0,
                    bottom: 0,
                    left: 0
                },
            },
            series: [{
                name: "Affan",
                data: [15, 18, 16, 17, 14, 13, 19]
            }],
            xaxis: {
                categories: ['Sat', 'Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri'],
                crosshairs: {
                    show: true
                },
                labels: {
                    offsetX: 0,
                    offsetY: 0,
                    style: {
                        colors: '#8380ae',
                        fontSize: '12px'
                    },
                },
                tooltip: {
                    enabled: false,
                },
            },
            yaxis: {
                labels: {
                    offsetX: -10,
                    offsetY: 0,
                    style: {
                        colors: '#8380ae',
                        fontSize: '12px'
                    },
                }
            }
        };

        new ApexCharts(lineChartTwo, lineChartTwoOptions).render();
    }

    /* ================================
      :: 5.0 Pie Chart
    ================================ */

    const pieChartOne = document.getElementById('pieChartOne');

    if (pieChartOne) {
        var pieChartOneOptions = {
            chart: {
                width: 260,
                type: 'pie',
                sparkline: {
                    enabled: true
                },
                dropShadow: {
                    enabled: false,
                },
            },
            colors: ['#0134d4', '#2ecc4a', '#ea4c62', '#1787b8'],
            series: [100, 55, 63, 77],
            labels: ['Business', 'Marketing', 'Admin', 'Ecommerce'],
        };

        new ApexCharts(pieChartOne, pieChartOneOptions).render();
    }

    /* ================================
      :: 6.0 Donut Chart
    ================================ */

    const donutChartOne = document.getElementById('donutChartOne');

    if (donutChartOne) {
        var donutChartOneOptions = {
            chart: {
                width: 260,
                type: 'donut',
                sparkline: {
                    enabled: true
                },
                dropShadow: {
                    enabled: false,
                },
            },
            colors: ['#0134d4', '#2ecc4a', '#ea4c62', '#1787b8'],
            series: [100, 55, 63, 77],
            labels: ['Business', 'Marketing', 'Admin', 'Ecommerce'],
        };

        new ApexCharts(donutChartOne, donutChartOneOptions).render();
    }

});