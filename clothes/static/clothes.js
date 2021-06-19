$(window).on('cart-ready', function () {
    cart.beforeAdd = function ($btn) {
        var deferred = $.Deferred(),
            productId = $btn.data('product-id'),
            productSex = $btn.data('product-sex'),
            modal;

        if (!productSex) {
            deferred.resolve();
            return deferred.promise();
        }

        modal = new Modal({
            url: '/uk/clothes/sizes?product_id=' + productId,
            contentGetter: function (response) {
                return response.modal;
            },
            onSuccess: function () {
                deferred.resolve();
            },
            onCancel: function () {
                deferred.reject();
            },
            onFormRender: function ($modal, response) {
                $.each(['male', 'female'], function (i, sex) {
                    var $size = $modal.find('[name=' + sex + '-size]'),
                        sizes = response.sizes[sex];

                    $size.change(function () {
                        var values = sizes[$size.val()];
                        $.each(values, function (name, value) {
                            $modal
                                .find('[name=' + sex + '-' + name + ']')
                                .val(value);
                        });
                    });
                });
            }
        });

        modal.show();

        return deferred.promise();
    };
});
