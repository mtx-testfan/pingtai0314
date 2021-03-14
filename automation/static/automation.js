//==动态拼接html代码==
//打开网址
function browser(){
    var html ='\
        <div class="row" command="browser">\
            <label>打开:</label>\
            <input type="text" placeholder="请输入url地址">\
        </div>\
        '
        //追加到空白的div中
        $('#cases').append(html)
}
//点击动作
function click(){
    var html = '\
        <div class="row" command="click">\
            <label>动作:</label>\
            <select>\
                <option value="click">click</option>\
            </select>\
        </div>\
        '
        //追加到空白的div中
        $('#cases').append(html)
}
//查找元素
function find(){
    var html = '\
        <div class="row" command="find">\
            <label>使用:</label>\
            <select>\
                <option value="xpath">xpath</option>\
                <option value="css selector">css selector</option>\
                <option value="name">name</option>\
                <option value="class name">class name</option>\
                <option value="id">id</option>\
                <option value="tag name">tag name</option>\
                <option value="link text">link text</option>\
                <option value="partial link text">partial link text</option>\
            </select>\
            <label>参数:</label>\
            <input type="text" placeholder="请输入参数的值">\
        </div>\
        '
        //追加到空白的div中
        $('#cases').append(html)
}
//输入文本
function send(){
    var html = '\
        <div class="row" command="send">\
            <label>填写:</label>\
            <input type="text" placeholder="请输入要填写的内容">\
        </div>\
        '
        //追加到空白的div中
        $('#cases').append(html)
}
// 等待的函数
function wait(){
    var html = '\
        <div class="row" command="wait">\
            <label>填写:</label>\
            <input type="text" placeholder="请输入要等待的时间">\
        </div>\
        '
        //追加到空白的div中
        $('#cases').append(html)
}
//自己构造解析参数传递给后台,收集参数传递给后台
function parse_parameters(html){
    var data = {}
    var command = $(html).attr('command')
    if (command=='browser'){
        data['command']='get'
        data['parameter']={
            'value':$(html).find('input').val()
        }
        }else if (command == "find"){
            data['command']='find'
            data['parameter']={
            'by':$(html).find('select').val(),
            'selector':$(html).find('input').val()
        }
        }else if (command == 'send'){
            data['command']='send'
            data['parameter']={
            'value':$(html).find('input').val()

        }
        }else if (command == 'click'){
            data['command']='click'
            data['parameter']={}
    }else if (command == 'wait'){
            data['command']='wait'
             data['parameter']={
            'value':$(html).find('input').val()
    }
    }else{
        console.log('错误的html')
    }
    console.log(data)
    return data

}

//实现case的时候，需要很多动作，然后依次判断，进行动态拼接html
function add_element(){
    var command = $('#option').val()
    if (command == 'browser'){
        browser()
    }else if(command == 'find'){
        find()

    }else if(command == 'send'){
        send()

    }else if(command == 'wait'){
        wait()

    }else if(command == 'click'){
        click()

    }else{
        alert('错误的方法')
    }

}


//定义run函数
function run(){
    //获取所有的拼接的测试步骤，div
    var list = $('#cases').find('div')
    //传递给后台的数据
    var data={
        //用例的名字
        'casename':$('#name').val(),
        //从前端收集到的操作命令
        'commands':[]
    }
    //item就是每一个命令拼接的div标签
    $(list).each(function(index,item){
        //解析出来的command是一个字典{}
        var command = parse_parameters(item)
        data['commands'].push(command)
    })
    console.log(data)
    var url = '/automation/api/v1/run'
    http(url,'post',data,success,fail)
}



//定义save函数
function save(){
    //获取所有的拼接的测试步骤，div
    var list = $('#cases').find('div')
    //传递给后台的数据
    var data={
        //用例的名字
        'casename':$('#name').val(),
        //从前端收集到的操作命令
        'commands':[]
    }
    //item就是每一个命令拼接的div标签
    $(list).each(function(index,item){
        //解析出来的command是一个字典{}
        var command = parse_parameters(item)
        data['commands'].push(command)
    })
    console.log(data)
    var url = '/automation/api/v1/save'
    http(url,'post',data,function(data){
        alert('保存成功')
    },fail)
}



$(function(){
//调用添加按钮
$('#command').click(add_element)
//调用保存按钮
$('#save').click(save)
//调用运行按钮
$('#run').click(run)



})