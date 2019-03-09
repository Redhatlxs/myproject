/**
 * Created by tarena on 18-11-21.
 */

/**
 * 异步向服务器发送请求，检查用户是否处于登录状态
 * */
function check_login(){
  $.get('/check_login/',function(data){
    var html = "";
    if(data.loginStatus == 1){
      //有用户登录： 欢迎：xxx　退出
      html += "欢迎:"+data.uname;
      html += "&nbsp;&nbsp;&nbsp;&nbsp;";
      html += "<a href='/logout/'>退出</a>";
    }else{
      //无用户登录： [登录] [注册有惊喜]
      html += "<a href='/login/'>[登录]</a>";
      html += "<a href='/register/'>[注册有惊喜]</a>";
    }
    //将html赋值给#rightNav>li:first
    $("#rightNav>li:first").html(html);
  },'json');
}

function load_type_goods(){
  $.get('/load_type_goods/',function(data){
    // console.log(data);
    var html = "";
    $.each(data,function(i,obj){
      //将obj.type转换为js对象
      var jsonType = JSON.parse(obj.type);
      html+="<p>";
        html+="<a href='#'>更多</a>";
        html+="<img src='/"+jsonType.picture+"'>";
      html+="</p>";
      //读取obj.goods,并转换为js对象
      var jsonGoods = JSON.parse(obj.goods);
      $.each(jsonGoods,function(j,good){
        console.log(good);
        if((j+1) % 5 == 0){
          html+="<div class='item no-margin'>";
        }else{
          html+="<div class='item'>"
        }
          html+="<div class='proImg'>";
            html+="<img src='/"+good.fields.picture+"'>";
          html+="</div>"
          html+="<p>";
            html+=good.fields.title;
            html+="<img src='/static/images/cart.png'>";
          html+="</p>";
          html+="<span>";
            html+="&yen;"+good.fields.price+"/"+good.fields.spec;
          html+="</span>";
        html+="</div>";
      })
    });
    $("#main").html(html);
  },'json');
}

/**
 * 页面加载时要执行的内容
 * */
$(document).ready(function(){
  //检查用户的登录状态
  check_login();
  //加载所有类型和商品
  load_type_goods();
});








