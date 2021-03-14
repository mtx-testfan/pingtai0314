//成功的回调函数 {'status':200, 'message':'get','data':data}
function success(data){
	//data指的是后台传给前端的数据，回调数据
	console.log(data)
}
//失败的回调函数 报错信息，异常
function fail(data){
 //回调失败你要对数据做什么处理
 console.log(data)

}

//最终想实现ajax的请求
function http(url,method,data,success,fail){
//三目式  变量 = 条件？满足条件的值:不满足条件的值
    data = method=='get'?data:JSON.stringify(data)
    $.ajax({
    url:url,
    type:method,
    dataType:'json',
    contentType:'application/json;charset=UTF-8',
    data:data,  //前端传递给后台的数据
    success:success,
    error:fail

    })
    }
