	
function getBulletins(serviceName) {
    //var uri = '//<%= Request.Url.Host%>/Bulletins/api/' + serviceName + '/active'
    var uri = 'https://my.sa.ucsb.edu/Bulletins/api/' + serviceName + '/active';
    $(document).ready(function () {
        // Send an AJAX request
        $.getJSON(uri)
            .done(function (data) {
                // On success, 'data' contains a list of products.
                $.each(data, function (key, item) {
                    // Add a list item for the product.
                    $('<li />', { html: formatItem(item) }).appendTo($('#bulletins'));
                });

            });

        function formatItem(item) {
            return item;
        }
    });
}