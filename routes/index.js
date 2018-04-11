var express = require('express');
var router = express.Router();


/* GET home page. */
router.get('/', function(req, res, next) {

  res.render('index', { title: 'Express' });
});
router.post('/get_quote',function(req, res, next){
    var PythonShell = require('python-shell');
    var pyshell = new PythonShell('/python/tests/test_yqd.py',{args:[req.body.symbol,req.body.desde.replace(/\-/g,""),req.body.hasta.replace(/\-/g,"")]});
    var texto = [];
    var caso = "texto";
    var sd,opc_val,valor_prom;
// sends a message to the Python script via stdin


    pyshell.on('message', function (message) {
        if(message.split("@@").length > 1){
            caso = message.split("@@")[0];
        }else{
            switch(caso){
                case "texto":
                    texto.push(message);
                    break;
                case "sd":
                    console.log(message);
                    break;
                case "opc":
                    opc_val = parseFloat(message);
                    break;
                case "s_T":
                    valor_prom = parseFloat(message);
                    break;
                default:
                    break;
            }
        }
        // received a message sent from the Python script (a simple "print" statement)
    });

// end the input stream and allow the process to exit
    pyshell.end(function (err,code,signal) {
        if (err){
          console.log("Python Error: %s",err);
          console.log(signal);
          res.send("ERROR");
          return;
        }
        console.log('The exit code was: ' + code);
        console.log('The exit signal was: ' + signal);
        console.log('finished');
        console.log(opc_val);
        res.render('stock_rows',{data: texto,sd:sd,opc:opc_val,prom:valor_prom});

    });


});

module.exports = router;
