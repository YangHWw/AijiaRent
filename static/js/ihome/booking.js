function hrefBack() {
    history.go(-1);
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

function decodeQuery(){
    var search = decodeURI(document.location.search);
    return search.replace(/(^\?)/, '').split('&').reduce(function(result, item){
        values = item.split('=');
        result[values[0]] = values[1];
        return result;
    }, {});
}

function showErrorMsg() {
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function(){
            $('.popup_con').fadeOut('fast',function(){}); 
        },1000) 
    });
}

$(document).ready(function(){
    $(".input-daterange").datepicker({
        format: "yyyy-mm-dd",
        startDate: "today",
        language: "zh-CN",
        autoclose: true
    });
    $(".input-daterange").on("changeDate", function(){

        var startDate = $("#start-date").val();
        var endDate = $("#end-date").val();

        if (startDate && endDate && startDate > endDate) {
            showErrorMsg();
        } else {
            var sd = new Date(startDate);
            var ed = new Date(endDate);
            // console.log(sd)
            days = (ed - sd)/(1000*3600*24) + 1;
            var price = $(".house-text>p>span").html();
            var amount = days * parseFloat(price);
            $(".order-amount>span").html(amount.toFixed(2) + "(共"+ days +"晚)");
            var token = $('input[name=csrfmiddlewaretoken]').val();
        }
    });
})

document.onclick=function () {
    var obj = event.srcElement;
    if (obj.id == 'subbtn'){
        var obj = document.getElementById('beforeurl')
        var beforeurl = window.location.href.split('?')[1]
        console.log(beforeurl)
        var startDate = $("#start-date").val();
        var endDate = $("#end-date").val();
        var sd = new Date(startDate);
        var ed = new Date(endDate);
        days = (ed - sd)/(1000*3600*24) + 1;
        var price = $(".house-text>p>span").html();
        var amount = days * parseFloat(price);
        var token = $('input[name=csrfmiddlewaretoken]').val();
        console.log(startDate, endDate, price, amount)
        $.ajax({
            url:'/order/book',
            dataType:'json',
            type:'POST',
            data:{
                csrfmiddlewaretoken:token,
                startDate:startDate,
                endDate:endDate,
                price:price,
                amount:amount,
                beforeurl:beforeurl
            },
            success: function (data) {
                console.log(data.res);
                if(data.res == 1) {
                    var url = "/order/success";
                    $(location).attr("href", url)
                }
                else if(data.res == 0){
                    console.log(data)
                    alert('该房子在该时间段内被预定，正在为你推荐其他房子')
                    var url = "/search?";
                    url += ("aid=" + data.aid);
                    url += "&";
                    url += ("aname=" + data.areaname);
                    url += "&";
                    url += ("sd=" + data.st);
                    url += "&";
                    url += ("ed=" + data.et);
                    url += "&";
                    url += ("sort=" + 'new');
                    $(location).attr("href", url)
                }
            }
        })
    }
}