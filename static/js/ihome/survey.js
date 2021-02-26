function chooseadd(obj){
      var ss= document.getElementsByName("address");
      for (var i = 0; i < ss.length; i++) {
          ss[i].checked = false;
      }
      obj.checked = true;
}

function choosehouse(obj){
      var ss= document.getElementsByName("house");
      for (var i = 0; i < ss.length; i++) {
          ss[i].checked = false;
      }
      obj.checked = true;
}

function chooseori(obj){
      var ss= document.getElementsByName("ori");
      for (var i = 0; i < ss.length; i++) {
          ss[i].checked = false;
      }
      obj.checked = true;
}
function choosefloor(obj){
      var ss= document.getElementsByName("storey");
      for (var i = 0; i < ss.length; i++) {
          ss[i].checked = false;
      }
      obj.checked = true;
}


$("button").click(function(){
    var choice = new Array();
    var choiceAdd = new Array();
    var choicelife = new Array();
    var choicehouse = new Array();
    var choiceori = new Array();
    var choicestorey = new Array();
    var choicebed= new Array();
    $('input:checkbox').each(function() {
        if ($(this).prop("checked")==true) {
            // console.log($(this).val())
            if($(this).prop("name") == "address") {
                choiceAdd.push($(this).val())
            }
            if($(this).prop("name") == "life") {
                choicelife.push($(this).val())
            }
            if($(this).prop("name") == "house") {
                choicehouse.push($(this).val())
            }
            if($(this).prop("name") == "ori") {
                choiceori.push($(this).val())
            }
            if($(this).prop("name") == "storey") {
                choicestorey.push($(this).val())
            }
            if($(this).prop("name") == "bed") {
                choicebed.push($(this).val())
            }
        }
    });
    choice.push(choiceAdd, choicelife, choicehouse, choicestorey, choiceori, choicebed)
    // console.log(choice);
    var token = $('input[name=csrfmiddlewaretoken]').val();
    $.ajax({
        url:'/survey',
        dataType:'json',
        type:'POST',
        data:{
            csrfmiddlewaretoken:token,
            choice:JSON.stringify(choice)
        },
        success: function (data) {
            console.log(data.res);
            url = '/' + 'surveylist' + '/' + data.url1 + '?area=' + data.area
            console.log(url)
            $(location).attr("href", url)

        }
    })
})