(function($){
$.extend({
    form:{
        beautify: function(selector){
            $(selector).each(function(){
                var tag = $(this)[0].tagName.toLocaleLowerCase(),
                width = $(this).outerWidth();
                //美化select表单
                if(tag == 'select'){
                    var li = '', selected='<div class="form-select-selected"><span>'+$(this).find("option:selected").text()+'</span><i></i></div>';
                    $(this).children('option').each(function(){
                        if(!!$(this).attr('selected')){
                            li += '<li class="form-child-selected">'+$(this).text()+'</li>';
                        }
                        else{
                            li += '<li>'+$(this).text()+'</li>';
                        }
                    })
                    $(this).hide();
                    $(this).after('<div class="form-select" >'+selected+'<ul>'+li+'</ul></div>');

                    $(this).next().find('.form-select-selected').click(function(e){
                        var ul = $(this).parent().children('ul'),
                        init=function(){
                            $('.form-select-selected').removeClass('click');
                            $('.form-select ul').hide();
                        };
                        init();
                        if(ul.css('display') == 'none'){
                            ul.show();    
                            $(this).addClass('click');
                        }
                        else{
                            ul.hide();
                            $(this).removeClass('click');
                        }
                        e.stopPropagation();
                        $(document).one("click", init);
                        
                    })

                    $(this).next().find('ul li').click(function(){
                        var select = $(this).parent().parent().prev(), index = $(this).index(), selected = $(this).parent().parent().find('.form-select-selected');
                        select.children('option').each(function(){
                            if($(this).index() == index){
                                $(this).prop('selected', true);
                            }
                            else{
                                $(this).prop('selected', false);
                            }
                        })
                        $(this).parent().children('li').removeClass('form-child-selected');
                        $(this).addClass('form-child-selected');
                        selected.children('span').html($(this).html());
                        selected.removeClass('click');
                        $(this).parent().hide();
                    })

                }
                else if(tag == 'input'){
                    //美化checkbox表单
                    if($(this).attr('type') == 'checkbox'){
                        if(typeof $(this).attr('switch') != 'undefined'){
                            var current = $(this);
                            $(this).hide();
                            var status = $(this).prop('checked');
                            $(this).after('<div class="form-switch"><ul><li class="on '+(status ? 'checked' : '')+'" title="已开启"><em></em>ON</li><li  title="已关闭" class="off '+(!status ? 'checked' : '')+'"><em></em>OFF</li></ul></div>');
                            $(this).next().find('ul li').click(function(){
                                if($(this).hasClass('on')){
                                    current.prop('checked', false);
                                }
                                else{
                                    current.prop('checked', true);
                                }
                                $(this).parent().find('li').addClass('checked');
                                $(this).removeClass('checked');
                            })
                        }
                    }
                }
            });
        },

        on: function(selector, event, callback){
            $(selector).each(function(){
                var parent = $(this), tag = $(this)[0].tagName.toLocaleLowerCase();
                if(tag == 'select'){
                    if($(this).next().hasClass('form-select')){
                        if(event == 'change'){
                            $(this).next().find('.form-select-selected').bind('DOMNodeInserted', function(){
                                callback.apply(this, [parent]);
                            })
                        }
                    }
                }
                else if(tag == 'input'){
                    if(parent.attr('type') == 'checkbox'){
                        if(typeof parent.attr('switch') != 'undefined'){
                            if(parent.next().hasClass('form-switch')){
                                parent.next().find('ul li').click(function(){
                                    callback.apply(this, [parent]);
                                })
                            }
                        }
                    }
                }
            })
        },

        post: function(item){
            var dataType = $(item).attr('data-type') != 'undefined' ? $(item).attr('data-type') : 'json';
            $.ajax({
                url: $(item).attr('action'),
                cache: false,
                type: 'POST',
                dataType: dataType,
                data: $(item).serialize(),
                success: function(res){
                    if(!res.success){
                        layer.msg(res.message,{icon:2,time:1000});
                    }
                    else{
                        if(!!res.url){
                            layer.msg(res.message, {icon: 6,time: 1000}, function(){
                                window.location.href = res.url;
                            });
                        }
                        else{
                            layer.msg(res.message);
                        }
                    }
                }
            })
            return false;
        }
    }
})
})(jQuery);