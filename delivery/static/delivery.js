
DeliveryForm = function (params) {

    var $deliveryMethod = params.$deliveryMethod,
        $city = params.$city,
        $warehouse = params.$warehouse,
        deliveryMethods = params.deliveryMethods,
        citiesUrl = params.citiesUrl,
        warehousesUrl = params.warehousesUrl;

    setEvents();
    handleDeliveryMethodChange();

    function setEvents() {
        $deliveryMethod.on('change', handleDeliveryMethodChange);
        $city.on('change', handleCityChange);
    }

    function handleDeliveryMethodChange() {

        var method = $deliveryMethod.val(),
            action = method == deliveryMethods.self_delivery ? 'hide' : 'show';

        $city.parent()[action]();
        $warehouse.parent()[action]();

        $city.autocomplete({
            serviceUrl: citiesUrl,
            width: 'auto',
            minChars: 2,
            onSelect: function () {
                $(this).trigger('change');
            }
        });

        $warehouse.autocomplete({
            serviceUrl: warehousesUrl,
            width: 'auto',
            minChars: 1,
            params: getWarehouseParams()
        });

    }

    function handleCityChange() {
        $warehouse.val('');
        $warehouse.autocomplete('setOptions', {params: getWarehouseParams()});
    }

    function getWarehouseParams() {
        return {
            delivery_method: $deliveryMethod.val(),
            city: $city.val()
        };
    }

};
