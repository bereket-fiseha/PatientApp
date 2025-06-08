

function genericFillEditModal(url,id){
  $.ajax({
      url: url +'/'+ id,
      headers: {
        "X-CSRFToken": $("input[name=csrfmiddlewaretoken]").val(),
      },
      type: "GET",
      data: {},
      success: function (result) {
        $.each(result[0]["fields"], function (key, value) {
          $("#" + key).val(value);
        });
        console.log(result)
      },
      error: function () {},
    });
 

}

  function genericSave(modelName,formUrl,modalId,formId,create_mode,edit_id) {

    var dict = {};
    var form_data = $("#" + formId).serializeArray();
    console.log(form_data)
    $.each(form_data, function (key, input) {
      dict[input.name] = input.value;
    });
      if (!create_mode && edit_id != undefined) {
        dict["id"] = edit_id;
      }
    $.ajax({
      url: formUrl,
      headers: {
        "X-CSRFToken": $("input[name=csrfmiddlewaretoken]").val(),
      },
      type: "POST",
      data: dict,
      success: onSaveSuccess(modelName,create_mode,modalId),
      error: onSaveError(modelName),
    });
  }

  function onSaveSuccess(modelName,create_mode,modalId){

    if (create_mode) {
      
      toastr.success( modelName+ " created successfully.");
    } else {
      toastr.success(modelName+" updated successfully.");
    }
    $("#"+modalId).modal("hide");

    setTimeout(function () {
       location.reload();
    }, 2000);

  }
  function onSaveError(modelName) {
    toastr.error("An error occurred while saving the "+ modelName);
  }
  function fillEditModal(getUrl){

$.ajax({
      url: getUrl,
      headers: {
        "X-CSRFToken": $("input[name=csrfmiddlewaretoken]").val(),
      },
      type: "GET",
      data: {

      },
      success: function (result) {

        $.each(result[0]["fields"], function(key, value) {
          $("#" + key).val(value);
        });
      },
      error: function () {},
    });
  }
 
  

 