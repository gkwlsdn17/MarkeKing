getAgeChart();
getSexChart();
getSignUpChart();

function getAgeChart(){
    $.ajax({
        type: 'GET',
        url: '/customer/statistics/chart/age/',
        success: function (data) {
            data = JSON.parse(data)
            var ctx = $("#chart_age").get(0).getContext("2d");
            new Chart(ctx, {
                type: 'pie',
                data: {
                    datasets: [{
                        data: data['values'],
                        backgroundColor: ["#0074D9", "#FF4136", "#2ECC40", "#FF851B", "#7FDBFF", "#B10DC9", "#FFDC00", "#001f3f", "#39CCCC", "#01FF70", "#85144b", "#F012BE", "#3D9970", "#111111", "#AAAAAA"]
                    }],
                    labels: data['keys']
                },
                options: pieOption
            });
        }
    });
    
    var pieOption = {
        plugins: {
            datalabels: {
                formatter: (value, ctx) => {
                    let datasets = ctx.chart.data.datasets;
                    if (datasets.indexOf(ctx.dataset) === datasets.length - 1) {
                        let sum = datasets[0].data.reduce((a, b) => a + b, 0);
                        let percentage = Math.round((value / sum) * 100) + '%';
                        return percentage;
                    } else {
                        return percentage;
                    }
                },
                color: '#fff'
            }
        }
    };
    
}

function getSexChart(){
    $.ajax({
        type: 'GET',
        url: '/customer/statistics/chart/sex/',
        success: function (data) {
            data = JSON.parse(data)
            var ctx = $("#chart_sex").get(0).getContext("2d");
            new Chart(ctx, {
                type: 'pie',
                data: {
                    datasets: [{
                        data: data['values'],
                        backgroundColor: ["#0074D9", "#FF4136", "#2ECC40", "#FF851B", "#7FDBFF", "#B10DC9", "#FFDC00", "#001f3f", "#39CCCC", "#01FF70", "#85144b", "#F012BE", "#3D9970", "#111111", "#AAAAAA"]
                    }],
                    labels: data['keys']
                },
                options: pieOption
            });
        }
    });
    
    var pieOption = {
        plugins: {
            datalabels: {
                formatter: (value, ctx) => {
                    let datasets = ctx.chart.data.datasets;
                    if (datasets.indexOf(ctx.dataset) === datasets.length - 1) {
                        let sum = datasets[0].data.reduce((a, b) => a + b, 0);
                        let percentage = Math.round((value / sum) * 100) + '%';
                        return percentage;
                    } else {
                        return percentage;
                    }
                },
                color: '#fff'
            }
        }
    };
}

function getSignUpChart(){
    $.ajax({
        type: 'GET',
        url: '/customer/statistics/chart/signUp/',
        success: function (data) {
            data = JSON.parse(data)
            var ctx = $("#chart_signUp").get(0).getContext("2d");
            new Chart(ctx, {
                type: 'line',
                data: {
                    datasets: [{
                        data: data['values'],
                        borderColor: 'rgb(75, 192, 192)',
                        label: '회원가입수',
                        tension: 0.1,
                        fill: false
                    }],
                    labels: data['keys'],

                }
                
            });
        }
    });
    
}