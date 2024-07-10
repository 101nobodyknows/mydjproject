var acc = document.getElementsByClassName("faq_header");
    var i;

    for (i = 0; i < acc.length; i++) {
        acc[i].addEventListener("click", function() {
            this.classList.toggle("active");
            var panel = this.nextElementSibling;
            panel.classList.toggle("faq_open")
            // if (panel.classList === "faq_open") {
            //     panel.classList.remove("faq_open")
            // } else {
            //     panel.classList.add("faq_open")
            // }
        });
    }