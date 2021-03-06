(function () {
    $(document).ready(function() {
        /* Focus form field when clicking on error message. */
        $('#content-inner ul.errorlist a').click(function () {
                $($(this).attr('href')).focus();
                return false;
            });
    });
})();


/**
 * Handles autofill of text with default value for browsers that don't
 * support the HTML5 `placeholder` functionality.
 *
 * When an input field is empty, the default value (from `placeholder`
 * attribute) will be set on blur. Then, when focused, the value will
 * be set to empty.
 *
 */
 jQuery.fn.autoPlaceholderText = function () {
    // TODO: Make this CSS driven?
    var colors = ['#9b9b9b',  // default value grayed out
                  '#333'];    // focus value

    // check for html5 placeholder support and fallback to js solution
    if (!Modernizr.input.placeholder) {

        function onFocus() {
            var $this = $(this);
            if ($this.val() === $this.attr('placeholder')) {
                $this.val('').css('color',  colors[1]);
            }
        }

        function onBlur() {
            var $this = $(this);
            if ($this.val() === '') {
                $this.val($this.attr('placeholder')).css('color', colors[0]);
            }
        }

        this.each(function () {
            var $this = $(this);
            var placeholder = $this.attr('placeholder');
            if (placeholder) {
                if (!$this.val() || $this.val() === placeholder) {
                    $this.val(placeholder).css('color', colors[0]);
                }
                $this.focus(onFocus).blur(onBlur);
            }
        });

    }

    return this;
};
