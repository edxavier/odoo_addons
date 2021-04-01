odoo.define('net.detail_dash', 
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


    var netDetailDash = AbstractAction.extend({
        template: 'net.detail_dash_template',
        events: {
        },
        init: function(parent, context) {
            this._super(parent, context);
            //console.log(context);
            this.host_id = context.context.host_id;
            this.host_name = context.context.host_name;
            //Primera funcion en ejecurat
            //console.log("INIT FUNCTION 1");
        },
        
        willStart: function() {
            //segunda funcion en ejecurat
            //console.log("WILLSTART FUNCTION")
            return $.when(ajax.loadLibs(this), this._super());
        },        
       start: function() {
            //Tercera funcion en ejecutar
            //console.log("START FUNCTION")
            var self = this;        
            //this.set("title", 'Dashboard X');
        
            return this._super().then(function() {
                self._rpc({
                    model: 'net.host.performance',
                    method: 'get_perfomance_details',
                    args: [self.host_id]
                }, []).then(function(result){
                    self.mem_bar_ds = result.mem_bar_ds
                    self.cpu_pie_ds = result.cpu_pie_ds

                    self.mem_history_ds = result.mem_history_ds
                    self.cpu_load_history_ds = result.cpu_load_history_ds
                    self.cpu_usage_history_ds = result.cpu_usage_history_ds
                    self.cpu_io_ds = result.cpu_io_ds
                    self.processes_ds = result.processes_ds

                    self.cpu_ctx_sw_int = result.cpu_ctx_sw_int
                    //console.log("LLAMADA RPC FINALIZADA")
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
            var theDashboard = QWeb.render( 'net.detail_chart_dash', { widget: self });
            $(theDashboard).appendTo(self.$el);
            self.graph();
            //return theDashboard;
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
            var processes_layout = $.extend( true, {}, base_history_layout );
            var cpu_usage_layout = $.extend( true, {}, base_history_layout );
            var mem_usage_layout = $.extend( true, {}, base_history_layout );
            var mem_usage_bar_layout = $.extend( true, {}, base_history_layout );
            var io_layout = $.extend( true, {}, base_history_layout);
            var ctx_interrups_layout = $.extend( true, {}, base_history_layout);


            processes_layout.title = "Historial procesos y tareas";
            cpu_load_layout.title = "Historial carga de CPU";
            cpu_usage_layout.title = "Historial uso de CPU";
            mem_usage_layout.title = "Historial uso de memoria";
            mem_usage_bar_layout.title = "Uso de memoria RAM";
            io_layout.title = "Actividad de lectura y escritura";
            ctx_interrups_layout.title = "Cambios de contexto e interrupciones";

            processes_layout.yaxis.title = "Total";
            ctx_interrups_layout.yaxis.title = "Transacciones/s";
            io_layout.yaxis.title = "Bloques/s";
            //mem_usage_bar_layout.barmode =  'stack';
            mem_usage_bar_layout.xaxis.zeroline = true;

            Plotly.newPlot('processes_chart', self.processes_ds, processes_layout, {editable: true});
            Plotly.newPlot('cpu_ctxsw_int', self.cpu_ctx_sw_int, ctx_interrups_layout, {editable: true});
            Plotly.newPlot('cpu_load', self.cpu_load_history_ds, cpu_load_layout, {editable: true});
            Plotly.newPlot('cpu_usage', self.cpu_usage_history_ds, cpu_usage_layout, {editable: true});
            Plotly.newPlot('io_chart', self.cpu_io_ds, io_layout, {editable: true});
            
            Plotly.newPlot('mem_hist_chart', self.mem_history_ds, mem_usage_layout, {editable: true});
            
            
            Plotly.newPlot('mem_bar_chart', self.mem_bar_ds, mem_usage_bar_layout ,{editable: true});
            Plotly.newPlot('cpu_usage_bar_chart', self.cpu_pie_ds, cpu_usage_layout ,{editable: true});
            
        }

    });

    core.action_registry.add('net_detail_dash', netDetailDash);

    return netDetailDash;

});