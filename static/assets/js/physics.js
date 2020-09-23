Date.prototype.pattern = function (fmt) {
    var o = {
        "M+": this.getMonth() + 1, //月份
        "d+": this.getDate(), //日
        "h+": this.getHours() % 12 == 0 ? 12 : this.getHours() % 12, //小时
        "H+": this.getHours(), //小时
        "m+": this.getMinutes(), //分
        "s+": this.getSeconds(), //秒
        "q+": Math.floor((this.getMonth() + 3) / 3), //季度
        "S": this.getMilliseconds() //毫秒
    };
    var week = {
        "0": "/u65e5",
        "1": "/u4e00",
        "2": "/u4e8c",
        "3": "/u4e09",
        "4": "/u56db",
        "5": "/u4e94",
        "6": "/u516d"
    };
    if (/(y+)/.test(fmt)) {
        fmt = fmt.replace(RegExp.$1, (this.getFullYear() + "").substr(4 - RegExp.$1.length));
    }
    if (/(E+)/.test(fmt)) {
        fmt = fmt.replace(RegExp.$1, ((RegExp.$1.length > 1) ? (RegExp.$1.length > 2 ? "/u661f/u671f" : "/u5468") : "") + week[this.getDay() + ""]);
    }
    for (var k in o) {
        if (new RegExp("(" + k + ")").test(fmt)) {
            fmt = fmt.replace(RegExp.$1, (RegExp.$1.length == 1) ? (o[k]) : (("00" + o[k]).substr(("" + o[k]).length)));
        }
    }
    return fmt;
};


function show_confirm(text, data, show) {
    if (show) {
        var r = window.confirm(text);//window.confirm("Press a button");
        if (r === true) {
            var action = data["action"];
            if (action === "install_reset" || action === "re_install") {
                var b = confirm("确定不是客户机，重装数据会全部清除，后果自负,不能反悔！");
                if (!b) {
                    return
                }
            }
            run_Post_ajax(data);
        }
    } else {
        run_Post_ajax(data);

    }


}

function run_Post_ajax(data) {
    var date = new Date();
    var dd = date.pattern("yyyy-MM-dd hh:mm:ss");
    var phy_status = $("#phy-status");
    var action = data["action"];
    var ipmi = data["ipmi"];
    $(".loading").removeClass("hdle");
    phy_status.parent().children("div").children("div").append("<div>[" + dd + "]#" + ipmi + " " + action + "</div>");
    $.ajax({
        url: "",
        type: "POST",
        dataType: 'json',
        data: data,
        success: function (json) {
            $(".loading").addClass("hdle");
            if (json.result === "000") {
                // alert(json.desc)
                //成功后把其他按钮显示出来
                if (action === "status") {
                    var aa=json.data["status"];
                    // console.log(aa);
                    if (aa.indexOf("超时") === -1) {
                        phy_status.siblings("button").show();
                        $("#status").text(json.data["status"])
                    }
                }
                phy_status.parent().children("div").children("div").append("<div>" + json.data["ipmi"] + ":" + json.data["status"] + "</div>");
            } else {
                alert(json.result + ":" + json.desc);
            }

        }
    })
}

function run(data, confirm_str) {

    var phy_status = $("#phy-status");
    var ipmis = phy_status.attr("ipmis");
    var ipmi = ipmis.substring(0, ipmis.indexOf(","));
    var last_ipmi = ipmis.substring(ipmis.indexOf(",") + 1, ipmis.length);
    phy_status.attr("ipmis", last_ipmi);
    data["ipmi"] = ipmi;
    var show = phy_status.attr("show");
    if (show === "true") {
        phy_status.attr("show", "false");
        show_confirm(confirm_str, data, true);
    }
    else {
        show_confirm(confirm_str, data, false);
    }


}

function add_select(diquip) {
    if (diquip) {
        $(".loading").removeClass("hdle");
        var data = {action: "diquip", diqu: diquip};
        $.ajax({
            url: "",
            type: "POST",
            dataType: 'json',
            data: data,
            success: function (json) {
                $(".loading").addClass("hdle");
                if (json.result === "000") {
                    var select_tag = $("#jiaohuanip");
                    select_tag.empty();
                    var data = json.data;
                    select_tag.append("<option >" + "--------" + "</option>");
                    for (var item in data) {
                        select_tag.append("<option value='" + data[item]["ip_code"] + "'>" + data[item]["ip_desc"] + "</option>");
                    }


                }

            }
        })
    }
}

