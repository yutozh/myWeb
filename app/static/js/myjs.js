var isLogin = 0;
var first = true;
var chatShow = false;
var chat_page = 1;
var showLogin = function () {
    if (isLogin == 1) {
        $(".half-ring").toggleClass("open");
        $(".underdown").fadeToggle(500);
    }
    else {
        $(".login-grey").fadeToggle(500);
        $(".login-popup").fadeToggle(500);
        if (first) {
            register();
            first = false;
        }
    }
};
$(document).ready(function () {
    var bg = $("#bg");
    var cbg = $.cookie("bg");
    var bgn = 1;
    if(cbg === undefined || cbg.indexOf("bg") <0 )
        {
            $.cookie("bg", "../static/img/bg1.jpg", { path: 'oattao.cn/', expires: 10 });
            cbg =  "../static/img/bg1.jpg";
        }
    bgn = cbg.substring(cbg.indexOf("bg")+2,cbg.indexOf("bg")+3);
    bg.attr("src", $.cookie("bg"));

    var active = $("._content").attr("value");
    if(active != undefined ){
        $("#menu-" + active).addClass("nav-active");
    }
    $("body").css("min-height", ($(document).height()));
    isLogin = $(".login-hide").attr("value");
    if (isLogin == 0){
        $("#switch-img").attr("src","/static/img/userdefault.jpg")
    }
    $(".menu-center").click(showLogin);
    $(".chat-button").click(chatSelect);

    var changebg = $("#change-bg");
    changebg.click(function () {
        bgn = (bgn + 1) % 5 +1;
        $.cookie("bg","../static/img/bg" + bgn +".jpg", { path: 'oattao.cn/', expires: 10 });
        bg.fadeOut("slow");
        setTimeout(function () {
                bg.attr("src", $.cookie("bg"));
                bg.fadeIn("slow");
            }, 1000);
    });

});

$(".login-close-icon").click(function () {
    $(".login-grey").fadeOut();
    $(".login-popup").fadeOut();
});

$('.editor-type').click(function () {
    $('.editor-type-selected').attr("class", "editor-type");
    $(this).toggleClass("editor-type-selected");
});

var handlerEmbed = function (captchaObj) {
    $("#login-submit").click(function (e) {
        var validate = captchaObj.getValidate();
        if (!validate) {
            $("#notice")[0].className = "show";
            setTimeout(function () {
                $("#notice")[0].className = "hide";
            }, 2000);
            e.preventDefault();
        }
        else {
//            $.post("{{url_for('edit', username=user.username)}}", {title: title, body: connent, type:type});
            var username = $("#UserName").val();
            var password = $("#Psd").val();
            var isRemem = $("#isRemember").prop("checked");
            var csrf_token = $("#csrf_token").attr("value");
            $.ajax({
                url: "/login", // 进行二次验证
                type: "post",
                dataType: "json",
                data: {
                    // 二次验证所需的三个值
                    geetest_challenge: validate.geetest_challenge,
                    geetest_validate: validate.geetest_validate,
                    geetest_seccode: validate.geetest_seccode,
                    aim: "login",
                    username: username,
                    password: password,
                    remember: isRemem,
                    csrf_token: csrf_token
                },
                beforeSend: function () {
                    $("#login-submit").toggleClass("btn_disabled").attr("disabled", "true");
                    $(".login-submit-span").toggleClass("fa fa-spinner fa-spin");
                },
                success: function (data) {
                    if (data && (data.status === "success")) {
                        if (data.login_res == "ok") {
                            window.location.reload();
                        }
                        else {
                            $("#login-alert").html(data.login_res).show();
                            setTimeout(function () {
                                $("#login-alert").hide();
                            }, 5000);
                            captchaObj.refresh();
                            $("#login-submit").toggleClass("btn_disabled").removeAttr("disabled");
                            $(".login-submit-span").toggleClass("fa fa-spinner fa-spin");
                        }

                    } else {
                        alert("请求失败，请检查验证码是否滑动正确");
                        captchaObj.refresh();
                        $("#login-submit").toggleClass("btn_disabled").removeAttr("disabled");
                        $(".login-submit-span").toggleClass("fa fa-spinner fa-spin");
                        e.preventDefault();
                    }
                }
            });
        }
    });
    // 将验证码加到id为captcha的元素里
    captchaObj.appendTo("#embed-captcha");
    captchaObj.onReady(function () {
        $("#wait")[0].className = "hide";
    });
};

