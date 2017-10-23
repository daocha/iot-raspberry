function toogleLight(enabled){
	var csrftoken = getCookie('csrftoken');
	$.ajax({
		type: "POST",
		dataType: "json",
		contentType : "application/json",
		url: '/home/device/request',
		data: JSON.stringify({
			"control" : {"light" : enabled ? "1" : "0"}
		}),
		success: function(res){
			var msg = "";
			var notifyType = "success";
			if(res.success == 1){
				msg = "Operation succeeded: turning light " + (enabled?"on":"off") + " has been successfully requested.";
				notifyType = "success";
				$("#bulb").toggleClass("bulb");
				$("#bulb").toggleClass("bulb-disabled");
				$("#bulb").prop('onclick',null).off('click');
				$("#bulb").click(function(){
					toogleLight(!enabled);
				});
			}else{
				msg = "Operation failed: turning light " + (enabled?"on":"off") + " has been successfully requested.";
				notifyType = "danger";
			}
			$.notify({
				message: msg,
			},{
				// settings
				type: notifyType,
				delay: 3000,
				placement: {
					from: "top",
					align: "center"
				},
				animate: {
					enter: 'animated rubberBand',
					exit: 'animated bounceOutRight'
				}
			});
		}
	});
}