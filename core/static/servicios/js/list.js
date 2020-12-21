function getData() {
tblClient= $('#data').DataTable({
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
            {"data": "id_servicio"},
            {"data": "veh.client.NombreCliente"},
            {"data": "veh.placa"},
            {"data": "fecha"},
            {"data": "descr"},
            {"data": "descr"},

        ],
        columnDefs: [
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = '<a href="/core/test/editar/' + row.id_servicio + '/" class="btn btn-info btn-xs btn-flat"><i class="fas fa-file-pdf"></i></a> ';
                    buttons += '<a href="#' + row.id_servicio + '/" type="button" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a> ';
                    return buttons;
                }
            },
        ],
        initComplete: function (settings, json) {

        }
    });
}

$(function () {

    modal_title = $('.modal-title');

    getData();

    $('.btnAdd').on('click', function () {
        $('input[name="action"]').val('add');
        modal_title.find('span').html('Creación de un cliente');
        console.log(modal_title.find('i'));
        modal_title.find('i').removeClass().addClass('fas fa-plus');
        $('form')[0].reset();
        $('#myModalClient').modal('show');
    });

    $('#myModalClient').on('shown.bs.modal', function () {
        $('form')[0].reset();
    });

    $('form').on('submit', function (e) {
        e.preventDefault();
        //var parameters = $(this).serializeArray();
        var parameters = new FormData(this);
        submit_with_ajax(window.location.pathname, 'Notificación', '¿Estas seguro de realizar la siguiente acción?', parameters, function () {
            $('#myModalClient').modal('hide');
            tblClient.ajax.reload();
            //getData();
        });
    });
});