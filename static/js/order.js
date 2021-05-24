    Chart.defaults.global.defaultFontFamily = '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
    
    Chart.defaults.global.defaultFontColor = '#292b2c';
    
    var ctx = document.getElementById("myBarChart");
    var myLineChart = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: ["OTT", "ITT", "TLB", "Bill Pay", "Other Service Fee", "CBX Relate Fee"],
        datasets: [{
          label: "Jtrust Service Offer",
          backgroundColor: "rgba(2,117,216,1)",
          borderColor: "rgba(2,117,216,1)",
          data: [100, 100, 150, 150, 50, 0],
        }],
      },
      options: {
        scales: {
          xAxes: [{
            time: {
              unit: 'Services'
            },
            gridLines: {
              display: false
            },
            ticks: {
              maxTicksLimit: 6
            }
          }],
        },
        legend: {
          display: false
        }
      }
    });
    
    // Configure Pusher instance
    const pusher = new Pusher('2690251fcfe4d024df15', {
        cluster: 'ap1',
        encrypted: true
    });
    
    // Subscribe to poll trigger
    var orderChannel = pusher.subscribe('order');
    
    // Listen to 'order placed' event
    var order = document.getElementById('order-count')
    orderChannel.bind('place', function(data) {
      myLineChart.data.datasets.forEach((dataset) => {
          dataset.data.fill(parseInt(data.units),-1);
      });
      myLineChart.update();
      order.innerText = parseInt(order.innerText)+1
    });