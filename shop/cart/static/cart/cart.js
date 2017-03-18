
AddToCartControl = function (params) {
    var self = this;
    this.csrf = params.csrf;
    this.url = params.url;
    this.$buttons = $('[data-role=add-to-cart-btn]');
    this.$totals = $('[data-role=cart-total]');

    this.$buttons.click(function () {
        var data = {
            csrfmiddlewaretoken: self.csrf,
            product_pk: $(this).data('product-pk')
        },
        $btn = $(this);

        $.post(self.url, data, function (response) {
            $btn.text(response.message).attr('disabled','disabled');
            self.$totals.text('(' + response.total + ')');
        });
    });
};
