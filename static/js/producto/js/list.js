$(function () {
    $('#data').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            data: {
                'action': 'searchdata'
            },
            dataSrc: ""
        },


        columns: [
            {"data": "id_producto"},
            {"data": "nombre"},
            {"data": "precioVenta"},
            {"data": "stock"},
            {"data": "observaciones"},
            {"data": "observaciones"},
        ],
        columnDefs: [
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons1 = '<a href="/core/producto/editar/' + row.id_producto + '/" class="btn btn-warning btn-xs btn-flat"><i class="fas fa-edit"></i></a> ';
                    buttons1 += '<a href="/core/producto/eliminar/' + row.id_producto + '/" type="button" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a>';
                    return buttons1;
                }
            },

            {
                targets: [-3],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    if (row.stock>=10 && row.stock<=20)
                    return '<div class="card bg-warning"><h5>'+row.stock+'</h5></div>';
                    if (row.stock<=9)
                    return '<div class="card bg-danger"><h4>'+row.stock+'</h4></div>';
                    else
                    return '<div class="card bg-success">'+row.stock+'</div>';
                }
            },
        ],
        initComplete: function (settings, json) {

        }
    });
});