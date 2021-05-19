
(function ($) {
    $(document).ready(function () {
        var $fields = $('[data-role=attibute-field]'),
            $category = $('[name=category]');

        function handleCategoryChange() {
            $fields.each(function () {
                var $field = $(this),
                    categoryIds = String($field.data('category-ids')).split(','),
                    $row = $field.closest('.multi-field');

                if($.inArray($category.val(), categoryIds) !== -1) {
                    $row.show();
                } else {
                    $row.hide();
                }

            });
        }

        $category.change(handleCategoryChange).trigger('change');

    });
})(django.jQuery);
