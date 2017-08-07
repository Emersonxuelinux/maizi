//get或post方法
function do_ajax(){
    word = $("#word").val();
    //用键值对的形式向服务器传送数据，在django的views中也用相同名称获取数据
    //这个方法就是$.ajax()的简写形式
    if (word != ''){
        $.get('/search/', {'word':word}, function(data){
        //alert(data.length);
        //获得的data里面其实是一个字典，用each方法遍历出来
        //jQuery.parseJSON()函数用于将格式完好的JSON字符串转为与之对应的JavaScript对象。
        queries = $.parseJSON(data)
        str = ''
        $.each(queries,function(key,value){
            //具体取哪个字段可以在chrome的控制台查看一下返回的json文件内容
            //这种写法每次都会刷新，最后只会出现最后一条记录
            //$('#word_txt').html('<li>'+value.fields.title+'</li>')
            //为了实现自动填充功能，绑定一个事件，其中this指的是当前值
            //为了避免单引号失效，里面用双引号
            str += '<li id="this_li" onclick="autoCompelete(this)">'+value.fields.title+'</li>';
            if(str != ''){
                $('#drop_down').css('display','block');
                $('#word_txt').html(str)
            }
            else{
                $('#drop_down').css('display','none');
            }
            
        });
    });
    }
    else {
        $('#drop_down').css('display','none');
    }
    
}

function autoCompelete(obj){
    //alert($(obj).html())
    $("#word").val($(obj).html())
    $('#drop_down').css('display','none');
}