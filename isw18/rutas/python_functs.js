var ejs = require("ejs");
var PythonShell = require('python-shell');
function buscar(simbolo,desde,hasta){
    var pyshell = new PythonShell('/python/tests/actions.py',{args:[simbolo,desde.replace(/\-/g,""),hasta.replace(/\-/g,"")]});
    var acciones = [];
    var caso = "texto";
    var sd,s_val;
    var maxdays = (new Date(hasta).getTime() - new Date(desde).getTime())/(1000*60*60*24);
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
            $("#fsubmit").html('<i class="glyphicon glyphicon-search" style="margin: 0;padding: 5px; font-size:35px;text-shadow:2px 2px 4px #000000"></i>');
            $("#estado").html("");
            $("#loader").removeClass("loader col-md-offset-6").addClass("");
            $("#form_option").removeClass("hidden").addClass("");
            $("#stock_rows").html(err);
            return 0;
        }
        ejs.renderFile("./views/stock_rows.ejs", {data: acciones,maxdays: maxdays,sd:sd,s_val:s_val}, function(err, str){
            // str => Rendered HTML string
            if(err){
                $("#fsubmit").html('<i class="glyphicon glyphicon-search" style="margin: 0;padding: 5px; font-size:35px;text-shadow:2px 2px 4px #000000"></i>');
                $("#estado").html("");
                $("#loader").removeClass("loader col-md-offset-6").addClass("");
                $("#form_option").removeClass("hidden").addClass("");
                $("#stock_rows").html(err);
                return 0;
            }
            $("#fsubmit").html('<i class="glyphicon glyphicon-search" style="margin: 0;padding: 5px; font-size:35px;text-shadow:2px 2px 4px #000000"></i>');
            $("#estado").html("");
            $("#loader").removeClass("loader col-md-offset-6").addClass("");
            $("#form_option").removeClass("hidden").addClass("");
            $("#stock_rows").html(str);
            return 1;
        });
    });

}

function get_opc_val (t_riesgo,p_ejercicio,t_mad,simulaciones,intervalo,s_val,sd){
    var pyshell = new PythonShell('/python/tests/test_yqd.py',{args:[parseFloat(t_riesgo),parseFloat(p_ejercicio),parseInt(t_mad)/365,parseInt(simulaciones),parseInt(intervalo),parseFloat(s_val),parseFloat(sd)]});
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
            $("#value_option").html(err);
            return 0;
        }
        ejs.renderFile("./views/value_option.ejs", {data: opc_val}, function(err, str){
            // str => Rendered HTML string
            if(err){
                $("#value_option").html(err);
                return 0;
            }
            $("#value_option").html(str);
            return 1;
        });

    });
}

function get_opc_val_r(t_riesgo,p_ejercicio,t_mad,simulaciones,intervalo,s_val,sd){
    const rscript = require('js-call-r');
    const result = rscript.callSync('./R/option.R', {
        r: t_riesgo,
        ej_price: p_ejercicio,
        T_num: t_mad,
        n_sims: simulaciones,
        n_intrv: intervalo,
        s_val: s_val,
        sd: sd
    });
    $("#value_option").html(result.result);
}