function getCookie(obj,cookiename){
	var i,str;
	c = new Array();
	p = new Array("", "");
	str = document.cookie;c = str.split(";");
	for(i = 0; i < c.length; i++){
		if(c[i].indexOf(cookiename+"=") >= 0){
			p = (c[i].substr(c[i].indexOf("=")+1)).split("<>");
			break;
		}
	}
	if(cookiename == "SN_UPLOAD"){
		obj.pass.value =  unescape(p[0]);
		try{
			obj.postkey.value =  unescape(p[1]);
		}catch(e){}
	}else if(cookiename == "SN_DEL"){
		obj.delpass.value =  unescape(p[0]);
	}
	return true;
}
function delnoin(no){
	document.getElementById("Del").delno.value = no;
	document.getElementById("Del").del.focus();
}
var _onload = window.onload;
onload = function(e){
	getCookie(document.getElementById("Form"), 'SN_UPLOAD');
	getCookie(document.getElementById("Del"), 'SN_DEL');
};
