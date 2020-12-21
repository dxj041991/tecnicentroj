var tblProducts;
var vents = {
    items: {
        cli: '',
        fecha: '',
        subtotal: 0.00,
        iva: 0.00,
        total: 0.00,
        products: []
    },

    calculate_invoice: function () {
        var subtotal = 0.00;
        var tot = 0.00;
        var iva = $('input[name="iva"]').val();
        $.each(this.items.products, function (pos, dict) {
            dict.pos = pos;
            dict.subtotal = (dict.cant * parseFloat(dict.precioVenta/1.12));
            tot += parseFloat(dict.precioVenta);
            subtotal += dict.subtotal;
        });
        this.items.subtotal = subtotal ;
        this.items.precio = tot/1.12;
        this.items.iva = this.items.subtotal * iva;
        this.items.total = this.items.subtotal + this.items.iva;

        $('input[name="subtotal"]').val(this.items.subtotal.toFixed(2));
        $('input[name="ivacalc"]').val(this.items.iva.toFixed(2));
        $('input[name="total"]').val(this.items.total.toFixed(2));
    },

    list: function (item) {
    this.calculate_invoice();
    tblProducts = $('#tblProducts').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        data : this.items.products,
        columns: [
            {"data": "id_producto"},
            {"data": "nombre"},
            {"data": "precioVenta"},
            {"data": "cant"},
            {"data": "subtotal"},

        ],


                columnDefs: [



            {
                    targets: [0],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<a rel="remove" class="btn btn-danger btn-xs btn-flat" style="color: white;"><i class="fas fa-trash-alt"></i></a>';
                    }
                },

            {
                    targets: [1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        if(row.id_producto==4)
                        return '<input type="text" name="nombre" class="form-control form-control-sm input-sm" autocomplete="off" value="' + row.nombre + '">';
                        else
                        return row.nombre;

                    }
                },

            {
                    targets: [2],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<input type="text" name="precioVenta" class="form-control form-control-sm input-sm" autocomplete="off" value="' + (row.precioVenta - row.precioVenta*0.12)+ '">';
                    }
                },

            {
                    targets: [3],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<input type="text" name="cant" class="form-control form-control-sm input-sm" autocomplete="off" value="' + row.cant + '">';
                    }
                },

        ],

        rowCallback(row, data, displayNum, displayIndex, dataIndex) {

                $(row).find('input[name="cant"]').TouchSpin({
                    min: 1,
                    max: 1000000000,
                    step: 1
                });

                $(row).find('input[name="precioVenta"]').TouchSpin({
                    min: 0,
                    max: 100,
                    step: 0.01,
                    decimals: 2,
                    boostat: 5,
                    maxboostedstep: 10,
                });

            },




        initComplete: function (settings, json) {

        }
    });
    }
    };

$(function () {
$('.select2').select2({
            theme:"bootstrap4",
            language: 'es'
        });
$('#fecha').datetimepicker({
        format: 'YYYY-MM-DD',
        date: moment().format("YYYY-MM-DD"),
        locale: 'es',
        minDate: moment().format("YYYY-MM-DD")
    });

$("input[name='iva']").TouchSpin({
        min: 0,
        max: 100,
        step: 0.01,
        decimals: 2,
        boostat: 5,
        maxboostedstep: 10,
        postfix: '%'
    }).on('change keyup', function () {
        vents.calculate_invoice();
    })
        .val(0.12);

$('input[name="search"]').autocomplete({
                source: function (request, response) {
                    $.ajax({
                        url: window.location.pathname,
                        type: 'POST',
                        data: {
                            'action': 'search_products',
                            'term': request.term
                        },
                        dataType: 'json',
                    }).done(function (data) {
                        response(data);
                    }).fail(function (jqXHR, textStatus, errorThrown) {
                        //alert(textStatus + ': ' + errorThrown);
                    }).always(function (data) {

                    });
                },
                delay: 500,
                minLength: 1,
                select: function (event, ui) {
                    event.preventDefault();
                    console.clean;
                    ui.item.cant=1;
                    ui.item.subtotal=0.00;
                    console.log(vents.items);
                    vents.items.products.push(ui.item);
                    vents.list();
                    $(this).val('');
                }
            });

 $('.btnRemoveAll').on('click', function () {
            if (vents.items.products.length === 0) return false;
            alert_action('Notificación', '¿Esta seguro de eliminar todos los productos de su detalle?', function (){
            vents.items.products = [];
            vents.list();
            });


    });

$('#tblProducts tbody')
        .on('click', 'a[rel="remove"]', function () {
            var tr = tblProducts.cell($(this).closest('td, li')).index();
            alert_action('Notificación', '¿Estas seguro de eliminar el producto de tu detalle?',
                function () {
                    vents.items.products.splice(tr.row, 1);
                    vents.list();
                }, function () {

                });
        })
        .on('change keyup', 'input[name="cant"]', function () {
            console.clear();
            var cant = parseInt($(this).val());
            var tr = tblProducts.cell($(this).closest('td, li')).index();
            vents.items.products[tr.row].cant = cant;
            vents.calculate_invoice();
            $('td:eq(4)', tblProducts.row(tr.row).node()).html('$' + vents.items.products[tr.row].subtotal.toFixed(2));

        }).on('change keyup', 'input[name="precioVenta"]', function () {
            console.clear();
            var precioVenta = parseFloat($(this).val());
            var tr = tblProducts.cell($(this).closest('td, li')).index();
            vents.items.products[tr.row].precioVenta = precioVenta;
            vents.calculate_invoice();
            $('td:eq(4)', tblProducts.row(tr.row).node()).html('$' + vents.items.products[tr.row].subtotal.toFixed(2));
        });




// event submit
    $('form').on('submit', function (e) {
        e.preventDefault();

        if (vents.items.products.length === 0) {
            message_error('Debe al menos tener un item en su detalle de venta');
            return false;
        }

        vents.items.fecha = $('input[name="fecha"]').val();
        vents.items.cli = $('select[name="cli"]').val();
        var parameters = new FormData();
        parameters.append('action', $('input[name="action"]').val());
        parameters.append('vents', JSON.stringify(vents.items));
        submit_with_ajax(window.location.pathname, 'Notificación',
            '¿Estas seguro de realizar la siguiente acción?', parameters, function (response) {
                alert_action('Notificación', '¿Desea imprimir su factura de venta?', function () {
                    window.open('/core/venta/invoice/pdf/' + response.id + '/', '_blank');
                    location.href = '/core/venta/listar';
                }, function () {
                    location.href = '/core/venta/listar';
                });
            });
    });

    vents.list();

});
