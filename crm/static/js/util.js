function convertPhone(obj){
    number = obj.innerHTML;
    phone = number.replace(/^(\d{2,3})(\d{3,4})(\d{4})$/, `$1-$2-$3`);
    obj.innerHTML = phone;
}

function convertDate(obj){
    objText = obj.innerHTML;
    obj.innerHTML = objText.replace(/^(\d{4})(\d{2})(\d{2})(\d{2})(\d{2})(\d{2})$/, `$1-$2-$3 $4:$5:$6`)

}