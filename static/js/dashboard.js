
window.onload = function() {


  load_data();
};

function logout(){
  sessionStorage.setItem('token','');
  window.location.href = "http://"+window.location.hostname+":"+window.location.port;
}

function load_data(){
    $("#ajax_loader").show();
    $('#id_card_div2').empty();
    // console.log(sessionStorage.getItem('token'));
  $.ajax({
    url: str_login_url,
    headers:{ "X-CSRFToken": str_csrf },
    data: {
       csrfmiddlewaretoken: str_csrf,
       'id':sessionStorage.getItem('token'),
        },
        cache: false,
       type: "POST",
       success: function(data,response) {
            $("#ajax_loader").hide();
           if (data['status'] == 'success') {

               $('#id_card_div2').append('<div class="col-xl-3 col-sm-6 mb-3"><div class="card text-white bg-danger o-hidden h-100"><div class="card-body"><div class="card-body-icon"><i class="fas fa-fw fa-list"></i></div><div class="mr-5">Opened Issues</div></div><span class="card-footer text-white clearfix small z-1" "><span class="float-left">'+data.project.opened_issues+'</span><span class="float-right"></span></span></div></div>');


             $('#id_card_div2').append('<div class="col-xl-3 col-sm-6 mb-3"><div class="card text-white bg-danger o-hidden h-100"><div class="card-body"><div class="card-body-icon"><i class="fas fa-fw fa-list"></i></div><div class="mr-5">Doing Issues</div></div><span class="card-footer text-white clearfix small z-1" "><span class="float-left">'+data.project.labeled_issues+'</span><span class="float-right"></span></span></div></div>');

             $('#id_card_div2').append('<div class="col-xl-3 col-sm-6 mb-3"><div class="card text-white bg-warning o-hidden h-100"><div class="card-body"><div class="card-body-icon"><i class="fas fa-fw fa-list"></i></div><div class="mr-5">Previous day commits</div></div><span class="card-footer text-white clearfix small z-1" "><span class="float-left">'+data.project.commits+'</span><span class="float-right"></span></span></div></div>');

             for (var int_itr = 0; int_itr < data.project.project.length; int_itr++) {

               var url_project = "http://" + window.location.hostname+":" + window.location.port+"/project/" + data.project.project[int_itr]["id"]

               $('#id_card_div2').append('<div class="col-xl-3 col-sm-6 mb-3" ><div class="card text-white bg-success o-hidden h-100"><div class="card-body"><div class="card-body-icon"><i class="fas fa-fw fa-shopping-cart"></i></div><div class="mr-5">'+data.project.project[int_itr]["project"]+'</div></div><a class="card-footer text-white clearfix small z-1" href="'+url_project+'"><span class="float-left">View Details</span><span class="float-right"><i class="fa fa-angle-right"></i></span></a></div></div>');
             }
           }
          //  http://+'window.location.hostname'+:+'window.location.port'+/project/
           else{
             $("#ajax_loader").hide();
             if (data.project == 'Authentication failed') {
               window.location.href = "http://"+window.location.hostname+":"+window.location.port;
             }
           }


       },
       error: function(xhr) {

       }
      });
}
