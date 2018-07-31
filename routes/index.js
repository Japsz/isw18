var express = require('express');
var router = express.Router();


/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index', { title: '' });
});

router.post('/get_actions',function(req, res, next){
    var PythonShell = require('python-shell');
    var pyshell = new PythonShell('/python/tests/actions.py',{args:[req.body.symbol,req.body.desde.replace(/\-/g,""),req.body.hasta.replace(/\-/g,"")]});
    var acciones = [];
    var caso = "texto";
    var sd,s_val;
    var maxdays = (new Date(req.body.hasta).getTime() - new Date(req.body.desde).getTime())/(1000*60*60*24);
// sends a message to the Python script via stdin
    pyshell.on('message', function (message) {
        if(message.split("@@").length > 1){
            caso = message.split("@@")[0];
        }else {
            switch(caso){
                case "texto":
                    acciones.push(message);
                    break;
                case "sd":
                    console.log("sigma:");
                    sd = parseFloat(message);
                    break;
                case "s_T":
                    s_val = parseFloat(message);
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
          res.send("ERROR"); //NOTA: Intentar retornar sin errores
          return;
        }
        console.log('The exit code was: ' + code);
        console.log('The exit signal was: ' + signal);
        console.log('finished');
        console.log(acciones);
        res.render('stock_rows',{data: acciones,maxdays: maxdays,sd:sd,s_val:s_val});
    });
});

router.post('/get_option',function(req,res,next){
    console.log(req.body);
    var PythonShell = require('python-shell');
    var pyshell = new PythonShell('/python/tests/test_yqd.py',{args:[parseFloat(req.body.t_riesgo),parseFloat(req.body.p_ejercicio),parseInt(req.body.t_mad)/365,parseInt(req.body.simulaciones),parseInt(req.body.intervalo),parseFloat(req.body.s_val),parseFloat(req.body.sd)]});
    var caso,valor_prom,opc_val;
    pyshell.on('message', function (message) {
        if(message.split("@@").length > 1){
            caso = message.split("@@")[0];
        }else{
            switch(caso){
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
        res.render('value_option',{data: opc_val,val_prom: valor_prom});

    });

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
                    console.log("sigma:");
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
        console.log(texto);
        res.render('stock_rows',{data: texto,sd:sd,opc:opc_val,prom:valor_prom});

    });
});

module.exports = router;
