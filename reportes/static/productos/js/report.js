v$(function () {
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
        order: false,
        paging: false,
        ordering: false,
        info: false,
        searching: false,
        dom: 'Bfrtip',
        buttons: [
            {
                extend: 'excelHtml5',
                text: 'Descargar Excel <i class="fas fa-file-excel"></i>',
                titleAttr: 'Excel',
                className: 'btn btn-success btn-flat btn-xs'
            },

        ],


        columns: [
            {"data": "id_producto"},
            {"data": "nombre"},
            {"data": "precioVenta"},
            {"data": "stock"},
        ],
        columnDefs: [

        ],
        initComplete: function (settings, json) {

        }
    });
});