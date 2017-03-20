
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


CartItemControl = function (params) {
    var self = this;
    this.csrf = params.csrf;
    this.setQtyUrl = params.setQtyUrl;
    this.removeUrl = params.removeUrl;
    this.$container = params.$container;
    this.$totals = $('[data-role=cart-total]');

    this.productPk = this.$container.data('product-pk');
    this.$input = this.$container.find('[data-role=set-qty]');
    this.$plusQty = this.$container.find('[data-role=plus-qty]');
    this.$minusQty = this.$container.find('[data-role=minus-qty]');
    this.$remove = this.$container.find('[data-role=remove-cart-item]');
    this.$subtotal = this.$container.find('[data-role=cart-item-subtotal]');

    this.$input.change(function () {
        var data = {
            csrfmiddlewaretoken: self.csrf,
            product_pk: self.productPk,
            qty: $(this).val()
        };

        $.post(self.setQtyUrl, data, function (response) {
            self.$totals.text('(' + response.total + ')');
            self.$subtotal.text(response.subtotal);
        });
    });

    this.$plusQty.click(function() {
        var val = parseInt(self.$input.val());
        self.$input.val(val + 1).trigger('change');
    });

    this.$minusQty.click(function() {
        var val = parseInt(self.$input.val());
        if (val > 1) {
            self.$input.val(val - 1).trigger('change');
        }
    });

    this.$remove.click(function() {
        var data = {
            csrfmiddlewaretoken: self.csrf,
            product_pk: self.productPk
        };

        $.post(self.removeUrl, data, function (response) {
            self.$totals.text('(' + response.total + ')');
            self.$container.remove();
        });
    });
};
