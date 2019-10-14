'use strict'

class FormValidation{

  constructor(form){
    this.form = form;
  }

  addValidation(fieldName, validationDescriptor, msgError){

		let validation;

		switch(validationDescriptor){
			case 'required':

				validation = this.required(fieldName, msgError);
				return (!validation ? false : true);

				break;
			case 'numeric':

				validation = this.numeric(fieldName, msgError);
        return (!validation ? false : true);

				break;
      case 'selection':

        validation = this.selection(fieldName, msgError);
        return (!validation ? false : true);

        break;

			default:
				console.log('Error: No se pudo validar el campo');
		}
	}


  addValidationJson(object2Validate){

    let validations = object2Validate.validations;
    let validation;

    for(let i=0; i<validations.length; i++){

      let key = Object.keys(validations[i])[0];
			let fieldName = object2Validate.fieldName;
			let msgError = validations[i][key].msgError;

      switch(key){
				case 'required':

					validation = this.required(fieldName, msgError)
					return (!validation ? false : true);

					break;
				case 'numeric':

					validation = this.numeric(fieldName, msgError)
					return (!validation ? false : true);

					break;
        case 'selection':

          validation = this.selection(fieldName, value, msgError);
          return (!validation ? false : true);

          break;
				default:
					console.log('Error: No se pudo validar el campo');
			}

    }
  }

  getForm(){
    return this.form;
  }

  required(fieldName, msgError){

    let form = this.getForm();

    if(form[fieldName].value == ""){

      if(msgError != ""){
        form[fieldName].value = msgError;
      }

      form[fieldName].style.color = "red";
      form[fieldName].style.borderColor = "red";

      return false;
    }

    return true
  }

  numeric(fieldName, msgError){

  	let form = this.getForm();
  	let rgx = /^[+-]?\d+(\.\d+)?$/;

  	if(!rgx.test(form[fieldName].value)){

        form[fieldName].value = msgError;
        form[fieldName].style.color = "red";
        form[fieldName].style.borderColor = "red";
        return false;
    }

    return true;
  }

  selection(fieldName, value){

    let form = this.getForm();

    if(form[fieldName].value === value){

      form[fieldName].style.color = "red";
      form[fieldName].style.borderColor = "red";
      return false;
    }

    return true;

  }

}
