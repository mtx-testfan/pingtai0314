//主要是把team的信息从数据库中查询出来，然后展现到页面上面
//前后端交互.ajax
function init_team(){
    var url= '/variable/api/v1/aggregate';
    var  data = {
        type:'team',   //表名  team表名
        key:'team'  //按照哪个字段进行查询 team字段
    };
    http(url,'post',data,function(data){
        console.log(data);
        //做一个动态的拼接，option拼接
        var html = '';
        //循环data数据  for(index in data['data']){}
        // index 索引值  0,1,2       data['data']array
        for(index in data['data']){
            //html的拼接
            html += '<option value="'+data['data'][index]['_id']+'">'+data['data'][index]['_id']+'</option>>'

        }
        //把option标签追加到select标签里面
        $('#team').append(html)
    },function(data){
        console.log(data)
    })
}



$(function(){
    init_team()
});