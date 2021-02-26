function hrefBack() {
    history.go(-1);
}

function decodeQuery(){
    var url = window.location.pathname;
    var houseid = url.split('/')[2]
    return houseid
}

$(document).ready(function(){
    var mySwiper = new Swiper ('.swiper-container', {
        loop: true,
        autoplay: 2000,
        autoplayDisableOnInteraction: false,
        pagination: '.swiper-pagination',
        paginationType: 'fraction'
    })
    $(".book-house").show();
})
$('.imgclick').click(function(){
    var statue = 0;
    if($(this).attr('src') == '/static/images/shoucang_black.png'){
        $(this).attr('src','/static/images/shoucang_red.png');
        statue = 1;
    }else{
        $(this).attr('src','/static/images/shoucang_black.png');
        statue = 0;
    }      
    console.log('statue',statue)
    var houseid = decodeQuery()
    var token = $('input[name=csrfmiddlewaretoken]').val();
    $.ajax({
        url:'/collect',
        dataType:'json',
        type:'POST',
        data:{
            csrfmiddlewaretoken:token,
            statue:statue,
            houseid:houseid
        },
        success: function (data){
            if(data.res == 1){
                console.log('收藏成功')
            }
            else if(data.res == 0){
                console.log('取消收藏')
            }
            else if(data.res == 2){
                $(location).attr("href", '/user/login')
            }
        }
    })
});