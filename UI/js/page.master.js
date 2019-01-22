class DisplayManager {
    constructor(selector_list) {
        this.selector_list = selector_list;
    }

    active(selector) {
        for(var i in this.selector_list){
			$(this.selector_list[i]).hide()
		}
		$(selector).show()
    }
}

var validation = {
    isNotEmpty:function (str) {
        var pattern =/\S+/;
        return pattern.test(str);  // returns a boolean
    },
    isNumber:function(str) {
        var pattern = /^\d+$/;
        return pattern.test(str);  // returns a boolean
    },
    isSame:function(str1,str2){
        return str1 === str2;
    }
};