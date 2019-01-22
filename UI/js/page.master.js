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