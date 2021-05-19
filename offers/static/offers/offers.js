
PriceOfferModal = function (params) {

    params.$target.click(function () {

        $.get(params.url, function (response) {

            var $modal = $(response),
                $submitBtn = $modal.find('button[type=submit]');

            $('body').append($modal);

            $modal.modal('show');

            $modal.on('hidden.bs.modal', function (e) {
                $modal.remove();
            });

            $modal.find('form').submit(function (e) {

                e.preventDefault();

                $submitBtn.prop('disabled', true);

                $(this).ajaxSubmit({
                    success: function(response) {
                        $modal.modal('hide');
                        if ($.notify) {
                            $.notify({message: response}, {type: 'success'});
                        }
                    },
                    error: function(response) {
                        $modal.find('.modal-body').html(response.responseText);
                        $submitBtn.prop('disabled', false);
                    }
                });
            });

        });

    });
};
