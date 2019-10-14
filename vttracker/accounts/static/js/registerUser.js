function jsonFormat(formArray) {
  let returnArray = {};
  for (let i=0;i<formArray.length;i++) {
      if (formArray[i].value) {
          returnArray[formArray[i].name] = formArray[i].value;
      }
  }
  return returnArray;
}

function validation(form){

  let result = [];
  //validationFields
  let formValidator = new FormValidation(form);

  result.push(formValidator.addValidation('name', 'required', 'El campo no debe estar vacio.'));
  result.push(formValidator.addValidation('lastP', 'required', 'El campo no debe estar vacio.'));
  result.push(formValidator.addValidation('lastM', 'required', 'El campo no debe estar vacio.'));
  result.push(formValidator.addValidation('phone', 'required', 'El campo no debe estar vacio.'));
  result.push(formValidator.addValidation('address', 'required', 'El campo no debe estar vacio.'));

  for(let i=0; i<result.length; i++){

    if(!result[i]){ return false; }
  }

  return true;

}

$('#btnSaveUser').click(function(e){
  e.preventDefault();

  //validation
  let form = document.querySelector('#formSaveUser');
  let result = validation(form);




  let formData = jsonFormat($("#formSaveUser").serializeArray());

  $.ajax({
    data: formData,
    type: form.attr('method'),
    url: form.attr('action'),
    success: function(response){
      if(response.status){
        alert(response.msg);
        window.location.replace("http://127.0.0.1:8000/accounts/register/");
      }

      if(!response.status){
        let errors = response.errors;
        let string = "";

        for(field in errors){
          let typeErrors = errors[field];

          for(let i=0; i < typeErrors.length; i++){
              string = " " + typeErrors[i];
          }

          alert(field + ":" + string);
          string = "";
        }
      }
    },
    error: function(e){
      console.log(e);
    }
  });
});
