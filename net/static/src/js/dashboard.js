odoo.define('net.dashboard', 
function (require) {
    "use strict";
    
    //var ControlPanelMixin = require('web.ControlPanelMixin');
    var AbstractAction = require('web.AbstractAction');
    var ajax = require('web.ajax');
    var core = require('web.core');
    var rpc = require('web.rpc');
    var session = require('web.session');
    var web_client = require('web.web_client');
    var _t = core._t;
    var QWeb = core.qweb;


    var netDashboard = AbstractAction.extend({
        template: 'net.dashboard_template',
        events: {
        },
        init: function(parent, context) {
            this._super(parent, context);
            console.log(parent);
            console.log(context);
            this.date_range = 'week';  // possible values : 'week', 'month', year'
            var self = this;
            //Primera funcion en ejecurat
            console.log("INIT FUNCTION 1");
        },
        
        willStart: function() {
            //segunda funcion en ejecurat
            console.log("WILLSTART FUNCTION")
            return $.when(ajax.loadLibs(this), this._super());
        },
        start: function() {
            //Tercera funcion en ejecutar
            console.log("START FUNCTION")
            var self = this;
            
            this.set("title", 'Dashboard X');
            return this._super().then(function() {
                self._rpc({
                    model: 'net.memory',
                    method: 'get_memory_history',
                }, []).then(function(result){
                    self.mem_bar_ds = result.mem_bar_ds
                    self.mem_history_ds = result.mem_history_ds
                    self.cpu_load_history_ds = result.cpu_load_history_ds
                    self.cpu_usage_history_ds = result.cpu_usage_history_ds

                    console.log("LLAMADA RPC FINALIZADA")
                    self.render();            
                    //self.employee_data = result[0]
                });                
                //self.$el.parent().addClass('oe_background_grey');
            });
        },
        

        render: function() {
            var self = this;
            //console.log(QWeb.render('net.chart_dash', {widget: self}))
            //$('#myDash').append(QWeb.render('net.chart_dash', { widget: self }));
            var theDashboard = QWeb.render( 'net.chart_dash', { widget: self });
            $(theDashboard).appendTo(self.$el);
            self.graph();
            //return theDashboard;
        },
          // Function which gives random color for charts.
        getRandomColor: function () {
            var letters = '0123456789ABCDEF'.split('');
            var color = '#';
            for (var i = 0; i < 6; i++ ) {
                color += letters[Math.floor(Math.random() * 16)];
            }
            return color;
        },
        graph: function() {
            var self = this;
                                                
            
            var base_history_layout = {
                 height: 350,
                 yaxis: {
                    title:'% Uso', 
                    hoverformat: '.1f %',
                    zeroline: true,
                    showline: true,
                }, 
                 xaxis: {title:'Fecha', showgrid: false, showline: true,}
            };
            // Hcaer copia profunda del objeto de lo contrario todos referencian al mismo objeto y los cambios se sobreescriben
            var cpu_load_layout = $.extend( true, {}, base_history_layout );
            var cpu_usage_layout = $.extend( true, {}, base_history_layout );
            var mem_usage_layout = $.extend( true, {}, base_history_layout );
            var mem_usage_bar_layout = $.extend( true, {}, base_history_layout);

            cpu_load_layout.title = "Historial de carga de CPU";
            cpu_usage_layout.title = "Historial de uso de CPU";
            mem_usage_layout.title = "Historial de uso real de memoria";
            mem_usage_bar_layout.title = "Uso de memoria RAM";
            mem_usage_bar_layout.barmode =  'stack';
            mem_usage_bar_layout.xaxis.zeroline = true;

            Plotly.newPlot('myChart2', self.mem_history_ds, mem_usage_layout, {editable: true});
            Plotly.newPlot('cpu_load', self.cpu_load_history_ds, cpu_load_layout, {editable: true});
            Plotly.newPlot('cpu_usage', self.cpu_usage_history_ds, cpu_usage_layout, {editable: true});
            Plotly.newPlot('mem_chart', self.mem_bar_ds, mem_usage_bar_layout ,{editable: true});
            
        }

    });

    core.action_registry.add('net_dashboard', netDashboard);

    return netDashboard;

});