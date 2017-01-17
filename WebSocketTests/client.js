var ws = new WebSocket("ws://nathantouch:9999/");
ws.onopen = function() {
    function schedule(i) {
        setTimeout(function() { 
          ws.send('Hello from the client! (iteration ' + i + ')');
          schedule(i + 1);
        }, 1000);            
    };
    schedule(1);            
};