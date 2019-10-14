var $j = jQuery.noConflict();
getVehicles();

var object_file = {};

$j('input:file').change(function(e){

  let hasFile = $j('input:file').toArray().some(function(file) {
    object_file['image'] = e.target.files[0];
    return file.value;
  });

  $j('#btnSaveRefuel').prop('disabled', !hasFile);
});

$j('#datepickerA').attr('type', 'date');

function jsonFormat(formArray) {
  let returnArray = {};
  for (let i=0;i<formArray.length;i++) {
      if (formArray[i].value) {
          returnArray[formArray[i].name] = formArray[i].value;
      }
  }
  return returnArray;
}

function saveRefuel(formData){
  let form = $j('#formSaveRefuel');

  $j.ajax({
    type: form.attr('method'),
    url: form.attr('action'),
    data: JSON.stringify(formData),
    success: function(response){
      console.log(response);
      if(response.status){
        alert(response.msg);
      }
      else{
        alert(response.errors);
      }
    },
    error: function(e){
      console.log(e);
    }
  });
}

function getVehicles(){
  $j.ajax({
    type: 'GET',
    url: Dictionary.getVehicles,
    success: function(response){
      if(response.status){
        let data = JSON.parse(response.data);
        let vehiclesList = $('#vehiclesList');
        for(let i=0; i<data.length; i++){
          let vehicle = data[i].fields.alias;
          let option = document.createElement('option');

          option.text = vehicle;
          option.setAttribute('value', data[i].pk);
          vehiclesList.append(option);
        }
      }else{
        alert(response.msgError);
      }
    },
    error: function(e){
      console.log(e);
    }
  });
}

function validation(form){
  let result = [];
  //validationFields
  let formValidator = new FormValidation(form);

  result.push(formValidator.addValidation('liters', 'numeric', 'El campo solo debe contener números.'));
  result.push(formValidator.addValidation('amount', 'numeric', 'El campo solo debe contener números.'));
  result.push(formValidator.addValidation('vehiclesList', 'selection', '0'));


  for(let i=0; i<result.length; i++){
    if(!result[i]){ return false; }
  }

  return true;

}

$j('#formSaveRefuel').submit(function(e){
  e.preventDefault();

  //validation
  let form = document.querySelector('#formSaveRefuel');
  let result = validation(form);

  if(result){
    let formData = $j('#formSaveRefuel');
    let vehiclesList = document.querySelector('#vehiclesList');
    var data = new FormData(formData.get(0));

    data.append('vehicle_id', vehiclesList.options[vehiclesList.selectedIndex].value);

    $j.ajax({
      type: formData.attr('method'),
      url: formData.attr('action'),
      data: data,
      cache: false,
      processData: false,
      contentType: false,
      success: function(response){
        console.log(response);
        if(response.status){
          alert(response.msg);
        }
        else{
          alert(response.errors);
        }
      },
      error: function(e){
        console.log(e);
      }
    });
  }

});
