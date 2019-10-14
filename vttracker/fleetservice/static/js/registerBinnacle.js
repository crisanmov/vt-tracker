
var $j = jQuery.noConflict();

changesTypesInput();
getVehicles();

function changesTypesInput(){
  $('#timeS').attr('type', 'time');
  $('#timeE').attr('type', 'time');
  $('#dateB').attr('type', 'date');
}

function jsonFormat(formArray) {
  let returnArray = {};
  for (let i=0;i<formArray.length;i++) {
      if (formArray[i].value) {
          returnArray[formArray[i].name] = formArray[i].value;
      }
  }
  return returnArray;
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

function saveBinnacle(formData){
  let form = $j('#formSaveBinnacle');

  $j.ajax({
    type: form.attr('method'),
    url: form.attr('action'),
    data: formData,
    success: function(response){
      //console.log(response);
      if(response.status){
        alert(response.msg);
      }else{
        console.log(response.errors);
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

  //object with array validations
  let start_kilometer = {
		'fieldName': 'start_kilometer',
		'validations': [
			{ 'required': { 'msgError': 'El campo no debe estar vacio.' } },
			{ 'numeric': { 'msgError': 'El campo solo debe contener números.' } },
		]
	};

  let end_kilometer = {
		'fieldName': 'end_kilometer',
		'validations': [
			{ 'required': { 'msgError': 'El campo no debe estar vacio.' } },
			{ 'numeric': { 'msgError': 'El campo solo debe contener números.' } },
		]
	};

  /*
    validations for json object
    instance.addValidation(json_object);
  */
  result.push(formValidator.addValidationJson(start_kilometer));
  result.push(formValidator.addValidationJson(end_kilometer));

  /*
    validation only inputs
    instance.addValidation('name_input', 'validation_descriptor', 'msg error');
  */
  result.push(formValidator.addValidation('start_time', 'required', 'El campo no debe estar vacio.'));
  result.push(formValidator.addValidation('end_time', 'required', 'El campo no debe estar vacio.'));
  result.push(formValidator.addValidation('datetime', 'required', 'El campo no debe estar vacio.'));

  /*
    validation select
    instance.addValidation('name_input', 'validation_descriptor', 'value a validate');
  */
  result.push(formValidator.addValidation('route', 'selection', 'Seleccion'));
  result.push(formValidator.addValidation('vehiclesList', 'selection', '0'));

  for(let i=0; i<result.length; i++){

    if(!result[i]){ return false; }
  }

  return true;
}

$j('#btnSaveBinnacle').click(function(e){
  e.preventDefault();

  let form = document.querySelector('#formSaveBinnacle');
  let result = validation(form);

  if(result){
    let formData = jsonFormat($j('#formSaveBinnacle').serializeArray());
    let vehiclesList = document.querySelector('#vehiclesList');
    let vehicleSelected = vehiclesList.options[vehiclesList.selectedIndex].value;

    formData['vehicle_id'] = vehicleSelected;
    saveBinnacle(formData);
  }

});

$j('#vehiclesList').change(function(){
  let id_vehicle = $j('#vehiclesList option:selected').text();
  $j.ajax({
    type: 'GET',
    data: {'vehicle': id_vehicle, 'from_file': true},
    url: Dictionary.getCurrentMileagesVehicle,
    success: function(response){
      console.log(response);
      if(response.status){

          //let current_mileages = response.end_kilometer__max;
          let current_mileages = response.current_mileages;
          //console.log(current_mileages);

          if(current_mileages == 'null'){
            $j('#id_start_kilometer').prop('readonly', false);
          }

          $j('#id_start_kilometer').val(current_mileages);
          $j('#id_start_kilometer').prop('readonly', true);
          $j('#id_start_kilometer').css('color', 'green');
      }else{
        alert(response.msgError);
      }
    },
    error: function(e){
      console.log(e);
    }
  });

});

//##################  UTILS  ########################
$j(':input').keypress(function(){
  $j(this).css('color', 'black');
  $j(this).css('border-color', '');
});

$j('select').change(function(){
  $j(this).css('color', 'black');
  $j(this).css('border-color', '');
  $j(':input[name=start_kilometer]').css('border-color', '');
});

$j(':input[name=end_kilometer]').focus(function(){
  if($j(this).val() != ''){
    $j(this).val('');
  }
});

$j(':input[name=datetime]').focus(function(){
  $j(this).css('color', 'black');
  $j(this).css('border-color', '');
});
