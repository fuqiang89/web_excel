(function ($) {
    "use strict";

    var passwd = function (options) {
        this.init('passwd', options, passwd.defaults);
    };

    $.fn.editableutils.inherit(passwd, $.fn.editabletypes.abstractinput);

    $.extend(passwd.prototype, {
        render: function() {
           this.$input = this.$tpl.find('input');
        },

        value2html: function(value, element) {
            if(!value) {
                $(element).empty();
                return;
            }
            var html = '修改密码';
            $(element).html(html);
        },

        html2value: function(html) {
          return null;
        },

       value2str: function(value) {
           var str = '';
           if(value) {
               for(var k in value) {
                   str = str + k + ':' + value[k] + ';';
               }
           }
           return str;
       },

       str2value: function(str) {
           return str;
       },

       value2input: function(value) {
           if(!value) {
             return;
           }
           this.$input.filter('[name="oldPasswd"]').val(value.oldPasswd);
           this.$input.filter('[name="newPasswd"]').val(value.newPasswd);
           this.$input.filter('[name="retryPasswd"]').val(value.retryPasswd);
       },

       input2value: function() {
           return {
              oldPasswd: this.$input.filter('[name="oldPasswd"]').val(),
              newPasswd: this.$input.filter('[name="newPasswd"]').val(),
              retryPasswd: this.$input.filter('[name="retryPasswd"]').val()
           };
       },

       activate: function() {
            this.$input.filter('[name="oldPasswd"]').focus();
       },

       autosubmit: function() {
           this.$input.keydown(function (e) {
                if (e.which === 13) {
                    $(this).closest('form').submit();
                }
           });
       }
    });

    passwd.defaults = $.extend({}, $.fn.editabletypes.abstractinput.defaults, {
        tpl: '<div class="editable-passwd"><label><span>旧密码: </span><input type="password" name="oldPasswd" class="form-control input-small"></label></div>'+
             '<div class="editable-passwd"><label><span>新密码: </span><input type="password" name="newPasswd" class="form-control input-small"></label></div>'+
             '<div class="editable-passwd"><label><span>确认密码: </span><input type="password" name="retryPasswd" class="form-control input-small"></label></div>',
             
        inputclass: ''
    });

    $.fn.editabletypes.passwd = passwd;

}(window.jQuery));