function register() {
    $("#embed-captcha").html("");
    $.ajax({
        // 获取id，challenge，success（是否启用failback）
        url: "/register?t=" + (new Date()).getTime(), // 加随机数防止缓存
        type: "get",
        dataType: "json",
        success: function (data) {
            // 使用initGeetest接口
            // 参数1：配置参数
            // 参数2：回调，回调的第一个参数验证码对象，之后可以使用它做appendTo之类的事件
            initGeetest({
                gt: data.gt,
                challenge: data.challenge,
                product: "float", // 产品形式，包括：float，embed，popup。注意只对PC版验证码有效
                offline: !data.success // 表示用户后台检测极验服务器是否宕机，一般不需要关注
            }, handlerEmbed);
        }
    });
}

function scoll(id) {
    $("html,body").animate({scrollTop: $(id).offset().top}, 500);
}

function chatSelect() {
    if (chatShow) {
        $(".right-chat").animate({"right": "-350px"}, 500);
        chatShow = false;
    }
    else {
        $(".right-chat").animate({"right": 0}, 500);
        // var chat_content = $(".chat-body-content");
        if (chat_page == 1) {
            $(".chat-body-content").html("");
            add_chat();
        }
        chatShow = true;
    }
}

$(".chat-body-content").scroll(function () {
    var t = $(this),
        viewH = t.height(),//可见高度
        contentH = t.get(0).scrollHeight,//内容高度
        scrollTop = t.scrollTop();//滚动高度
    //if(contentH - viewH - scrollTop <= 100) { //到达底部100px时,加载新内容
    if (scrollTop == (contentH - viewH)) { //到达底部100px时,加载新内容
        if (chat_page != 0) {
            setTimeout(add_chat, 1000);
        }
    }
});

function add_chat() {
    $.ajax(
        {
            url: "/ajax_post_get",
            type: "post",
            dataType: "json",
            data: {
                page: chat_page
            },
            success: function (data) {
                var res = "";
                $(data.content).each(function (i) {
                    res += '<div class="chat-post">\
                <img class="img-circle chat-chater-img" src="/static/user/user_img/' + this.authorimg + '" />\
                <span class="chat-chater-name">' + this.author + '</span>\
                <span class="chat-timestamp" style="float: right; margin-top: 4px">' + this.timestamp + '</span>\
                <div class="chat-chat-main">\
                ' + this.body + '\
                    </div>\
                <div class="chat-operator">\
                <a>评论</a>\
                <a>举报</a>\
                <span class="fa fa-thumbup"></span>\
                    </div>\
            </div>'

                });
                if (data.isEnd) {
                    res += "<div class='chat-temp'><p style='text-align: center'>没有更多留言了...</p></div>";
                    chat_page = 0;
                }
                else {
                    res += "<div class='chat-temp'><p style='text-align: center'><span class='fa fa-spinner fa-spin'></span>加载中，请稍候...</p></div>"
                    chat_page += 1;
                }
                $(".chat-temp").remove();
                $(".chat-body-content").append(res);
            }
        }
    );
}

$("#chat-submit").click(function (e) {
    var text = $("#chat-content-new").val();
    if (text.length > 140) {
        alert("字数不足或超出限制");
    }
    try {
        var user = $("#login-hide-forJudge").val().split(" ");
    }
    catch (ee) {
        showLogin();
        e.preventDefault();
    }
    if (user != "") {
        $.ajax(
            {
                url: "/ajax_post_add",
                type: "post",
                dataType: "json",
                data: {
                    content: text
                },
                success: function (data) {
                    if (data.result == "success") {
                        t = data.content;
                        $("#chat-content-new").val("");
                        res = '<div class="chat-post">\
                <img class="img-circle chat-chater-img" src="/static/user/user_img/' + t.authorimg + '"/>\
                <span class="chat-chater-name">' + t.author + '</span>\
                <span class="chat-timestamp" style="float: right; margin-top: 4px">' + t.timestamp + '</span>\
                <div class="chat-chat-main">\
                ' + t.body + '\
                    </div>\
                <div class="chat-operator">\
                <a>评论</a>\
                <a>举报</a>\
                <span class="fa fa-thumbup"></span>\
                    </div>\
            </div>';
                        $(".chat-body-content").prepend(res).animate({scrollTop: 0}, 1000);
                    }
                    else {
                        alert("提交失败，请检查内容是否超出限制");
                    }
                }
            }
        );
        e.preventDefault();
    }
});


