$(function() {
    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    $.ajaxSetup({
        crossDomain: false, // obviates need for sameOrigin test
        /*beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type)) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }*/
        beforeSend: function(xhr, settings) {
             if (csrfSafeMethod(settings.type)) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
             }
             else{
                 function getCookie(name) {
                     var cookieValue = null;
                     if (document.cookie && document.cookie != '') {
                         var cookies = document.cookie.split(';');
                         for (var i = 0; i < cookies.length; i++) {
                             var cookie = jQuery.trim(cookies[i]);
                             // Does this cookie string begin with the name we want?
                             if (cookie.substring(0, name.length + 1) == (name + '=')) {
                                 cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                                 break;
                             }
                         }
                     }
                     return cookieValue;
                 }
                 if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                     // Only send the token to relative URLs i.e. locally.
                     xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                 }
             }
         }
    });

    var first_name = false;
    var last_name = false;
    var email = false;
    var password = false;
    var code = false;
    var fields = [];
    var content_object_data = '';
    var wrapper = $('.wrapper');
    var html = $('html');
    var password_correct = false;
    var empty_submit = false;

    var lat_error = 'Пишите в латинской раскладке';

    var append_html = function(html, wrapper) {
        wrapper.remove();
        $('body').append(html);
        var wrapper = $('.wrapper');
        wrapper.fadeIn(500);
        wrapper.css('height', $('.page-content').height());
        wrapper.css('display', 'block');
        fix_form_scrolling()
    };

    fix_form_scrolling = function() {
        var window_height = $(window).height();
        var floater = $('.wrapper-floater');
        var form_heiht = floater.height();
        var wrapper = $('.wrapper');

        var m = ( $(window).height() - floater.height() ) / 2;
        floater.css('margin-top', m + 'px');
        if (form_heiht > window_height - 10){
            var offset_heigth = floater.offset().top;
            wrapper.css('position', 'absolute');
            floater.css('top', $(window).scrollTop() + 'px');
            if (offset_heigth < 0)
                floater.css({'margin-top': '0px', 'top': '0px'});
        }
        else{
            if(wrapper.css('position') == 'absolute'){
                $('.wrapper').css('position', 'fixed');
                floater.css('top', '0px');
            }
        }
    };


    resize_login_form = function(scroll_mobile) {
        var wrapper = $('.wrapper');
        var floater = $('.wrapper-floater');
        var width = $(window).width();
        var containerWidth = floater.width();
        var leftMargin = (width - containerWidth) / 2;

        var isMobile = false;
        if(/(android|bb\d+|meego).+mobile|avantgo|bada\/|blackberry|blazer|compal|elaine|fennec|hiptop|iemobile|ip(hone|od)|ipad|iris|kindle|Android|Silk|lge |maemo|midp|mmp|netfront|opera m(ob|in)i|palm( os)?|phone|p(ixi|re)\/|plucker|pocket|psp|series(4|6)0|symbian|treo|up\.(browser|link)|vodafone|wap|windows (ce|phone)|xda|xiino/i.test(navigator.userAgent)
            || /1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\-)|ai(ko|rn)|al(av|ca|co)|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\-m|r |s )|avan|be(ck|ll|nq)|bi(lb|rd)|bl(ac|az)|br(e|v)w|bumb|bw\-(n|u)|c55\/|capi|ccwa|cdm\-|cell|chtm|cldc|cmd\-|co(mp|nd)|craw|da(it|ll|ng)|dbte|dc\-s|devi|dica|dmob|do(c|p)o|ds(12|\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8|ez([4-7]0|os|wa|ze)|fetc|fly(\-|_)|g1 u|g560|gene|gf\-5|g\-mo|go(\.w|od)|gr(ad|un)|haie|hcit|hd\-(m|p|t)|hei\-|hi(pt|ta)|hp( i|ip)|hs\-c|ht(c(\-| |_|a|g|p|s|t)|tp)|hu(aw|tc)|i\-(20|go|ma)|i230|iac( |\-|\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|kddi|keji|kgt( |\/)|klon|kpt |kwc\-|kyo(c|k)|le(no|xi)|lg( g|\/(k|l|u)|50|54|\-[a-w])|libw|lynx|m1\-w|m3ga|m50\/|ma(te|ui|xo)|mc(01|21|ca)|m\-cr|me(rc|ri)|mi(o8|oa|ts)|mmef|mo(01|02|bi|de|do|t(\-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|n30(0|2)|n50(0|2|5)|n7(0(0|1)|10)|ne((c|m)\-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg|pg(13|\-([1-8]|c))|phil|pire|pl(ay|uc)|pn\-2|po(ck|rt|se)|prox|psio|pt\-g|qa\-a|qc(07|12|21|32|60|\-[2-7]|i\-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h\-|oo|p\-)|sdk\/|se(c(\-|0|1)|47|mc|nd|ri)|sgh\-|shar|sie(\-|m)|sk\-0|sl(45|id)|sm(al|ar|b3|it|t5)|so(ft|ny)|sp(01|h\-|v\-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl\-|tdg\-|tel(i|m)|tim\-|t\-mo|to(pl|sh)|ts(70|m\-|m3|m5)|tx\-9|up(\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)|vk(40|5[0-3]|\-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|w3c(\-| )|webc|whit|wi(g |nc|nw)|wmlb|wonu|x700|yas\-|your|zeto|zte\-/i.test(navigator.userAgent.substr(0,4)))
            isMobile = true;

        if (isMobile){
            var scale = 1;
            if (window.matchMedia('(min-width : 320px)').matches) {
                scale = 0.9
            }
            else if(window.matchMedia('(min-width : 480px)').matches){
                scale = 1.3
            }
            else if(window.matchMedia('(min-width : 768px)').matches){
                scale = 2.1
            }
            else if(window.matchMedia('(min-width : 992px)').matches){
                scale = 2.7
            }

            if(scroll_mobile != 0){
                var meta = '<meta name="viewport" content="width=device-width, initial-scale=' + scale + '">';
                $('head').append(meta);

                width = $(document).width();
                var left = $(window).width() / 2 - 180;
                $('body').scrollLeft(width / 2 - 180 - left);
                $('body').scrollTop(floater.offset().top);
            }
        }
        else{
            floater.css("marginLeft", leftMargin);
        }
    };

    $(window).resize(function() {
        resize_login_form(0);
        fix_form_scrolling();
    });

    $(window).load(function() {
        if ($.cookie('toastmessage')){
            $('body').append($.cookie('toastmessage'));
            $.removeCookie("toastmessage");
        }
    });


    $(window).load(function() {
        if(typeof(template_show) !== 'undefined' && template_show){
            var params = {};
            if (app_info.object){
                params['contentType'] = app_info.object.ctype_id;
                params['objectId'] = app_info.object.id;
            }
            reg('social_reg', params);
        }
    });

    $(document).on('click', '.success-close', function(){
        $('.wrapper').fadeOut();
        if($('.element4 form').length > 0)
            find_fields($('.element4 form'));
        else if($('.subscription_form').length > 0)
            find_fields($('.subscription_form'));
        if($('.success-title', $('.wrapper')).length){
            if(!$('.banner-reminder-content').length)
                window.location = window.location.origin + window.location.pathname;
        }
    });
    // hide wrapper after clicking mouse on 'dark' part aside of .wrapper-floater
    $(document).on('click', '.wrapper', function(e){
        if ($(e.target).is('.wrapper')) {
            if (!login_required) {
                $('.wrapper').fadeOut();
                $('.tipsy').hide().remove();
                if($('.element4 form').length > 0)
                    find_fields($('.element4 form'));
                else if($('.subscription_form').length > 0)
                    find_fields($('.subscription_form'));
                if ($('.success-title', $('.wrapper')).length) {
                    if (!$('.banner-reminder-content').length)
                        window.location = window.location.origin + window.location.pathname;
                }
            }
        }
    });


    /* CUSTOM CHECKBOX */
    $(document).on('change', '#id_subscribed', function(){
        if($(this).attr('checked') == 'checked'){
            $(this).attr('checked', false);
            $('.checkbox_icon').removeClass('checkbox_checked')
        }
        else{
            $(this).attr('checked','checked');
            $('.checkbox_icon').addClass('checkbox_checked')
        }
        $('.checkbox_icon').removeClass('checkbox_hover')
    });
    $(document).on('mouseover', '.callback__checkbox', function(){
        $('.checkbox_icon').addClass('checkbox_hover')
    });
    $(document).on('mouseout', '.callback__checkbox', function(){
        $('.checkbox_icon').removeClass('checkbox_hover')
    });
    /* END CUSTOM CHECKBOX */

    $.urlParam = function(name){
        var results = new RegExp('[\?&]' + name + '=([^&#]*)').exec(window.location.href);
        if (results == null){
            return null;
        }else{
            return results[1] || 0;
        }
    };
    $(window).load(function() {
        if($.urlParam('subscription_link')){
            var params = {};
            params['subscription_link'] = $.urlParam('subscription_link');
            if ($.urlParam('account'))
                params['account'] = $.urlParam('account');
            reg('subscription', params, GetSubscriptionUrl);
        }
        if($.urlParam('confirm_email_link')){
            var params = {};
            params['confirm_email_link'] = $.urlParam('confirm_email_link');
            params['contentType'] = $.urlParam('contentType');
            params['objectId'] = $.urlParam('objectId');
            reg('confirm_email_link', params);
        }
    });
    /* END GET SUBSCRIPTION */
});
