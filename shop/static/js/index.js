function order(gid, gname, price){
    data = [{
        'GOODS_NO': gid,
        'GOODS_NAME': gname,
        'GOODS_COUNT': 1,
        'GOODS_PRICE': price
    }]
    json_data = JSON.stringify(data);

    var form = document.getElementById('form')

    var json_input = document.createElement('input');
    json_input.setAttribute('type', 'hidden');
    json_input.setAttribute('name', 'goods');
    json_input.setAttribute('value', json_data);
    form.appendChild(json_input)

    form.submit();

}

function selectOrder(){
    var query = 'input[name="item"]:checked';
    var list = document.querySelectorAll(query);
    var data = [];
    list.forEach(e => {
        var item = e.value.split("$")
        data.push({
        'GOODS_NO': item[0],
        'GOODS_NAME': item[1],
        'GOODS_COUNT': 1,
        'GOODS_PRICE': item[2]
        })
        
    });
    console.log(data)
    json_data = JSON.stringify(data);

    var form = document.getElementById('form');

    var json_input = document.createElement('input');
    json_input.setAttribute('type', 'hidden');
    json_input.setAttribute('name', 'goods');
    json_input.setAttribute('value', json_data);
    form.appendChild(json_input);

    form.submit();
}