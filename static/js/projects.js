
window.onload = function() {
  load_data();
};

function load_data(){
  $("#ajax_loader").show();
  $('#id_card_body').empty();
  $.ajax({
    url: str_project_url,
    data: {
       csrfmiddlewaretoken: str_csrf,
       'project_id':id,
       'id':sessionStorage.getItem('token'),
        },
        cache: false,
       type: "POST",
       success: function(data,response) {
         $("#ajax_loader").hide();
         if (data['status'] == 'success') {
           var back_url = "http://" + window.location.hostname+":" + window.location.port+"/dashboard/" + sessionStorage.getItem('token');

           $('#id_card_body').append('<div class="col-lg-4 col-md-4"><label for="">Opened Issues &nbsp;&nbsp;:</label><span>&nbsp;&nbsp;'+data.data.issues+'</span></div><div class="col-lg-4 col-md-4"><label for="">Doing Issues &nbsp;&nbsp;&nbsp;&nbsp; :</label><span>&nbsp;&nbsp;'+data.data.labeled+'</span></div><div class="col-lg-4 col-md-4"><label for="">Total Commits &nbsp;&nbsp; :</label><span>&nbsp;&nbsp;'+data.data.commits+'</span></div></div><a class="btn btn-primary btn-block" href="'+back_url+'">Back</a>');
         }
       },
       error: function(xhr) {
         $("#ajax_loader").hide();
       }
      });
}
