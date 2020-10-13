function close_delivery_modal() {
    $(".single-delivery-div").remove();
    $("#order-id-delivery-modal").val('');
    $("#show_delivery_modal").modal("hide");
}

function make_it(task) {

    var order_id = $("#orderID_DeliveryModal").val();

    if (order_id == "" || !order_id) {
        alert("Something went wrong!");
        return
    }


    $.ajax({
       url:     "/make_it_as",
       method:  "GET",
       data:    `task=${task}&orderID=${order_id}`,
       success: (response)=>{
          if (response.status == 1) {
              location.reload();
          }else{
              alert("Something went wrong");
          }
       }
    })

}

function show_delivery_modal(orderID) {
    
    $.ajax({
      url: "/getDeliveries",
      type: "GET",
      data: "order_id="+orderID,
      success: (response)=>{
        console.log(response);

        if (response.isCompleted) {
            $("#holder-options").css('display', 'none')
        }else{
            $("#holder-options").css('display', '')
        }

        console.log(typeof response.all_deliveries);

        $("#orderID_DeliveryModal").val(orderID);

        for (const key in response.all_deliveries) {
          if (response.all_deliveries.hasOwnProperty(key)) {
            const element = response.all_deliveries[key];
            console.log(element);
            $("#delivery-body").append(`
          
              <div class="card-body native-profile single-delivery-div">

                <div class="row px-2">
                  <div class="col-sm-1 px-0 d-flex align-items-center">
                    <i class="material-icons bg-success text-white p-1" style="border-radius: 100%; cursor: pointer;">done</i>
                  </div>

                  <div class="col-sm-7 d-flex align-items-center">
                    <h5>${element[1]}</h5>
                  </div>

                  <div class="col-sm-4 px-0">
                    <a href="media/${element[0]}" download>
                    <button type="button" class="btn btn-orange btn-block">Download</button>
                    </a>
                  </div>
                </div>

              </div>
            
            `);
            
          }
        }

        
      }

    })


    $("#show_delivery_modal").modal("show");
}

function allowdrop(event){
    event.preventDefault();
    var THIS = event.target;
    $(THIS).addClass("dragover");
    $("#showing_div").css("display", "none");

}

function now_drop(event){
    event.preventDefault();
    input = document.getElementById("target_file");
    input.files = event.dataTransfer.files;
    readURL(input, 'showing_div');

}

function previous_state(event){
      var THIS = event.target;
      $(THIS).removeClass("dragover");
}





function open_delivery_modal(orderID) {
    $("#order_id").val(orderID);
    $("#delivery_modal").modal("show");
}

function deliver_now(form) {
    var orderID = $("#order_id").val();
    var target_file = $("#target_file").val()

    if (orderID != "" && target_file != "" && target_file && orderID) {
       $("#deliver-form").submit();
    }else{
      alert("Please add a file for the delivery!")
    }
}

function readURL(input, show) {
    nameFile = input.files[0].name.split(".");
    nameFile = nameFile[nameFile.length-1];
    
    console.log(nameFile);
    if(nameFile=="docx" || nameFile=="pdf" || nameFile=="txt" || nameFile=="doc"){
        if (input.files && input.files[0]) {
            $("#file-error-msg").text("");

            console.log(input.files)

            var reader = new FileReader();

      

            reader.onload = function (e) {
                var result_to_show = e.target.result;
                console.log(result_to_show)
                
                $("#"+show).prop("class", "decrease-s-width");
                $('#'+show)
                    .attr('src', result_to_show)
                    .width('97%')
                    .height(500);

            };

            $("#success-msg").text("Your document has been attached!");

        }
    }else{
        $(`#target_file`).val(null);
        $("#success-msg").text("");
        alert("Invalid file type!");

    }
    
}


  



function upload_file(whick_input) {
      $("#"+whick_input).click();
}


function show_modal(id, file){
    $("#container").load("http://127.0.0.1:8000/media/"+file);
    // $("#container").load("http://Langvarsity.pythonanywhere.com/media/"+file);

    $("#modelId2").modal("show");
}
function go_to(file){
}

var current_status = 1;
function show_next_line() {

    if (current_status < 4) {
        $("#error_msg").text("");

        var current_org = $(`#org_${current_status}`).val();
        var current_year = $(`#year_${current_status}`).val();
        var current_type = $(`#type_${current_status}`).val();

        if (current_org == "" || current_year == "" || current_type == "" ) {
            $("#error_msg").text("Kindly fill the given fields to add new one!");
        }else{
            $("#error_msg").text("");

            console.log(current_org);
            console.log(current_year);
            console.log(current_type);

            // expand new line
            current_status += 1;

            $(`#line_${current_status}`).css('display', '')

        }

        
    }else{

      $("#error_msg").text("You can add maximum 4 experiences right now!");


    }

}