$(function () {
    //设置隐藏
    //$("#physics-status").removeClass("display-none").parent().siblings().children("div").addClass("display-none");
    // $("#physics-status").parent().siblings().children("div").addClass("display-none");
    var title_contents=$(".box-body .title-content");
    title_contents.children("p").click(function () {

        var class_str=$(this).next().attr("class");
        // console.log(class_str);
        if (class_str.toString().indexOf("display-none")>0){
            $(this).next().removeClass("display-none");
        }
        else {
            $(this).next().addClass("display-none");
        }

    });
    //初始化标题一
    var phy_status = $("#phy-status");
    phy_status.siblings("button").hide();
    phy_status.parent().children("div").children("div").append("<div>" + "操作内容在这里显示" + "</div>");

    //监听输入框
    phy_status.parent().siblings().find("input").bind("input propertychange", function (event) {
        var input_text = $(this).val();
        $("#status").text("未知");
        phy_status.siblings("button").hide();
    });
    phy_status.parent().children("button").click(function () {
        var ipmi = $(this).parent().siblings().children().find("input").val();
        if (ipmi.length < 1) {
            alert("请填入正确的ipmi");
            return;
        }
        var diqu = $(this).parent().siblings().find("select").val();
        if (diqu.length < 1) {
            alert("请填入相应的地区");
            return;
        }
        var action = $(this).attr("name");

        var ipmi_arry = ipmi.split(",");
        ipmi = "";
        for (j = 0; j < ipmi_arry.length; j++) {
            var ipmi_str = ipmi_arry[j];
            if (ipmi_str.split(".").length === 1) {
                if (ipmi_arry[j].length > 0) {
                    ipmi = ipmi.concat("172.16.200.".concat(ipmi_str));
                    ipmi = ipmi.concat(",");
                }

            } else {
                if (ipmi_arry[j].length > 0) {
                    ipmi = ipmi.concat(ipmi_arry[j]);
                    ipmi = ipmi.concat(",");
                }

            }

        }

        var attr_ipmi = "";
        for (i = 0; i < ipmi_arry.length; i++) {
            if (ipmi_arry[i].length < 1) {
                continue;
            }
            var show = true;
            if (i > 0) {
                show = false;
            }
            var ipmi_str12 = ipmi_arry[i];
            if (ipmi_str12.split(".").length === 1) {
                ipmi_str12 = "172.16.200.".concat(ipmi_str12);
            }
            var data = {ipmi: ipmi_str12, diqu: diqu, action: action};
            var confirm_str = "是否确定要操作ipmi为：" + ipmi + "的机器？";
            phy_status.attr("time", 1);
            if (!show) {
                if (action === "install_reset" ||  action === "re_install" ) {

                    phy_status.attr("time", 30);

                } else {
                    phy_status.attr("time", 1);
                }

            }
            attr_ipmi = attr_ipmi + ipmi_str12;
            attr_ipmi = attr_ipmi + ",";
        }

        phy_status.attr("ipmis", attr_ipmi);
        phy_status.attr("show", "true");
        var time = phy_status.attr("time");

        var attr_ipmi_arr = attr_ipmi.split(",");
        for (var i = 0; i < attr_ipmi_arr.length; i++) {
            if (attr_ipmi_arr[i].length > 0) {
                setTimeout(function () {
                    run(data, confirm_str);
                }, time * i * 2000);
            }

        }

    });

    //初始化标题二
    var phy_status2 = $("#phy-status-2");
    var jiaohuanip = $("#jiaohuanip");
    var select_tag = $("#jiaodiqu");
    select_tag.change(function () {
        var select_val = $(this).val();
        add_select(select_val);
    });

    phy_status2.parent().children("div").children("div").append("<div>" + "操作内容在这里显示1" + "</div>");
    phy_status2.parent().siblings().find("button").click(function () {
        var date = new Date();
        var dd = date.pattern("yyyy-MM-dd hh:mm:ss");
        var code = jiaohuanip.val();
        var diqu = select_tag.val();
        var command = $("#jiaohuancommand").val();
        var data = {action: "allinfo", code: code, diqu: diqu, command: command};
        var confirm_str = "是否确定要操作？";
        if (!confirm(confirm_str)) {
            return
        }
        phy_status2.parent().children("div").children("div").append("<div>[" + dd + "]#" + "info</div>");
        $(".loading").removeClass("hdle");
        $.ajax({
            url: "",
            type: "POST",
            dataType: 'json',
            data: data,
            success: function (json) {
                $(".loading").addClass("hdle");
                if (json.result === "000") {
                    phy_status2.parent().children("div").children("div").append("<pre>" + json.data["info"] + "<pre/>");
                } else {
                    alert(json.result + ":" + json.desc);
                }

            }
        });


    });

    //页面进去初始化
    // console.log(action);
    var action=$("#action").val();
    // console.log(action);
    for(var i=0;i<title_contents.length;i++) {
        var action_val=$(title_contents[i]).find(".action").val();
        // console.log(action_val);
        if (action===action_val){
            // console.log("111");
            $(title_contents[i]).children("p").click();
        }
    }

    //适配rdp全屏
    var connect_rdp = $("#conn_rdp");
    var widthInput = $("<input type='hidden' name='screenWidth' />");
    var heightInput = $("<input type='hidden' name='screenHeight' />");
    widthInput.attr("value", $(window).width());
    heightInput.attr("value", $(window).height());
    connect_rdp.append(widthInput);
    connect_rdp.append(heightInput);

    //监听查询机器状态
    $(".phy_status").click(function () {
        var ipmi=$(this).val();
        var diqu=$(this).attr("name");
        console.log(diqu);
        var content_first=$(title_contents.children("p")).first().next();
        content_first.removeClass("display-none");
        content_first.find(".ipmi").val(ipmi);
        var select_obj_s=content_first.find("option");
        for(var i=0;i<select_obj_s.length;i++){
            if(select_obj_s[i].value===diqu){
                select_obj_s[i].selected=true;
                location.href = "#physics-status";
            }
        }


    });
});
